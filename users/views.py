from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from .serializers import *


# Create your views here.
@csrf_exempt
@api_view(http_method_names=['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def register(request):
    body = request.data
    serializer = UserSerializer(data=body)

    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    
    return Response(
        {
            'user_id': str(user.id),
            'Register': user.email
        },
        status=status.HTTP_201_CREATED
    )

@csrf_exempt
@api_view(http_method_names=['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return Response(
            {
                'error': 'User not found'
            }
        )

    user_serialize = UserSerializer(user)
    print(user_serialize.data['login_erro'])
    if user_serialize.data['login_erro'] >= 3:
        return Response(
            {
                'error': 'Conta bloqueada por excesso de erros de login. Contate um administrador.'
            }
        )

    if check_password(password, user.password):
        # Senha correta, cria um token baseado no email e id
        token = RefreshToken.for_user(user)

        # Atualiza campos no banco de dados
        user.is_logged_in = True
        if user.login_erro > 0:
            user.login_erro = User.LoginError.ZERO
            user.save()

        return Response(
            {
                'token': {
                    'access': str(token.access_token),
                    'refresh': str(token), 
                },
                'user': UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )
    else:
        # Senha incorreta, incrementa o contador de erros de login
        user.login_erro += 1
        user.save()

        if user.login_erro >= 3:
            return Response(
                {
                    'error': 'Conta bloqueada por excesso de erros de login. Contate um administrador.'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            return Response(
                {
                    'error': 'Password or email incorreto'
                }
            )

@csrf_exempt
@api_view(http_method_names=['PATCH'])
def logout(request):
    return Response(
        {
            'logout'
        }
    )

@csrf_exempt
@api_view(http_method_names=['PATCH'])
def change_password(request):
    return Response(
        {
            'change password'
        }
    )

@csrf_exempt
@api_view(http_method_names=['GET'])
def get_user(request):
    return Response(
        {
            'get user'
        }
    )

@csrf_exempt
@api_view(http_method_names=['GET'])
def get_users(request):
    return Response(
        {
            'get users'
        }
    )

@csrf_exempt
@api_view(http_method_names=['PATCH'])
def update_user(request):
    return Response(
        {
            'update user'
        }
    )

@csrf_exempt
@api_view(http_method_names=['PATCH'])
def inactive_user(request):
    return Response(
        {
            'inactive user'
        }
    )

@csrf_exempt
@api_view(http_method_names=['DELETE'])
def delete_user(request):
    return Response(
        {
            'delete_user'
        }
    )