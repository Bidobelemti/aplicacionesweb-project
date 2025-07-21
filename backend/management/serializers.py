from rest_framework import serializers
from .models import Waiter, Menu

class WaiterSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Waiter.
    Convierte los objetos Waiter a formato JSON y viceversa.
    """
    class Meta:
        model = Waiter
        fields = ['id', 'nombre', 'genero', 'experiencia', 'sueldo', 'zona']

class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Menu.
    Convierte los objetos Menu a formato JSON y viceversa.
    """
    class Meta:
        model = Menu
        fields = ['id', 'nombre_del_plato', 'precio', 'disponibilidad']

