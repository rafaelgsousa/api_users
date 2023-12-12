from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Device, User


class UserSerializer (serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=100)
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=100)
    picture = serializers.ImageField(required=False)

    def create(self, validated_data):
        # Crie um novo usuário com os dados validados
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            picture=validated_data.get('picture', None),
            password=make_password(validated_data['password']),  # Criptografa a senha
            nv_user=User.NivelUsuario.ZERO,  # Define o nível do usuário como ZERO por padrão
            is_logged_in=False,  # Define que o usuário não está logado por padrão
            login_erro=User.LoginError.ZERO,  # Define o erro de login como ZERO por padrão
        )
        
        return user
    def login(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

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

            return {'token': token.key}
        else:
            # Senha incorreta, incrementa o contador de erros de login
            user.login_erro += 1
            user.save()

            if user.login_erro >= 3:
                return {'error': 'Conta bloqueada por excesso de erros de login. Contate um administrador.'}
            else:
                return {'error': 'Password or email incorreto'}

class DeviceSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ('name', 'user')

    def create(self, validated_data):
        # Crie um novo usuário com os dados validados
        device = Device.objects.create(
            name=validated_data['name'],
            user=validated_data['user'],
        )
        
        return device
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance