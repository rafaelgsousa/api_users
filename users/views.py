import random

from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.exceptions import PermissionDenied
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
        raise PermissionDenied(detail='error: Account blocked due to excessive login errors. Contact an administrator.')
    if not user.is_active:
        raise PermissionDenied(detail='error: User is inactive.')

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
            raise PermissionDenied(detail='error: Account blocked due to excessive login errors. Contact an administrator.')
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
        raise PermissionDenied(detail='error: No authorization for this procedure.')
    
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
@api_view(http_method_names=['POST'])
def forget_password_send_email(request, email):
    print(request.data)
    print(f'email : {email}')
    user = get_object_or_404(CustomUser, email=email)
    print(user)
    send_mail(
            'Reset Password',
            f'Acesse esse link: example.com.br para começar a mudar seu password',
            'rafaeldevtesting@gmail.com',
            [user.email],
            fail_silently=False,
        )

    return Response(
        {
            'message' : 'send email'
        },
        status=status.HTTP_200_OK
    )

@csrf_exempt
@api_view(http_method_names=['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password_by_settings(request, id):
    token = request.auth
    user_id = token['user_id']

    if str(id) != user_id:
        raise PermissionDenied(detail='error: No authorization for this procedure.')
    
    code = get_object_or_404(VerificationCode, id=id)

    if not code.code_verificated:
        raise PermissionDenied(detail='error: Code without verification.')
    
    user = get_object_or_404(CustomUser,id=id)
    result = UserSerializer(
        instance=user,
        data=request.data,
        partial=True
    )
    result.is_valid(raise_exception=True)
    result.save()    
    return Response(
        {
            'user': 'change password'
        },
        status=status.HTTP_200_OK
    )

@csrf_exempt
@api_view(http_method_names=['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password_by_login_page(request, email):
    token = request.auth
    user_id = token['user_id']
    return Response(
        {
            'message' : 'change password'
        }
    )

@csrf_exempt
@api_view(http_method_names=['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def send_verification_code(request):
    user = request.user
    if user.is_authenticated:
        code = str(random.randint(100000, 999999))
        VerificationCode.objects.create(user=user, code=code)
            
        # Envie o código por e-mail
        send_mail(
            'Código de Verificação',
            f'Seu código de verificação é: {code}',
            'rafaeldevtesting@gmail.com',
            [user.email],
            fail_silently=False,
        )
            
        return Response(
            {
                'detail': 'Código enviado com sucesso.'
            }, 
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {
                'detail': 'Usuário não autenticado.'
            }, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@csrf_exempt
@api_view(http_method_names=['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verify_code(request):
    user = request.user
    code = request.data.get('code', None)
        
    if user.is_authenticated and code:
        # Verifique se o código está correto
        if VerificationCode.objects.filter(user=user, code=code).exists():
            # Lógica para permitir a alteração da senha
            return Response(
                {
                    'detail': 'Código verificado com sucesso.'
                }, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'detail': 'Código inválido.'
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                'detail': 'Usuário não autenticado ou código ausente.'
            }, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@csrf_exempt
@api_view(http_method_names=['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    token = request.auth
    user_id = token['user_id']
    user_req = get_object_or_404(CustomUser, id=user_id)
    user = get_object_or_404(CustomUser, id=id)

    if str(id) != user_id:
        check_level(user_req, 1)
    
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

    check_level(user, 1)
    
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
    user_req = get_object_or_404(CustomUser,id=user_id)
    user = get_object_or_404(CustomUser,id=id)

    check_update_is_logged_in(request.data)

    if str(id) != user_id:
        check_level_to_update_nv_user(request.data, user_req, user)

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
@api_view(http_method_names=['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, id):
    token = request.auth
    user_id = token['user_id']
    user = get_object_or_404(CustomUser, id=id)
    user_req = get_object_or_404(CustomUser,id=user_id)

    if str(id) != user_id:

        if user_req.nv_user >= 2:
            check_levels(user_req, user)
    
    user.delete()
    
    return Response(
        {
            'message':'delete_user'
        },
        status=status.HTTP_204_NO_CONTENT
    )