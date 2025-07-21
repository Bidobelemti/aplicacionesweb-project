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
            print("DEBUG: Serializer is valid. Proceeding to create order...") # Deja este print para depurar
            validated_data = order_serializer.validated_data
            print(f"DEBUG: validated_data: {validated_data}") # Deja este print para depurar

            mesero_id = validated_data['mesero_id']
            order_type = validated_data['order_type']
            items_data = validated_data['items']
            order = None

            # ... (Toda la lógica de creación de EatInOrder, TakeAwayOrder, ShippingOrder y OrderItem) ...

            # Esto es lo que debería retornar una vez creada la orden
            if order_type == 'eatin':
                response_serializer = EatInOrderSerializer(order)
            elif order_type == 'takeaway':
                response_serializer = TakeAwayOrderSerializer(order)
            elif order_type == 'shipping':
                response_serializer = ShippingOrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        else:
            # Esto debería capturar los errores de validación si la data es inválida
            print(f"DEBUG: Serializer is NOT valid.")
            print(f"DEBUG: Type of order_serializer.errors: {type(order_serializer.errors)}")
            print(f"DEBUG: Content of order_serializer.errors: {order_serializer.errors}")
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        import traceback
        traceback.print_exc() # Esto imprimirá el rastro completo del error en la consola
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