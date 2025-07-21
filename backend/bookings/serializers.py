from rest_framework import serializers
from .models import Booking, Table
from management.models import Waiter
from management.serializers import WaiterSerializer  # Asegúrate de tenerlo

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    waiter = WaiterSerializer(read_only=True)
    waiter_id = serializers.PrimaryKeyRelatedField(
        queryset=Waiter.objects.all(), write_only=True, source='waiter', required=False
    )

    class Meta:
        model = Booking
        fields = ['id', 'customer', 'table', 'date', 'time', 'waiter', 'waiter_id']
        read_only_fields = ['customer', 'waiter']

    def validate(self, data):
        table = data.get('table')

        # Verificar si la mesa está disponible
        if table and not table.is_available:
            raise serializers.ValidationError("La mesa seleccionada ya está ocupada.")

        return data
