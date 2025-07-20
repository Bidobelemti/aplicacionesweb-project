from django.urls import path
from .views import OrderListView, api_info
urlpatterns = [
    path('', api_info, name='api_info'),  # GET /api/users/
    path('orders/', OrderListView.as_view(), name='order-list'),

]