from rest_framework import status
from rest_framework.test import APITestCase

from ..models import CustomUser


class TestRegisterView(APITestCase):
    user = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'phone': '86911111111',
            'password': '123456789'
        }
    
    user_field_already_used = {
            'first_name': 'Mary',
            'last_name': 'Doe',
            'email': 'marydoe@example.com',
            'phone': '86911111111',
            'password': '123456789'
        }
    
    bad_user = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'phone': '86911111111',
        }
    
    login = {
            'email': 'johndoe@example.com',
            'password': '123456789'
        }
    
    bad_login = {
            'email': 'johndoe@example.com',
            'password': '12345678'
        }
    
    def test_register_success(self):
        registration_data = self.user

        response = self.client.post('/api/users/register/', registration_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email=registration_data['email']).exists())
        self.assertIn('user_id', response.data)
        self.assertIn('Register', response.data)
        self.assertEqual(response.data['Register'], registration_data['email'])

    def test_register_bad_request_without_password_field(self):
        registration_data = self.bad_user

        response = self.client.post('/api/users/register/', registration_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(not CustomUser.objects.filter(email=registration_data['email']).exists())
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'], ['This field is required.'])

    def test_register_bad_request_phone_field_already_used(self):
        registration_data = self.user
        second_registration_data = self.user_field_already_used

        self.client.post('/api/users/register/', registration_data)
        response = self.client.post('/api/users/register/', second_registration_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(not CustomUser.objects.filter(email=second_registration_data['email']).exists())
        self.assertIn('phone', response.data)
        self.assertEqual(response.data['phone'], ['custom user with this phone already exists.'])

    def test_login_sucess(self):
        registration_data = self.user

        self.client.post('/api/users/register/', registration_data)

        response = self.client.post('/api/users/login/', self.login)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('access', response.data['token'])
        self.assertIn('refresh', response.data['token'])
        self.assertIn('user', response.data)
        self.assertIn('email', response.data['user'])
        self.assertEqual(response.data['user']['email'], 'johndoe@example.com')
        self.assertIn('first_name', response.data['user'])
        self.assertIn('last_name', response.data['user'])
        self.assertIn('is_logged_in', response.data['user'])
        self.assertEqual(response.data['user']['is_logged_in'], True)

    def test_login_bad_password_status_400_bad_request(self):
        registration_data = self.user

        response = self.client.post('/api/users/register/', registration_data)

        response = self.client.post('/api/users/login/', self.bad_login)
        user = CustomUser.objects.filter(email='johndoe@example.com')[0]

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'],'Incorrect password or email. Three login errors lead to account lockout')
        self.assertEqual(user.login_erro,1)

    def test_get_data_user_with_token_jwt_status_200(self):
        registration_data = self.user

        self.client.post('/api/users/register/', registration_data)

        response_login = self.client.post('/api/users/login/', self.login)

        token = response_login.data['token']['access']
        id = response_login.data['user']['id']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(f'/api/users/{id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('email', response.data['user'])
        self.assertEqual(response.data['user']['email'], registration_data['email'])
        self.assertIn('first_name', response.data['user'])
        self.assertIn('last_name', response.data['user'])
        self.assertIn('is_logged_in', response.data['user'])
        self.assertEqual(response.data['user']['login_erro'], 0)

    def test_get_data_user_without_token_jwt_status_401(self):
        registration_data = self.user

        self.client.post('/api/users/register/', registration_data)

        response_login = self.client.post('/api/users/login/', self.login)

        id = response_login.data['user']['id']
    
        response = self.client.get(f'/api/users/{id}/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

