import os
import random

from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

load_dotenv()

from utils import *

from ..models import *
from ..serializers import *


class CodeBySettings(ModelViewSet):
    serializer_class = VerifCodeSerializer

    def create(self, request):
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
    
    def retrieve(self):
        sent_code = self.request.data.get('code', '')

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

    def destroy(self, request):
        token = request.auth
        user_id = token['user_id']

        user = get_object_or_404(CustomUser,id=user_id)
        
        result = UserSerializer(
            instance=user,
            data=self.request.data,
            partial=True
        )
        
        result.is_valid(raise_exception=True)

        result.save()

        code = get_object_or_404(VerificationCode, user=user.id)  
    
        code.delete()

        return Response(
            {
                'user': 'change password'
            },
            status=status.HTTP_200_OK
        )