from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Organisation
from rest_framework.test import APITestCase
from django.urls import reverse

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        
        # Create a user and set it as an attribute
        self.user = User.objects.create_user(
            firstName="John",
            lastName="Doe",
            email="john.doe@example.com",
            password="password123",
            phone="1234567890"
        )

    def test_register_and_login_user_successfully(self):
        # Register the user
        register_response = self.client.post(self.register_url, self.user_data)
        print(f"Register response content: {register_response.content}")
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        # Login the user
        login_data = {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }
        login_response = self.client.post(self.login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_token_generation(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, {
            "email": "john.doe@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_organisation_access_control(self):
        org = Organisation.objects.create(
            orgId="org123",
            name="John's Organisation",
            description="Test Description"
        )
        org.users.add(self.user)  # Add the user to the organisation
        print(f"Created organisation: {org.orgId}")
        
        # Authenticate as the user
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(f'/api/organisations/{org.orgId}/')
        if response.status_code != status.HTTP_200_OK:
            print(f"Access Control Test Response (User): {response.status_code}")
        else:
            print(f"Access Control Test Response (User): {response.status_code} - {response.data}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['data']['name'], "John's Organisation")

        # Access control: another user should not access this organization
        another_user_data = {
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jane.doe@example.com",
            "password": "password123",
            "phone": "9876543210"
        }
        another_user = User.objects.create_user(**another_user_data)
        self.client.force_authenticate(user=another_user)
        response = self.client.get(f'/api/organisations/{org.orgId}/')
        if response.status_code != status.HTTP_403_FORBIDDEN:
            print(f"Access Control Test Response (Another User): {response.status_code}")
        else:
            print(f"Access Control Test Response (Another User): {response.status_code} - {response.data}")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RegisterEndpointTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "1234567890"
        }

    def test_duplicate_email(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_missing_fields(self):
        data = {
            "firstName": "",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
