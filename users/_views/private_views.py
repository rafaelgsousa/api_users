import os
import random

from django.core.mail import send_mail
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

load_dotenv()

from utils import *

from ..models import *
from ..serializers import *


class CustomUserListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page'


class CustomUserViewSetsAuth(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = CustomUserListPagination

    def get_queryset(self):
        token = self.request.auth
        user_id = token['user_id']
        user = get_object_or_404(CustomUser, id=user_id)

        check_level(user, 1)

        return CustomUser.objects.all().order_by('-id')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Apply pagination to the result set
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'users': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'users': serializer.data})
    
    def logout(self, request, id):
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
    
    def send_verification_code_by_settings(request):
        token = request.auth
        user_id = token['user_id']

        user = get_object_or_404(CustomUser, id=user_id)

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

    def verify_code_by_settings(request):
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
                        'detail': 'Code verified successfully.'
                    },
                    status=status.HTTP_200_OK
                )

    def change_password_by_settings(request):
        token = request.auth
        user_id = token['user_id']

        user = get_object_or_404(CustomUser,id=user_id)
        
        code = get_object_or_404(VerificationCode, user=user.id)

        if not code.code_verificated:
            raise PermissionDenied(detail='error: No authorization for this procedure.')
        

        result = UserSerializer(
            instance=user,
            data=request.data,
            partial=True
        )
        
        result.is_valid(raise_exception=True)

        result.save()

        code.delete()

        return Response(
            {
                'user': 'change password'
            },
            status=status.HTTP_200_OK
        )

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

    def update_user(request, id):
        if not request.data:
            raise ValidationError({'detail': 'request without body.'})
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