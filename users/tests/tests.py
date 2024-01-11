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
    
    def test_register_success(self):
        registration_data = self.user

        response = self.client.post('/api/users/register/', registration_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='johndoe@example.com').exists())
        self.assertIn('user_id', response.data)
        self.assertIn('Register', response.data)
        self.assertEqual(response.data['Register'], 'johndoe@example.com')

    def test_login_sucess(self):
        registration_data = self.user

        response = self.client.post('/api/users/register/', registration_data)

        login = {
            'email': 'johndoe@example.com',
            'password': '123456789'
        }

        response = self.client.post('/api/users/login/', login)

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

        login = {
            'email': 'johndoe@example.com',
            'password': '12345678'
        }

        response = self.client.post('/api/users/login/', login)
        user = CustomUser.objects.filter(email='johndoe@example.com')[0]
        print(user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'],'Incorrect password or email. Three login errors lead to account lockout')
        self.assertEqual(user.login_erro,1)



