from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
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
from .utils import *


# Create your views here.
@csrf_exempt
@api_view(http_method_names=['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def register(request):
    token = request.auth
    user_id = token['user_id']
    user = get_object_or_404(CustomUser,id=user_id)

    if not user.is_logged_in:
        return Response(
            {
            'error': 'User no logged'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

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

    user = get_object_or_404(CustomUser,email=email)
    
    user_serialize = UserSerializer(instance=user)
    if user_serialize.data['login_erro'] >= 3:
        return Response(
            {
                'error': 'Account blocked due to excessive login errors. Contact an administrator.'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    if check_password(password, user.password):
        # Senha correta, cria um token baseado no email e id
        token = RefreshToken.for_user(user)

        # Atualiza campos no banco de dados
        user.is_logged_in = True
        print(user.is_logged_in)
        if user.login_erro > 0:
            user.login_erro = CustomUser.LoginError.ZERO
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
                    'error': 'Account blocked due to excessive login errors. Contact an administrator.'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            return Response(
                {
                    'error': 'Incorrect password or email. Three login errors lead to account lockout'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

@csrf_exempt
@api_view(http_method_names=['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout(request, id):
    token = request.auth
    user_id = token['user_id']

    if str(id) != user_id:
        return Response(
                {
                    'error': 'No authorization for this procedure.'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    user = get_object_or_404(CustomUser, id=user_id)

    user.is_logged_id = False

    user.save()

    return Response(
        {
            'user': user.email,
            'message': 'logout'
        },
        status=status.HTTP_200_OK
    )

@csrf_exempt
@api_view(http_method_names=['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    token = request.auth
    user_id = token['user_id']
    return Response(
        {
            'change password'
        }
    )

@csrf_exempt
@api_view(http_method_names=['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    token = request.auth
    user_id = token['user_id']

    if str(id) != user_id:
        return Response(
            {
                'error': 'Unauthorized',
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user = get_object_or_404(CustomUser, id=id)

    if not user.is_logged_in:
        return Response(
            {
            'error': 'User no logged'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user_ser = UserSerializer(user)

    return Response(
        {
            'user': user_ser.data,
        },
        status=status.HTTP_200_OK
    )

@csrf_exempt
@api_view(http_method_names=['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_users(request):
    token = request.auth
    user_id = token['user_id']
    user = get_object_or_404(CustomUser,id=user_id)

    if not user:
        return Response(
            {
                'error': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if not user.is_logged_in:
        return Response(
            {
            'error': 'User no logged'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    users = CustomUser.objects.all().order_by('-id')

    users_ser = UserSerializer(instance=users, many=True)

    return Response(
        {
            'users': users_ser.data
        }
    )

@csrf_exempt
@api_view(http_method_names=['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, id):
    token = request.auth
    user_id = token['user_id']

    if str(id) != user_id:
        return Response(
            {
                'error': 'Unauthorized',
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user = get_object_or_404(CustomUser,id=user_id)

    if not user.is_logged_in:
        return Response(
            {
            'error': 'User no logged'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    result = UserSerializer(
        instance=user,
        data=request.data,
        partial=True
    )
    
    return Response(
        {
            'user': result.data
        },
        status=status.HTTP_200_OK
    )

@csrf_exempt
@api_view(http_method_names=['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def inactive_user(request, id):
    token = request.auth
    user_id = token['user_id']

    if str(id) != user_id:
        return Response(
            {
                'error': 'Unauthorized',
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user = get_object_or_404(CustomUser, id=id)

    if not user.is_logged_in:
        return Response(
            {
            'error': 'User no logged'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )     
    
    result = UserSerializer(
        instance=user,
        data=request.data,
        partial=True
    )
    
    return Response(
        {
            'user': result.data
        },
        status=status.HTTP_200_OK
    )

@csrf_exempt
@api_view(http_method_names=['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, id):
    token = request.auth
    user_id = token['user_id']

    if str(id) != user_id:
        return Response(
            {
                'error': 'Unauthorized',
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user = get_object_or_404(CustomUser, id=id)

    if not user.is_logged_in:
        return Response(
            {
            'error': 'User no logged'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    return Response(
        {
            'delete_user'
        },
        status=status.HTTP_204_NO_CONTENT
    )