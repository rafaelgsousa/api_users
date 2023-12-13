from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Device, User


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'picture', 'login_erro', 'is_logged_in']
        # fields = '__all__'

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
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
class DeviceSerializer (serializers.ModelSerializer):
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