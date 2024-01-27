import os
import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

load_dotenv()

from utils import *

from ..models import *
from ..serializers import *


class RescuePasswordViewSet(ModelViewSet):
    serializer_class = VerifCodeSerializer
    http_method_names = ['options', 'head', 'post', 'patch', 'delete']
    lookup_field = 'email'

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, email=request.data.get('email', None))

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
    
    def partial_update(self, request, *args, **kwargs):
        try:
            sent_code = request.data.get('code', None)

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
        except ValidationError as e:
            return Response(
                dict(e),
                status=status.HTTP_408_REQUEST_TIMEOUT
            )
    

    @action(detail=False, methods=['delete'])
    def change_password(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, email=self.kwargs.get('email',None))

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