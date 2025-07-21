from django.db import models
from django.conf import settings  # Esto detecta automáticamente a Customer como modelo de usuario
from management.models import Waiter

class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Mesa {self.number} (Capacidad: {self.capacity})"


class Booking(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    waiter = models.ForeignKey(Waiter, null=True, blank=True, on_delete=models.SET_NULL, related_name='bookings')
    zone = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.customer.email} en la mesa {self.table.number} para {self.date} {self.time}"

