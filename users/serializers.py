from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import CustomUser, Device


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'password', 'picture', 'login_erro', 'is_logged_in', 'nv_user', 'is_active']

    password = serializers.CharField(write_only=True, required=True)
    id = serializers.UUIDField(read_only=True)
    nv_user = serializers.IntegerField(write_only=True, required=False)

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
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.nv_user = validated_data.get('nv_user', instance.nv_user)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        password = validated_data.get('password')
        if password:
            instance.password = make_password(password)

        instance.save()

        return instance
    
    def validate(self, attrs):
        if attrs.get('first_name') == attrs.get('last_name') and attrs.get('first_name') != None and attrs.get('last_name') != None:
            raise serializers.ValidationError({
                "error": ["First_name and last_name do not equal"],
            })
        if attrs.get('nv_user') is not None:
            if attrs.get('nv_user') > 3 or attrs.get('nv_user') < 0 or type(attrs.get('nv_user')) != int:
                raise serializers.ValidationError({
                    "error": ["Nv_user has an invalid value"]
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