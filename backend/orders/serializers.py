# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import EatInOrder, TakeAwayOrder, ShippingOrder, MenuItem, OrderItem

# Usar get_user_model() en lugar de importar User directamente
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User

        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_id', 'cantidad', 'precio_unitario', 'subtotal']


class BaseOrderSerializer(serializers.ModelSerializer):
    mesero = UserSerializer(read_only=True)
    mesero_id = serializers.IntegerField(write_only=True)
    total_pagar = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    numero = serializers.CharField(read_only=True)
    order_type = serializers.CharField(source='get_order_type', read_only=True)
    
    class Meta:
        fields = [
            'id', 'fecha', 'numero', 'monto', 'menu', 'mesa', 'zona',
            'mesero', 'mesero_id', 'numero_personas', 'estado_pago',
            'total_pagar', 'order_type'
        ]


class EatInOrderSerializer(BaseOrderSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='eatin_items') 
    
    class Meta(BaseOrderSerializer.Meta):
        model = EatInOrder
        fields = BaseOrderSerializer.Meta.fields + ['mesa', 'servicio_mesa', 'items']


class TakeAwayOrderSerializer(BaseOrderSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='takeaway_items')
    
    class Meta(BaseOrderSerializer.Meta):
        model = TakeAwayOrder
        fields = BaseOrderSerializer.Meta.fields + ['empaque', 'tiempo_preparacion', 'items']


class ShippingOrderSerializer(BaseOrderSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='shipping_items')
    repartidor = UserSerializer(read_only=True)  # Añadir esto
    
    class Meta(BaseOrderSerializer.Meta):
        model = ShippingOrder
        fields = BaseOrderSerializer.Meta.fields + [
            'direccion_envio', 'telefono_contacto', 'repartidor', 
            'costo_envio', 'tiempo_estimado_entrega', 'items'
        ]


class PolymorphicOrderSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if isinstance(instance, EatInOrder):
            return EatInOrderSerializer(instance, context=self.context).data
        elif isinstance(instance, TakeAwayOrder):
            return TakeAwayOrderSerializer(instance, context=self.context).data
        elif isinstance(instance, ShippingOrder):
            return ShippingOrderSerializer(instance, context=self.context).data
        else:
            raise serializers.ValidationError("Tipo de orden no reconocido")


class CreateOrderSerializer(serializers.Serializer):
    mesero_id = serializers.IntegerField(write_only=True)
    order_type = serializers.CharField(write_only=True)
    mesa = serializers.IntegerField(required=False, allow_null=True)
    zona = serializers.CharField(required=False)
    numero_personas = serializers.IntegerField(required=False, allow_null=True)
    direccion_envio = serializers.CharField(required=False, allow_blank=True)
    telefono_contacto = serializers.CharField(required=False, allow_blank=True)
    repartidor_id = serializers.IntegerField(required=False, allow_null=True)

    items = OrderItemSerializer(many=True, write_only=True)

    def validate_items(self, value):
        for item in value:
            if 'menu_item_id' not in item or 'cantidad' not in item:
                raise serializers.ValidationError("Cada item debe tener 'menu_item_id' y 'cantidad'")
        return value
    
    def validate_zona(self, value):
        valid_zones = ['north', 'south', 'east', 'west', 'center']
        if value and value not in valid_zones:
            raise serializers.ValidationError(f"Zona debe ser una de: {', '.join(valid_zones)}")
        return value
    
    def validate(self, data):
        order_type = data.get('order_type')
        
        if order_type == 'eatin' and not data.get('mesa'):
            raise serializers.ValidationError("Los pedidos en mesa requieren número de mesa")
        
        if order_type == 'shipping':
            if not data.get('direccion_envio'):
                raise serializers.ValidationError("Los pedidos con envío requieren dirección")
            if not data.get('telefono_contacto'):
                raise serializers.ValidationError("Los pedidos con envío requieren teléfono")
        
        return data

class OrderStatsSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    eatin_orders = serializers.IntegerField()
    takeaway_orders = serializers.IntegerField()
    shipping_orders = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    pending_payments = serializers.IntegerField()
    paid_orders = serializers.IntegerField()