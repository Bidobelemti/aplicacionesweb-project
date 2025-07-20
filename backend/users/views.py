from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .models import Customer
from .serializers import RegisterSerializer, LoginSerializer


@api_view(['GET'])
def api_info(request):
    """Vista para mostrar información de la API en /api/users/"""
    return Response({
        'message': 'API de usuarios funcionando correctamente',
        'version': '1.0',
        'endpoints': {
            'info': '/api/users/ [GET]',
            'register': '/api/users/register/ [POST]',
            'login': '/api/users/login/ [POST]'
        }
    })


class RegisterView(APIView):
    """Vista para registrar nuevos usuarios"""
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user_id': user.id,
                'email': user.email,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Vista para iniciar sesión"""
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = Customer.objects.get(email=email)
                if user.check_password(password):
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({
                        'message': 'Inicio de sesión exitoso',
                        'user_id': user.id,
                        'email': user.email,
                        'token': token.key
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Contraseña incorrecta'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Customer.DoesNotExist:
                return Response({
                    'error': 'Usuario no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)