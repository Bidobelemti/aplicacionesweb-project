from django.urls import path
from .views import RegisterView, LoginView, api_info

urlpatterns = [
    path('', api_info, name='api_info'),  # GET /api/users/
    path('register/', RegisterView.as_view(), name='register'),  # POST /api/users/register/
    path('login/', LoginView.as_view(), name='login'),  # POST /api/users/login/
]