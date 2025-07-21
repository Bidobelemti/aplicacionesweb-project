from django.urls import path
from . import views
urlpatterns = [
    path('', views.api_info, name='api_info'),  # GET /api/users/
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('create/', views.create_order_with_items, name='create-order-with-items'),
    path('orders/<str:order_type>/<int:order_id>/status/', views.update_order_status, name='update-order-status'),
    path('menu/', views.MenuItemListCreateView.as_view(), name='menu-item-list-create'), # GET/POST /api/orders/menu/

    
    # URLs para pedidos en mesa
    path('eatin/', views.EatInOrderListCreateView.as_view(), name='eatin-order-list'),
    path('eatin/<int:pk>/', views.EatInOrderDetailView.as_view(), name='eatin-order-detail'),
    
    # URLs para pedidos para llevar
    path('takeaway/', views.TakeAwayOrderListCreateView.as_view(), name='takeaway-order-list'),
    path('takeaway/<int:pk>/', views.TakeAwayOrderDetailView.as_view(), name='takeaway-order-detail'),
    
    # URLs para pedidos con envío
    path('shipping/', views.ShippingOrderListCreateView.as_view(), name='shipping-order-list'),
    path('shipping/<int:pk>/', views.ShippingOrderDetailView.as_view(), name='shipping-order-detail'),
    
]