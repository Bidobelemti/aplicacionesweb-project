from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Table, Booking
from .serializers import TableSerializer, BookingSerializer

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
