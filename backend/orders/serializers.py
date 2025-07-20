from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EatInOrder, TakeAwayOrder, ShippingOrder, MenuItem, OrderItem


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'full_name']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


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
    class Meta(BaseOrderSerializer.Meta):
        model = EatInOrder
        fields = BaseOrderSerializer.Meta.fields + ['servicio_mesa']
    
    def validate(self, data):
        if not data.get('mesa'):
            raise serializers.ValidationError("Los pedidos en mesa deben tener asignada una mesa")
        return data


class TakeAwayOrderSerializer(BaseOrderSerializer):
    class Meta(BaseOrderSerializer.Meta):
        model = TakeAwayOrder
        fields = BaseOrderSerializer.Meta.fields + ['empaque', 'tiempo_preparacion']


class ShippingOrderSerializer(BaseOrderSerializer):
    repartidor = UserSerializer(read_only=True)
    repartidor_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta(BaseOrderSerializer.Meta):
        model = ShippingOrder
        fields = BaseOrderSerializer.Meta.fields + [
            'direccion_envio', 'repartidor', 'repartidor_id', 'costo_envio',
            'telefono_contacto', 'tiempo_estimado_entrega'
        ]
    
    def validate(self, data):
        if not data.get('direccion_envio'):
            raise serializers.ValidationError("Los pedidos con envío deben tener una dirección")
        if not data.get('telefono_contacto'):
            raise serializers.ValidationError("Los pedidos con envío deben tener un teléfono de contacto")
        return data


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
    order_type = serializers.ChoiceField(choices=['eatin', 'takeaway', 'shipping'])
    mesero_id = serializers.IntegerField()
    numero_personas = serializers.IntegerField(min_value=1)
    zona = serializers.CharField()
    items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1
    )
    
    # Campos específicos
    mesa = serializers.IntegerField(required=False, allow_null=True)
    direccion_envio = serializers.CharField(required=False, allow_blank=True)
    telefono_contacto = serializers.CharField(required=False, allow_blank=True)
    repartidor_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_items(self, value):
        for item in value:
            if 'menu_item_id' not in item or 'cantidad' not in item:
                raise serializers.ValidationError("Cada item debe tener 'menu_item_id' y 'cantidad'")
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