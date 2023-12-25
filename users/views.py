from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from utils import *

from .models import *
from .serializers import *


@csrf_exempt
@api_view(http_method_names=['POST'])
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

    user = get_object_or_404(CustomUser,email=email)
    
    user_serialize = UserSerializer(instance=user)
    if user_serialize.data['login_erro'] >= 3:
        return Response(
            {
                'error': 'Account blocked due to excessive login errors. Contact an administrator.'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user.is_active:
        return Response(
            {
                'error': 'User is inactive'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    if check_password(password, user.password):
        token = RefreshToken.for_user(user)

        user.is_logged_in = True
        user.save()
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
    
    user = get_object_or_404(CustomUser, id=id)

    user.is_logged_in = False

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
def change_password_by_settings(request):
    token = request.auth
    user_id = token['user_id']
    return Response(
        {
            'change password'
        }
    )

@csrf_exempt
@api_view(http_method_names=['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password_by_login_page(request):
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
        user_req = get_object_or_404(CustomUser, id=user_id)

        response = check_level(user_req, 1)

        if response:
            return response
        
        response = check_logged_in(user_req)

        if response:
            return response
    
    user = get_object_or_404(CustomUser, id=id)

    response = check_logged_in(user)

    if response:
        return response
    
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

    response = check_level(user, 1)

    if response:
        return response
    
    response = check_logged_in(user)

    if response:
        return response
    
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
    print(f'Request data {request.data} ')
    token = request.auth
    user_id = token['user_id']

    if str(id) != user_id:
        return Response(
            {
                'error': 'Unauthorized',
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user = get_object_or_404(CustomUser,id=id)

    response = check_logged_in(user)

    if response:
        return response
    
    result = UserSerializer(
        instance=user,
        data=request.data,
        partial=True
    )
    result.is_valid(raise_exception=True)
    result.save()    
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
        user_req = get_object_or_404(CustomUser, id=user_id)

        response = check_level(user_req, 1)

        if response:
            return response
        
        response = check_logged_in(user_req)

        if response:
            return response
        
        user = get_object_or_404(CustomUser, id=id)

        user.is_active = False
        user.save()
        
        return Response(
            {
                'message': f'User {user.email} is inactive'
            },
            status=status.HTTP_200_OK
        )
    
    user = get_object_or_404(CustomUser, id=id)

    response = check_logged_in(user)

    if response:
        return response
    
    user.is_active = False
    user.save()
    
    return Response(
        {
            'message': f'User {user.email} is inactive'
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

    response = check_logged_in(user)

    if response:
        return response
    
    user.delete()
    
    return Response(
        {
            'message':'delete_user'
        },
        status=status.HTTP_204_NO_CONTENT
    )