from django.contrib import admin
from django.contrib import admin
from .models import Waiter, Menu

@admin.register(Waiter)
class WaiterAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administrador para el modelo Waiter.
    """
    list_display = ('nombre', 'genero', 'experiencia', 'sueldo', 'zona')
    list_filter = ('zona', 'genero')
    search_fields = ('nombre', 'zona')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administrador para el modelo Menu.
    """
    list_display = ('nombre_del_plato', 'precio', 'disponibilidad')
    list_filter = ('disponibilidad',)
    search_fields = ('nombre_del_plato',)
    list_editable = ('precio', 'disponibilidad')