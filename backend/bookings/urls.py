from django.urls import path
from .views import ListTablesView, CreateBookingView, MyBookingsView, DeleteBookingView

urlpatterns = [
    path('salas/', ListTablesView.as_view(), name='salas'),
    path('reservas/', CreateBookingView.as_view(), name='crear_reserva'),
    path('reservas/mis-reservas/', MyBookingsView.as_view(), name='mis_reservas'),
    path('reservas/<int:pk>/', DeleteBookingView.as_view(), name='eliminar_reserva'),
]
