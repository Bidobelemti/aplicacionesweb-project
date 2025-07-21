from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TableViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'salas', TableViewSet)
router.register(r'reservas', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
