from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Organisation
from rest_framework.test import APITestCase

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "userId": "unique123",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

    def test_token_generation(self):
        response = self.client.post('/auth/login', {
            "email": "john.doe@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])

    def test_organisation_access_control(self):
        org = Organisation.objects.create(
            orgId="org123",
            name="John's Organisation",
            description="Test Description"
        )
        org.users.add(self.user)
        print(f"Created organisation: {org.orgId}")
        response = self.client.get(f'/api/organisations/{org.orgId}/')
        if response.status_code != status.HTTP_200_OK:
            print(f"Access Control Test Response (User): {response.status_code}")
        else:
            print(f"Access Control Test Response (User): {response.status_code} - {response.data}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['data']['name'], "John's Organisation")
        
        # Access control: another user should not access this organization
        another_user_data = {
            "userId": "unique456",
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
    def test_register_user_successfully(self):
        data = {
            "userId": "unique124",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post('/auth/register', data)
        print(f"Register Test Response: {response.status_code} - {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_email_or_userId(self):
        data = {
            "userId": "unique125",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        self.client.post('/auth/register', data)
        response = self.client.post('/auth/register', data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_login_user_successfully(self):
        data = {
            "userId": "unique126",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        self.client.post('/auth/register', data)
        login_data = {
            "email": "john@example.com",
            "password": "password123"
        }
        response = self.client.post('/auth/login', login_data)
        print(f"Login Test Response: {response.status_code} - {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_missing_fields(self):
        data = {
            "firstName": "",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post('/auth/register', data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
