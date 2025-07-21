from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from decimal import Decimal
from itertools import chain
from operator import attrgetter
from django.contrib.auth import get_user_model # Asegúrate de que esta importación esté presente

from .models import EatInOrder, TakeAwayOrder, ShippingOrder, MenuItem, OrderItem
from .serializers import (
    EatInOrderSerializer, TakeAwayOrderSerializer, ShippingOrderSerializer,
    PolymorphicOrderSerializer, MenuItemSerializer, CreateOrderSerializer,
    OrderStatsSerializer
)

User = get_user_model() # Asegúrate de que esta línea esté presente

@api_view(['GET'])
def api_info(request):
    """
    GET /api/orders/ - Información de la API
    """
    return Response({
        'message': 'Bienvenido a la API de órdenes',
        'endpoints': {
            'orders': '/api/orders/',
            'eatin_orders': '/api/orders/eatin/',
            'takeaway_orders': '/api/orders/takeaway/',
            'shipping_orders': '/api/orders/shipping/',
            'menu_items': '/api/menu/'
        }
    })


class OrderListView(APIView):
    """
    GET /orders - Lista todas las órdenes de todos los tipos
    """
    def get(self, request):
        # Obtener todas las órdenes
        eatin_orders = EatInOrder.objects.all()
        takeaway_orders = TakeAwayOrder.objects.all()
        shipping_orders = ShippingOrder.objects.all()

        # Combinar y ordenar por fecha
        all_orders = sorted(
            chain(eatin_orders, takeaway_orders, shipping_orders),
            key=attrgetter('fecha'),
            reverse=True
        )

        # Aplicar filtros
        order_type = request.query_params.get('type')
        status_filter = request.query_params.get('status')
        zona_filter = request.query_params.get('zona')

        if order_type:
            # Aquí necesitaríamos un serializador polimórfico o lógico para diferenciar
            if order_type == 'eatin':
                all_orders = [o for o in all_orders if isinstance(o, EatInOrder)]
            elif order_type == 'takeaway':
                all_orders = [o for o in all_orders if isinstance(o, TakeAwayOrder)]
            elif order_type == 'shipping':
                all_orders = [o for o in all_orders if isinstance(o, ShippingOrder)]
            else:
                return Response({'error': 'Tipo de orden no válido'}, status=status.HTTP_400_BAD_REQUEST)

        if status_filter:
            all_orders = [o for o in all_orders if o.estado_pago == status_filter]

        if zona_filter:
            all_orders = [o for o in all_orders if o.zona == zona_filter]
        
        # Serializar los resultados
        serializer = PolymorphicOrderSerializer(all_orders, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def create_order_with_items(request):
    try:
        # Imprime la data cruda que llega al serializador
        print(f"DEBUG: Raw request.data: {request.data}")

        order_serializer = CreateOrderSerializer(data=request.data)

        if order_serializer.is_valid():
            print("DEBUG: Serializer is valid. Proceeding to create order...")
            validated_data = order_serializer.validated_data
            print(f"DEBUG: validated_data: {validated_data}")

            mesero_id = validated_data['mesero_id']
            order_type = validated_data['order_type']
            items_data = validated_data['items']
            
            # Obtener el mesero
            try:
                mesero = User.objects.get(id=mesero_id)
            except User.DoesNotExist:
                return Response(
                    {'error': f'Mesero con ID {mesero_id} no encontrado'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Calcular el monto base sumando los items
            monto_base = Decimal('0.00')
            for item_data in items_data:
                menu_item_id = item_data['menu_item_id']
                cantidad = item_data['cantidad']
                
                try:
                    menu_item = MenuItem.objects.get(id=menu_item_id)
                    if not menu_item.disponible:
                        return Response(
                            {'error': f'El item {menu_item.nombre} no está disponible'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    precio_unitario = item_data.get('precio_unitario', menu_item.precio)
                    monto_base += cantidad * precio_unitario
                    
                except MenuItem.DoesNotExist:
                    return Response(
                        {'error': f'MenuItem con ID {menu_item_id} no encontrado'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Crear datos comunes para la orden
            common_data = {
                'mesero': mesero,
                'monto': monto_base,
                'menu': ', '.join([f"{item['cantidad']}x MenuItem#{item['menu_item_id']}" for item in items_data]),
                'zona': validated_data.get('zona', 'center'),
                'numero_personas': validated_data.get('numero_personas', 1),
                'estado_pago': 'pending'
            }

            # Crear la orden según el tipo
            order = None
            if order_type == 'eatin':
                mesa = validated_data.get('mesa')
                if not mesa:
                    return Response(
                        {'error': 'Los pedidos en mesa requieren número de mesa'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                order = EatInOrder.objects.create(
                    **common_data,
                    mesa=mesa
                )
                
            elif order_type == 'takeaway':
                order = TakeAwayOrder.objects.create(**common_data)
                
            elif order_type == 'shipping':
                direccion_envio = validated_data.get('direccion_envio')
                telefono_contacto = validated_data.get('telefono_contacto')
                repartidor_id = validated_data.get('repartidor_id')
                
                if not direccion_envio or not telefono_contacto:
                    return Response(
                        {'error': 'Los pedidos con envío requieren dirección y teléfono'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                shipping_data = {
                    **common_data,
                    'direccion_envio': direccion_envio,
                    'telefono_contacto': telefono_contacto
                }
                
                if repartidor_id:
                    try:
                        repartidor = User.objects.get(id=repartidor_id)
                        shipping_data['repartidor'] = repartidor
                    except User.DoesNotExist:
                        return Response(
                            {'error': f'Repartidor con ID {repartidor_id} no encontrado'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                
                order = ShippingOrder.objects.create(**shipping_data)
            
            else:
                return Response(
                    {'error': 'Tipo de orden no válido'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Crear los OrderItems
            for item_data in items_data:
                menu_item = MenuItem.objects.get(id=item_data['menu_item_id'])
                precio_unitario = item_data.get('precio_unitario', menu_item.precio)
                
                order_item_data = {
                    'menu_item': menu_item,
                    'cantidad': item_data['cantidad'],
                    'precio_unitario': precio_unitario
                }
                
                # Asignar la orden según el tipo
                if order_type == 'eatin':
                    order_item_data['eatin_order'] = order
                elif order_type == 'takeaway':
                    order_item_data['takeaway_order'] = order
                elif order_type == 'shipping':
                    order_item_data['shipping_order'] = order
                
                OrderItem.objects.create(**order_item_data)

            # Recargar la orden para obtener los items relacionados
            order.refresh_from_db()

            # Serializar la respuesta
            if order_type == 'eatin':
                response_serializer = EatInOrderSerializer(order)
            elif order_type == 'takeaway':
                response_serializer = TakeAwayOrderSerializer(order)
            elif order_type == 'shipping':
                response_serializer = ShippingOrderSerializer(order)
            
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'Error al crear la orden: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PATCH'])
def update_order_status(request, order_type, order_id):
    """
    PATCH /orders/{type}/{id}/status - Actualiza el estado de una orden
    """
    # Mapeo de tipos a modelos
    model_mapping = {
        'eatin': EatInOrder,
        'takeaway': TakeAwayOrder,
        'shipping': ShippingOrder
    }

    if order_type not in model_mapping:
        return Response(
            {'error': 'Tipo de orden no válido'},
            status=status.HTTP_400_BAD_REQUEST
        )

    model = model_mapping[order_type]
    order = get_object_or_404(model, id=order_id)

    new_status = request.data.get('estado_pago')
    if new_status not in ['pending', 'paid', 'cancelled']:
        return Response(
            {'error': 'Estado no válido'},
            status=status.HTTP_400_BAD_REQUEST
        )

    order.estado_pago = new_status
    order.save()
    return Response({'message': f'Estado de la orden {order_id} actualizado a {new_status}'}, status=status.HTTP_200_OK)


# Clases para listado y detalle de tipos de órdenes específicos
class EatInOrderListCreateView(generics.ListCreateAPIView):
    queryset = EatInOrder.objects.all()
    serializer_class = EatInOrderSerializer

class EatInOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EatInOrder.objects.all()
    serializer_class = EatInOrderSerializer


class TakeAwayOrderListCreateView(generics.ListCreateAPIView):
    queryset = TakeAwayOrder.objects.all()
    serializer_class = TakeAwayOrderSerializer

class TakeAwayOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TakeAwayOrder.objects.all()
    serializer_class = TakeAwayOrderSerializer


class ShippingOrderListCreateView(generics.ListCreateAPIView):
    queryset = ShippingOrder.objects.all()
    serializer_class = ShippingOrderSerializer

class ShippingOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShippingOrder.objects.all()
    serializer_class = ShippingOrderSerializer


class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


@api_view(['GET'])
def get_order_stats(request):
    """
    GET /orders/stats/ - Obtiene estadísticas generales de órdenes.
    """
    total_orders = EatInOrder.objects.count() + TakeAwayOrder.objects.count() + ShippingOrder.objects.count()
    eatin_orders = EatInOrder.objects.count()
    takeaway_orders = TakeAwayOrder.objects.count()
    shipping_orders = ShippingOrder.objects.count()

    # Suma de montos para el total de ingresos
    total_revenue = Decimal('0.00')
    total_revenue += EatInOrder.objects.aggregate(Sum('monto'))['monto__sum'] or Decimal('0.00')
    total_revenue += TakeAwayOrder.objects.aggregate(Sum('monto'))['monto__sum'] or Decimal('0.00')
    total_revenue += ShippingOrder.objects.aggregate(Sum('monto'))['monto__sum'] or Decimal('0.00')

    pending_payments = (
        EatInOrder.objects.filter(estado_pago='pending').count() +
        TakeAwayOrder.objects.filter(estado_pago='pending').count() +
        ShippingOrder.objects.filter(estado_pago='pending').count()
    )
    paid_orders = (
        EatInOrder.objects.filter(estado_pago='paid').count() +
        TakeAwayOrder.objects.filter(estado_pago='paid').count() +
        ShippingOrder.objects.filter(estado_pago='paid').count()
    )

    stats = {
        'total_orders': total_orders,
        'eatin_orders': eatin_orders,
        'takeaway_orders': takeaway_orders,
        'shipping_orders': shipping_orders,
        'total_revenue': total_revenue,
        'pending_payments': pending_payments,
        'paid_orders': paid_orders,
    }

    serializer = OrderStatsSerializer(stats)
    return Response(serializer.data)