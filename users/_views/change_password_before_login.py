import os
import random

from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
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


class CodeBeforeLogin(ModelViewSet):
    serializer_class = VerifCodeSerializer
    http_method_names = ['get', 'options', 'head', 'post', 'delete']

    def create(self, request):
        user = get_object_or_404(CustomUser, email=request.get('email',''))

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
                        'message': 'Code verified successfully.'
                    },
                    status=status.HTTP_200_OK
                )

    def destroy(self, request):
        user = get_object_or_404(CustomUser, email=self.request.get('email',''))

        result = UserSerializer(
                                instance=user,
                                data=request.data,
                                partial=True
                            )
        result.is_valid(raise_exception=True)

        result.save()
        
        code_db = get_object_or_404(VerificationCode,user=user.id)

        code_db.delete()

        return Response(
            {
                'message' : 'Change password'
            }
        )