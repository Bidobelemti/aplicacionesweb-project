from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Waiter, Menu
from .serializers import WaiterSerializer, MenuSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los administradores (is_staff)
    crear y modificar objetos. El resto de usuarios solo pueden leer.
    """
    def has_permission(self, request, view):
        # Permite métodos seguros (GET, HEAD, OPTIONS) a cualquier usuario.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permite el resto de métodos (POST, PUT, DELETE) solo si el usuario es staff.
        return request.user and request.user.is_staff

class MenuViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar, crear, actualizar y eliminar platos del menú.
    - GET /menu/: Lista todos los platos.
    - POST /menu/: Crea un nuevo plato (solo para administradores).
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class WaiterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para listar los camareros.
    - GET /waiters/: Lista todos los camareros.
    No permite crear, actualizar o eliminar desde la API.
    """
    queryset = Waiter.objects.all()
    serializer_class = WaiterSerializer
    permission_classes = [permissions.IsAuthenticated]
