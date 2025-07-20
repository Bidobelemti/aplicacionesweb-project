from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from decimal import Decimal
from itertools import chain
from operator import attrgetter

from .models import EatInOrder, TakeAwayOrder, ShippingOrder, MenuItem, OrderItem
from .serializers import (
    EatInOrderSerializer, TakeAwayOrderSerializer, ShippingOrderSerializer,
    PolymorphicOrderSerializer, MenuItemSerializer, CreateOrderSerializer,
    OrderStatsSerializer
)

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
            type_mapping = {
                'eatin': EatInOrder,
                'takeaway': TakeAwayOrder,
                'shipping': ShippingOrder
            }
            if order_type in type_mapping:
                all_orders = [o for o in all_orders if isinstance(o, type_mapping[order_type])]
        
        if status_filter:
            all_orders = [o for o in all_orders if o.estado_pago == status_filter]
            
        if zona_filter:
            all_orders = [o for o in all_orders if o.zona == zona_filter]
        
        serializer = PolymorphicOrderSerializer(all_orders, many=True, context={'request': request})
        
        return Response({
            'count': len(all_orders),
            'results': serializer.data
        })


class EatInOrderListCreateView(generics.ListCreateAPIView):
    """
    GET/POST /orders/eatin - Lista y crea pedidos en mesa
    """
    queryset = EatInOrder.objects.all()
    serializer_class = EatInOrderSerializer


class EatInOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/DELETE /orders/eatin/{id} - Detalle de pedido en mesa
    """
    queryset = EatInOrder.objects.all()
    serializer_class = EatInOrderSerializer


class TakeAwayOrderListCreateView(generics.ListCreateAPIView):
    """
    GET/POST /orders/takeaway - Lista y crea pedidos para llevar
    """
    queryset = TakeAwayOrder.objects.all()
    serializer_class = TakeAwayOrderSerializer


class TakeAwayOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/DELETE /orders/takeaway/{id} - Detalle de pedido para llevar
    """
    queryset = TakeAwayOrder.objects.all()
    serializer_class = TakeAwayOrderSerializer


class ShippingOrderListCreateView(generics.ListCreateAPIView):
    """
    GET/POST /orders/shipping - Lista y crea pedidos con envío
    """
    queryset = ShippingOrder.objects.all()
    serializer_class = ShippingOrderSerializer


class ShippingOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/DELETE /orders/shipping/{id} - Detalle de pedido con envío
    """
    queryset = ShippingOrder.objects.all()
    serializer_class = ShippingOrderSerializer


class MenuItemListCreateView(generics.ListCreateAPIView):
    """
    GET/POST /menu - Lista y crea items del menú
    """
    queryset = MenuItem.objects.filter(disponible=True)
    serializer_class = MenuItemSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria__icontains=categoria)
        return queryset


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/DELETE /menu/{id} - Detalle de item del menú
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


@api_view(['GET'])
def order_statistics(request):
    """
    GET /orders/stats - Obtiene estadísticas de órdenes
    """
    # Contar órdenes por tipo
    eatin_count = EatInOrder.objects.count()
    takeaway_count = TakeAwayOrder.objects.count()
    shipping_count = ShippingOrder.objects.count()
    total_count = eatin_count + takeaway_count + shipping_count
    
    # Calcular ingresos
    eatin_revenue = EatInOrder.objects.aggregate(total=Sum('total_pagar'))['total'] or Decimal('0')
    takeaway_revenue = TakeAwayOrder.objects.aggregate(total=Sum('total_pagar'))['total'] or Decimal('0')
    shipping_revenue = ShippingOrder.objects.aggregate(total=Sum('total_pagar'))['total'] or Decimal('0')
    total_revenue = eatin_revenue + takeaway_revenue + shipping_revenue
    
    # Contar por estado de pago
    pending_count = (
        EatInOrder.objects.filter(estado_pago='pending').count() +
        TakeAwayOrder.objects.filter(estado_pago='pending').count() +
        ShippingOrder.objects.filter(estado_pago='pending').count()
    )
    
    paid_count = (
        EatInOrder.objects.filter(estado_pago='paid').count() +
        TakeAwayOrder.objects.filter(estado_pago='paid').count() +
        ShippingOrder.objects.filter(estado_pago='paid').count()
    )
    
    stats_data = {
        'total_orders': total_count,
        'eatin_orders': eatin_count,
        'takeaway_orders': takeaway_count,
        'shipping_orders': shipping_count,
        'total_revenue': total_revenue,
        'pending_payments': pending_count,
        'paid_orders': paid_count,
    }
    
    serializer = OrderStatsSerializer(stats_data)
    return Response(serializer.data)


@api_view(['POST'])
def create_order_with_items(request):
    """
    POST /orders/create - Crea una orden completa con items
    """
    serializer = CreateOrderSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    order_type = validated_data['order_type']
    items_data = validated_data['items']
    
    # Calcular monto total
    total_monto = Decimal('0')
    menu_description = []
    
    for item_data in items_data:
        menu_item = get_object_or_404(MenuItem, id=item_data['menu_item_id'])
        cantidad = int(item_data['cantidad'])
        subtotal = menu_item.precio * cantidad
        total_monto += subtotal
        menu_description.append(f"{menu_item.nombre} x{cantidad}")
    
    # Preparar datos de la orden
    order_data = {
        'mesero_id': validated_data['mesero_id'],
        'numero_personas': validated_data['numero_personas'],
        'zona': validated_data['zona'],
        'monto': total_monto,
        'menu': ', '.join(menu_description),
    }
    
    # Crear orden según tipo
    try:
        if order_type == 'eatin':
            order_data['mesa'] = validated_data['mesa']
            order_serializer = EatInOrderSerializer(data=order_data)
            
        elif order_type == 'takeaway':
            order_serializer = TakeAwayOrderSerializer(data=order_data)
            
        elif order_type == 'shipping':
            order_data.update({
                'direccion_envio': validated_data['direccion_envio'],
                'telefono_contacto': validated_data['telefono_contacto'],
                'repartidor_id': validated_data.get('repartidor_id'),
            })
            order_serializer = ShippingOrderSerializer(data=order_data)
        
        if order_serializer.is_valid():
            order = order_serializer.save()
            
            # Crear items de la orden
            for item_data in items_data:
                menu_item = MenuItem.objects.get(id=item_data['menu_item_id'])
                cantidad = int(item_data['cantidad'])
                
                order_item_data = {
                    'menu_item': menu_item,
                    'cantidad': cantidad,
                    'precio_unitario': menu_item.precio
                }
                
                if order_type == 'eatin':
                    order_item_data['eatin_order'] = order
                elif order_type == 'takeaway':
                    order_item_data['takeaway_order'] = order
                elif order_type == 'shipping':
                    order_item_data['shipping_order'] = order
                
                OrderItem.objects.create(**order_item_data)
            
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
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
    
    # Serializar según el tipo
    serializer_mapping = {
        'eatin': EatInOrderSerializer,
        'takeaway': TakeAwayOrderSerializer,
        'shipping': ShippingOrderSerializer
    }
    
    serializer = serializer_mapping[order_type](order)
    return Response(serializer.data)