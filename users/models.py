from uuid import uuid4

from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

class User(models.Model):
    class NivelUsuario(models.IntegerChoices):
        ZERO = 0, 'Zero'
        UM = 1, 'Um'
        DOIS = 2, 'Dois'

    class LoginError(models.IntegerChoices):
        ZERO = 0, 'Zero'
        UM = 1, 'Um'
        DOIS = 2, 'Dois'
        TRES = 3, 'Tres'
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    picture = models.ImageField(upload_to='pictures/%Y/%m/%d', blank=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    nv_user = models.IntegerField(choices=NivelUsuario.choices, default=NivelUsuario.ZERO)
    is_logged_in = models.BooleanField(default=False)
    login_erro = models.IntegerField(choices=LoginError.choices, default=LoginError.ZERO)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
