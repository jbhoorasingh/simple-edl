from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from edl.models import Edl, EdlEntry  # Import your models
from edl.serializers import EdlSerializer, EdlEntrySerializer  # Import your serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class EdlAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/edl/'  # Replace with your API endpoint URL

    def create_authenticated_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        token = AccessToken.for_user(user)
        return user, token

    def test_authenticated_user_can_access_endpoint(self):
        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Make requests as an authenticated user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_access_endpoint(self):
        # Make requests without authentication
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_edl_ip_address(self):
        data = {"name": "test_ip_list_1",
                "description": "Test - IP List - 1",
                "edl_type": "ip_address"}
        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Edl.objects.count(), 1)

    def test_create_edl_fqdn(self):
        data = {"name": "test_fqdn_1",
                "description": "Test - FQDN - 1",
                "edl_type": "fqdn"}
        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Edl.objects.count(), 1)

    def test_create_edl_url(self):
        data = {"name": "test_url_1",
                "description": "Test - URL - 1",
                "edl_type": "url"}
        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Edl.objects.count(), 1)

    def test_get_edl_list(self):
        Edl.objects.create(name='test_ip_list_1', description='Test - IP List - 1', edl_type='ip_address')
        Edl.objects.create(name='test_fqdn_1', description='Test - FQDN - 1', edl_type='fqdn')
        Edl.objects.create(name='test_url_1', description='Test - URL - 1', edl_type='url')
        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Edl.objects.count())
