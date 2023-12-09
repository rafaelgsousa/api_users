from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['POST'])
def sign_up(request):
    return Response(
        {
            'Register'
        }
    )

@api_view(['POST'])
def sign_in(request):
    return Response(
        {
            'Login'
        }
    )

@api_view(['PATCH'])
def logout(request):
    return Response(
        {
            'logout'
        }
    )

@api_view(['PATCH'])
def change_password(request):
    return Response(
        {
            'change password'
        }
    )

@api_view(['GET'])
def get_user(request):
    return Response(
        {
            'get user'
        }
    )

@api_view(['GET'])
def get_users(request):
    return Response(
        {
            'get users'
        }
    )

@api_view(['PATCH'])
def update_user(request):
    return Response(
        {
            'update user'
        }
    )

@api_view(['PATCH'])
def inactive_user(request):
    return Response(
        {
            'inactive user'
        }
    )

@api_view(['DELETE'])
def delete_user(request):
    return Response(
        {
            'delete_user'
        }
    )