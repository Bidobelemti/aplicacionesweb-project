from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, WaiterViewSet

# Creamos un router para registrar nuestros ViewSets
router = DefaultRouter()
router.register(r'menu', MenuViewSet, basename='menu')
router.register(r'waiters', WaiterViewSet, basename='waiter')

# Las URLs de la API son determinadas automáticamente por el router.
urlpatterns = [
    path('', include(router.urls)),
]
