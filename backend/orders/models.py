from django.db import models
#from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class AbstractOrder(models.Model):
    """
    Clase abstracta que define la estructura común de todos los pedidos
    """
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('cancelled', 'Cancelado'),
    ]
    
    ZONE_CHOICES = [
        ('north', 'Norte'),
        ('south', 'Sur'),
        ('east', 'Este'),
        ('west', 'Oeste'),
        ('center', 'Centro'),
    ]
    
    fecha = models.DateTimeField(auto_now_add=True)
    numero = models.CharField(max_length=20, unique=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    menu = models.TextField()
    mesa = models.PositiveIntegerField(null=True, blank=True)
    zona = models.CharField(max_length=10, choices=ZONE_CHOICES, default='center')
    mesero = models.ForeignKey(User, on_delete=models.CASCADE, related_name='_orders_assigned_to_user')
    numero_personas = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    estado_pago = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    total_pagar = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    class Meta:
        abstract = True
        ordering = ['-fecha']
    
    def calcular_total(self):
        """
        Método que debe ser implementado por las subclases
        """
        raise NotImplementedError("Las subclases deben implementar calcular_total()")
    
    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self.generar_numero()
        self.total_pagar = self.calcular_total()
        super().save(*args, **kwargs)
    
    def generar_numero(self):
        """
        Genera un número único para la orden
        """
        return f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    def __str__(self):
        return f"{self.numero} - {self.get_order_type()} - ${self.total_pagar}"
    
    def get_order_type(self):
        return self.__class__.__name__


class EatInOrder(AbstractOrder):
    """
    Pedido para consumir en el restaurante
    """
    mesero = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eatin_orders_assigned', verbose_name='Mesero')
    servicio_mesa = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('2.50'))
    
    class Meta:
        verbose_name = "Pedido en mesa"
        verbose_name_plural = "Pedidos en mesa"
    
    def calcular_total(self):
        return self.monto + self.servicio_mesa
    
    def generar_numero(self):
        return f"MESA-{uuid.uuid4().hex[:8].upper()}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.mesa:
            raise ValidationError("Los pedidos en mesa deben tener asignada una mesa")
        super().clean()


class TakeAwayOrder(AbstractOrder):
    """
    Pedido para llevar
    """
    mesero = models.ForeignKey(User, on_delete=models.CASCADE, related_name='takeaway_orders_assigned', verbose_name='Mesero')
    empaque = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.00'))
    tiempo_preparacion = models.PositiveIntegerField(default=15)
    
    class Meta:
        verbose_name = "Pedido para llevar"
        verbose_name_plural = "Pedidos para llevar"
    
    def calcular_total(self):
        return self.monto + self.empaque
    
    def generar_numero(self):
        return f"LLEVAR-{uuid.uuid4().hex[:8].upper()}"


class ShippingOrder(AbstractOrder):
    """
    Pedido con envío a domicilio
    """
    mesero = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_orders_assigned', verbose_name='Mesero')
    direccion_envio = models.TextField()
    repartidor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='entregas')
    costo_envio = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('3.00'))
    telefono_contacto = models.CharField(max_length=15)
    tiempo_estimado_entrega = models.PositiveIntegerField(default=30)
    
    class Meta:
        verbose_name = "Pedido con envío"
        verbose_name_plural = "Pedidos con envío"
    
    def calcular_total(self):
        return self.monto + self.costo_envio
    
    def generar_numero(self):
        return f"ENVIO-{uuid.uuid4().hex[:8].upper()}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.direccion_envio:
            raise ValidationError("Los pedidos con envío deben tener una dirección")
        if not self.telefono_contacto:
            raise ValidationError("Los pedidos con envío deben tener un teléfono de contacto")
        super().clean()


class MenuItem(models.Model):
    """
    Modelo para los items del menú
    """
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Item del menú"
        verbose_name_plural = "Items del menú"
        ordering = ['categoria', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class OrderItem(models.Model):
    """
    Modelo para los items de cada orden
    """
    eatin_order = models.ForeignKey(EatInOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='eatin_items')
    takeaway_order = models.ForeignKey(TakeAwayOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='takeaway_items')
    shipping_order = models.ForeignKey(ShippingOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='shipping_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        verbose_name = "Item de la orden"
        verbose_name_plural = "Items de la orden"
    
    def save(self, *args, **kwargs):
        if not self.precio_unitario:
            self.precio_unitario = self.menu_item.precio
        super().save(*args, **kwargs)
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"{self.menu_item.nombre} x{self.cantidad}"