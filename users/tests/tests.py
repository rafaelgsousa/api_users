import json

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import CustomUser


class TestRegisterView(APITestCase):
    user = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'phone': '86911111111',
            'password': 'Ca123456789'
        }
    
    user_field_already_used = {
            'first_name': 'Mary',
            'last_name': 'Doe',
            'email': 'marydoe@example.com',
            'phone': '86911111111',
            'password': 'Ca123456789'
        }
    
    bad_user = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'phone': '86911111111',
        }
    
    login = {
            'email': 'johndoe@example.com',
            'password': 'Ca123456789'
        }
    
    bad_login = {
            'email': 'johndoe@example.com',
            'password': 'Ca12345678'
        }
    
    update = {
        'first_name': 'John Update'
    }

    bad_update = {
        'is_logged_in': False
    }

    bad_update_password = {
        'password': '987654321'
    }
    
    def test_register_success(self):
        registration_data = self.user

        response = self.client.post('/api/users/', registration_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email=registration_data['email']).exists())
        self.assertIn('id', response.data)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], registration_data['email'])

    def test_register_bad_request_without_password_field(self):
        registration_data = self.bad_user

        response = self.client.post('/api/users/', registration_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(not CustomUser.objects.filter(email=registration_data['email']).exists())
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'], ['This field is required.'])

    def test_register_bad_request_phone_field_already_used(self):
        registration_data = self.user
        second_registration_data = self.user_field_already_used

        self.client.post('/api/users/', registration_data)
        response = self.client.post('/api/users/', second_registration_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(not CustomUser.objects.filter(email=second_registration_data['email']).exists())
        self.assertIn('phone', response.data)
        self.assertEqual(response.data['phone'], ['custom user with this phone already exists.'])

    def test_login_sucess(self):
        registration_data = self.user

        self.client.post('/api/users/', registration_data)

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

        response = self.client.post('/api/users/', registration_data)

        response = self.client.post('/api/users/login/', self.bad_login)
        user = CustomUser.objects.filter(email=registration_data['email'])[0]

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'],'Incorrect password or email. Three login errors lead to account lockout')
        self.assertEqual(user.login_erro,1)

    def test_login_with_incorrect_password_three_times(self):
        registration_data = self.user

        response = self.client.post('/api/users/', registration_data)
        self.client.post('/api/users/login/', self.bad_login)
        self.client.post('/api/users/login/', self.bad_login)
        response = self.client.post('/api/users/login/', self.bad_login)
        user = CustomUser.objects.filter(email=registration_data['email'])[0]

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'],'error: Account blocked due to excessive login errors. Contact an administrator.')
        self.assertEqual(user.login_erro,3)

    def test_get_data_user_with_token_jwt_status_200(self):
        registration_data = self.user

        self.client.post('/api/users/', registration_data)

        response_login = self.client.post('/api/users/login/', self.login)
        
        token = response_login.data['token']['access']
        id = response_login.data['user']['id']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(f'/api/users/{id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], registration_data['email'])
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('is_logged_in', response.data)
        self.assertEqual(response.data['login_erro'], 0)

    def test_get_data_user_without_token_jwt_status_401(self):
        registration_data = self.user

        self.client.post('/api/users/', registration_data)

        response_login = self.client.post('/api/users/login/', self.login)
        
        id = response_login.data['user']['id']
        
        response = self.client.get(f'/api/users/{id}/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_logout_user_with_token_jwt_status_200(self):
        registration_data = self.user

        self.client.post('/api/users/', registration_data)

        response_login = self.client.post('/api/users/login/', self.login)

        token = response_login.data['token']['access']
        id = response_login.data['user']['id']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post(f'/api/users/logout/')
        user = CustomUser.objects.filter(email=registration_data['email'])[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['user'], registration_data['email'])
        self.assertEqual(response.data['message'], 'logout')
        self.assertEqual(user.is_logged_in, False)

    def test_lgogout_user_without_token_jwt_status_401(self):
        registration_data = self.user

        self.client.post('/api/users/', registration_data)

        response_login = self.client.post('/api/users/login/', self.login)

        id = response_login.data['user']['id']
    
        response = self.client.patch(f'/api/users/logout/{id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = json.loads(response.content)
        self.assertIn('error', response)
        self.assertEqual(response['error'], 'Request body cannot be None.')

    def test_update_user_status_200(self):
        registration_data = self.user

        self.client.post('/api/users/', registration_data)

        response_login = self.client.post('/api/users/login/', self.login)

        token = response_login.data['token']['access']
        id = response_login.data['user']['id']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.patch(f'/api/users/{id}/', self.update)
        user = CustomUser.objects.filter(email=registration_data['email'])[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], registration_data['email'])
        self.assertEqual(response.data['first_name'], self.update['first_name'])
        self.assertEqual(user.is_logged_in, True)
    
    def test_update_user_with_unauthorized_request_status_401(self):
        registration_data = self.user

        self.client.post('/api/users/', registration_data)

        response_login = self.client.post('/api/users/login/', self.login)

        token = response_login.data['token']['access']
        id = response_login.data['user']['id']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.patch(f'/api/users/{id}/', self.bad_update)
        user = CustomUser.objects.filter(email=registration_data['email'])[0]

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = json.loads(response.content)
        self.assertIn('error', response)
        self.assertEqual(response['error'], 'No authorization for this procedure.')
        self.assertEqual(user.is_logged_in, True)

    def test_update_password_without_sending_code_and_verification_status_401(self):
        registration_data = self.user

        self.client.post('/api/users/', registration_data)

        response_login = self.client.post('/api/users/login/', self.login)

        token = response_login.data['token']['access']
        id = response_login.data['user']['id']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.patch(f'/api/users/{id}/', self.bad_update_password)

        user = CustomUser.objects.filter(email=registration_data['email'])[0]

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = json.loads(response.content)
        self.assertIn('error', response)
        self.assertEqual(response['error'], 'No authorization for this procedure.')
        self.assertEqual(self.login['password'], registration_data['password'])