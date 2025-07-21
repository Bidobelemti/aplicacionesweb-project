from django.db import models
from django.core.validators import MinValueValidator
import decimal

class Waiter(models.Model):
    """
    Modelo para representar a un camarero.
    """
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    nombre = models.CharField(max_length=100, help_text="Nombre completo del camarero")
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, help_text="Género del camarero")
    experiencia = models.PositiveIntegerField(default=0, help_text="Años de experiencia")
    sueldo = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(decimal.Decimal('0.01'))], help_text="Sueldo mensual del camarero")
    zona = models.CharField(max_length=50, help_text="Zona del restaurante asignada")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Camarero"
        verbose_name_plural = "Camareros"
        ordering = ['nombre']


class Menu(models.Model):
    """
    Modelo para representar un plato del menú.
    """
    nombre_del_plato = models.CharField(max_length=150, unique=True, help_text="Nombre del plato")
    precio = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(decimal.Decimal('0.01'))], help_text="Precio del plato")
    disponibilidad = models.BooleanField(default=True, help_text="Indica si el plato está disponible")

    def __str__(self):
        return f"{self.nombre_del_plato} - {'Disponible' if self.disponibilidad else 'No Disponible'}"

    class Meta:
        verbose_name = "Plato del Menú"
        verbose_name_plural = "Platos del Menú"
        ordering = ['nombre_del_plato']
