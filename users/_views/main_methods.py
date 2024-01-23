from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.utils import timezone
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

load_dotenv()

from utils import *

from ..models import *
from ..serializers import *


class CustomUserListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page'

class CustomUserView(ModelViewSet):
    queryset = CustomUser.objects.filter()
    serializer_class = UserSerializer
    pagination_class = CustomUserListPagination
    http_method_names = ['get', 'options', 'head', 'patch', 'post', 'delete']
    
    def get_object(self):
        pk = self.kwargs.get('pk','')
        qs = CustomUser.objects.get(pk=pk)
        return qs
    
    def login(self, request):
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
            user.save(update_fields=list(['is_logged_in']))

            if user.login_erro > 0:
                user.login_erro = CustomUser.LoginError.ZERO
                user.save(update_fields=list(['login_erro']))

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
            user.save(update_fields=list(['login_erro']))

            if user.login_erro >= 3:
                raise PermissionDenied(detail='error: Account blocked due to excessive login errors. Contact an administrator.')
            else:
                return Response(
                    {
                        'error': 'Incorrect password or email. Three login errors lead to account lockout'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

    def logout(request, id):
        token = request.auth
        user_id = token['user_id']

        if str(id) != user_id:
            raise PermissionDenied(detail='error: No authorization for this procedure.')
        
        user = get_object_or_404(CustomUser, id=id)

        user.is_logged_in= False
        user.last_login_sistem= timezone.now()
            
        user.save(update_fields=list(['is_logged_in', 'last_login_sistem']))

        return Response(
            {
                'user': user.email,
                'message': 'logout'
            },
            status=status.HTTP_200_OK
        )
