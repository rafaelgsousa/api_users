from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


# Create your views here.
@api_view(http_method_names=['POST'])
def sign_up(request):
    print(request.data)
    if request.data == {}:
        return Response(
            {
                'error': 'Please provide email/password'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create(
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            email=request.data['email'],
            phone=request.data['phone'],
            picture=request.data.get('picture', None),
            password=make_password(request.data['password']),  # Criptografa a senha
        )
    serializer = UserSerializer(user)
    
    return Response(
        {
            'Register': serializer.data
        },
        status=status.HTTP_201_CREATED
    )

@api_view()
def sign_in(request):
    email = request.data['email']
    password = request.data['password']

    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return {'error': 'User not found'}

    if user.login_erro >= 3:
        return {'error': 'Conta bloqueada por excesso de erros de login. Contate um administrador.'}

    if check_password(password, user.password):
        # Senha correta, cria um token baseado no email e id
        token, created = Token.objects.get_or_create(user=user)

        # Atualiza campos no banco de dados
        user.is_logged_in = True
        user.login_erro = User.LoginError.ZERO
        user.save()

        return Response(
            {
                'token': token.key,
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
            return {'error': 'Password or email incorreto'}

@api_view()
def logout(request):
    return Response(
        {
            'logout'
        }
    )

@api_view()
def change_password(request):
    return Response(
        {
            'change password'
        }
    )

@api_view()
def get_user(request):
    return Response(
        {
            'get user'
        }
    )

@api_view()
def get_users(request):
    return Response(
        {
            'get users'
        }
    )

@api_view()
def update_user(request):
    return Response(
        {
            'update user'
        }
    )

@api_view()
def inactive_user(request):
    return Response(
        {
            'inactive user'
        }
    )

@api_view()
def delete_user(request):
    return Response(
        {
            'delete_user'
        }
    )