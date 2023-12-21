from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import CustomUser, Device


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'password', 'picture', 'login_erro', 'is_logged_in']

    password = serializers.CharField(write_only=True, required=True)
    id = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        # Crie um novo usuário com os dados validados
        user = CustomUser.objects.create(
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            picture=validated_data.get('picture', None),
            password=make_password(validated_data['password']),  # Criptografa a senha
            nv_user=CustomUser.NivelUsuario.ZERO,  # Define o nível do usuário como ZERO por padrão
            is_logged_in=False,  # Define que o usuário não está logado por padrão
            login_erro=CustomUser.LoginError.ZERO,  # Define o erro de login como ZERO por padrão
        )
        
        return user
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def validate(self, attrs):
        if attrs.get('first_name') == attrs.get('last_name'):
            raise serializers.ValidationError({
                "error": ["First_name and last_name do not equal"],
            })
        return super().validate(attrs)
    
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