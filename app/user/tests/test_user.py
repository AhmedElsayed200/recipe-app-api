"""
test user api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')
MY_PROFILE_URL = reverse('user:myprofile')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ test public features of user API """
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """ test sucess creation of users """

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_create_user_already_exist_failure(self):
        """ test failure creation if user already exist """

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_user_with_short_password_failure(self):
        """ test failure creation if password is short """

        payload = {
            'email': 'test@example.com',
            'password': '123',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        not_exist = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(not_exist)

    def test_create_token_success(self):
        """ test success of token creation """
        user_data = {
            'email': 'test@example.com',
            'password': 'pass123',
            'name': 'Test Name'
        }
        create_user(**user_data)

        payload = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_with_wrong_password(self):
        """ test failure of token creation with wrong password """
        user_data = {
            'email': 'test@example.com',
            'password': 'pass123',
            'name': 'Test Name'
        }
        create_user(**user_data)

        payload = {
            'email': user_data['email'],
            'password': 'wrongpass123'
        }
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertNotIn('token', res)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_empty_password(self):
        """ test failure of token creation with empty password """
        user_data = {
            'email': 'test@example.com',
            'password': 'pass123',
            'name': 'Test Name'
        }
        create_user(**user_data)

        payload = {
            'email': user_data['email'],
            'password': ''
        }
        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertNotIn('token', res)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_failure_access_to_my_profile_unauth(self):
        """ test failure access to my profile page if I am not auth (no token) """
        res = self.client.get(MY_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ test apis for private user (with token) """

    def setUp(self):
        self.payload = {
            'email': 'test@example.com',
            'password': 'testpass',
            'name': 'Test Name'
        }
        self.client = APIClient()
        self.user = create_user(**self.payload)
        self.client.force_authenticate(user=self.user)
    
    def test_access_my_profile_success(self):
        res = self.client.get(MY_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })
    
    def test_failure_post_to_my_profile(self):
        res = self.client.post(MY_PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_my_profile(self):
        newdata = {
            'name': 'new name',
            'password': 'newpassword123'
        }

        res = self.client.patch(MY_PROFILE_URL, newdata)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, newdata['name'])
        self.assertTrue(self.user.check_password(newdata['password']))
