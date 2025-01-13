from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.profile_url = reverse('profile')
        self.change_password_url = reverse('change_password')
        
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_login(self):
        # Create user first
        self.client.post(self.register_url, self.user_data)
        
        # Try logging in
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_profile_update(self):
        # Create and authenticate user
        self.client.post(self.register_url, self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        self.client.force_authenticate(user=user)

        # Update profile
        update_data = {
            'bio': 'New bio'
        }
        response = self.client.patch(self.profile_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'New bio')

    def test_change_password(self):
        # Create and authenticate user
        self.client.post(self.register_url, self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        self.client.force_authenticate(user=user)

        # Change password
        password_data = {
            'old_password': self.user_data['password'],
            'new_password': 'NewTestPass123!'
        }
        response = self.client.put(self.change_password_url, password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
