import os
import random

from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

load_dotenv()

from utils import *

from ..models import *
from ..serializers import *


class CustomUserListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page'


class CustomUserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    pagination_class = CustomUserListPagination

    def register(self, request):
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

            update = {"is_logged_in" : True}

            if user.login_erro > 0:
                update.login_erro = CustomUser.LoginError.ZERO

            result = UserSerializer(
                instance=user,
                data=update,
                partial=True
                )
            
            result.is_valid(raise_exception=True)
            user.save(update_fields=list(update.keys()))

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
            update = {"login_erro" : user.login_erro + 1}
            result = UserSerializer(
                instance=user,
                data=update,
                partial=True
                )
            
            result.is_valid(raise_exception=True)
            user.save(update_fields=list(update.keys()))

            if user.login_erro >= 3:
                raise PermissionDenied(detail='error: Account blocked due to excessive login errors. Contact an administrator.')
            else:
                return Response(
                    {
                        'error': 'Incorrect password or email. Three login errors lead to account lockout'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
    def send_verification_code_before_login(self, request, email=None):

        user = get_object_or_404(CustomUser, email=email)

        code = str(random.randint(100000, 999999))

        check = VerificationCode.objects.filter(user=user)

        check.delete()
        
        VerificationCode.objects.create(user=user, code=code)

        send_mail(
            subject='Link to Change Password',
            message='',
            from_email=f'{os.getenv("EMAIL_HOST_USER")}',
            recipient_list=[f'{user.email}'],
            fail_silently=False,
            html_message=f"""
                <h1>Verification Code</h1>
                <br>
                <br>
                <p>Code: <b>{code}</b> </p>
            """
        )

        return Response(
            {
                'message': 'Code sent successfully.'
            }, 
            status=status.HTTP_200_OK
        )

    def verify_code_before_login(self, request):
        sent_code = request.data.get('code', '')

        code_req = get_object_or_404(VerificationCode,code=sent_code)

        if (timezone.now() - code_req.created_at).total_seconds() > 60:
            raise ValidationError({'detail': 'The code has expired. Submit a new code.'})
        
        result = VerifCodeSerializer(
                    instance=code_req,
                    data={'code_verificated':True},
                    partial=True
                )

        result.is_valid(raise_exception=True)

        result.save()

        return Response(
                    {
                        'message': 'Code verified successfully.'
                    },
                    status=status.HTTP_200_OK
                )


    def change_password_before_login(self, request, email):

        user = get_object_or_404(CustomUser, email=email)
        
        code_db = get_object_or_404(VerificationCode,user=user.id)

        if not code_db.code_verificated:
            raise PermissionDenied(detail='error: No authorization for this procedure.')

        result = UserSerializer(
                                instance=user,
                                data=request.data,
                                partial=True
                            )
        result.is_valid(raise_exception=True)

        result.save()

        code_db.delete()

        return Response(
            {
                'message' : 'Change password'
            }
        )