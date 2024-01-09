from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import serializers

from .models import CustomUser, Device, VerificationCode


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'password', 'picture', 'login_erro', 'is_logged_in', 'nv_user', 'is_active', 'update_at']

    password = serializers.CharField(write_only=True, required=True)
    id = serializers.UUIDField(read_only=True)
    nv_user = serializers.IntegerField(write_only=True, required=False)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            picture=validated_data.get('picture', None),
            password=make_password(validated_data['password']),
            nv_user=CustomUser.NivelUsuario.ZERO,
            is_logged_in=False,
            login_erro=CustomUser.LoginError.ZERO,
        )
        
        return user
    
    def update(self, instance, validated_data):
        fields_to_update_at = ['first_name', 'last_name', 'email', 'phone', 'password', 'picture', 'nv_user', 'is_active']

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

        for field in fields_to_update_at:
            update_at = False
            value = validated_data.get(field)
            print(f'Value of {field}')
            print(value)
            if value is not None:
                print('Update = True')
                update_at = True
            if update_at:
                instance.update_at = timezone.now()
        
        try:
            instance.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error saving changes: {e}")

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

class VerifCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ['user', 'code', 'created_at', 'code_verificated']

    def create(self, validated_data):
        user = VerificationCode.objects.create(
            user = validated_data['email'],
            code = validated_data['first_name'],
            created_at = validated_data['last_name'],
            code_verificated = validated_data['email'],
        )

        return user

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)

        created_at_str = validated_data.get('created_at')
        if created_at_str:
            instance.created_at = parse_datetime(created_at_str)

        code_verificated = validated_data.get('code_verificated', instance.code_verificated)
        instance.code_verificated = bool(code_verificated)

        user_email = validated_data.get('user', instance.user.email)
        user = CustomUser.objects.get(email=user_email)

        if user:
            instance.user = user
        
        instance.save()
        
        return instance