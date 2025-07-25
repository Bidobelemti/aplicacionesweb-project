from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework import generics, permissions
from .models import Table, Booking
from .serializers import TableSerializer, BookingSerializer
from rest_framework.response import Response

class ListTablesView(generics.ListAPIView):
    queryset = Table.objects.filter(is_available=True)
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]


class CreateBookingView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.save(customer=self.request.user)
        # Marcamos la mesa como no disponible
        booking.table.is_available = False
        booking.table.save()



class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)

class DeleteBookingView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)

    def perform_destroy(self, instance):
        # Liberamos la mesa al borrar la reserva
        instance.table.is_available = True
        instance.table.save()
        instance.delete()
