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
        """Test that authenticated users can access the endpoint"""
        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Make requests as an authenticated user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_unauthenticated_user_cannot_access_endpoint(self):
        """Test that unauthenticated users cannot access the endpoint"""
        # Make requests without authentication
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_edl_ip_address(self):
        """Test creating a new EDL of type IP Address"""
        data = {"name": "test_ip_list_1",
                "description": "Test - IP List - 1",
                "edl_type": "ip_address"}
        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Edl.objects.count(), 1)


    def test_create_edl_ip_entries(self):
        edl = Edl.objects.create(name='test_ip_list_1', description='Test - IP List - 1', edl_type='ip_address')
        entries_to_add = [
            {"entry_value": "10.0.0.1", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "10.0.0.0/8", "valid_until": "2035-01-17T18:53:08.956Z"},
            {"entry_value": "10.0.0.0", "valid_until": "2036-01-17T18:53:08.956Z"}
        ]

        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        for data in entries_to_add:
            response = self.client.post('{}{}/entries'.format(self.url, edl.name), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EdlEntry.objects.filter(edl__name='test_ip_list_1').count(), 3)


    def test_create_edl_ip_invalid_entries(self):
        edl = Edl.objects.create(name='test_ip_list_1', description='Test - IP List - 1', edl_type='ip_address')
        entries_to_add = [
            {"entry_value": "test1.com", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "300.300.300.300", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "0/0", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "20...2", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "10.0.0.0/45", "valid_until": "2006-01-17T18:53:08.956Z"}
        ]

        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        for data in entries_to_add:
            response = self.client.post('{}{}/entries'.format(self.url, edl.name), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EdlEntry.objects.filter(edl__name='test_ip_list_1').count(), 0)


    def test_create_edl_fqdn(self):
        data = {"name": "test_fqdn_1",
                "description": "Test - FQDN - 1",
                "edl_type": "fqdn"}
        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Edl.objects.count(), 1)


    def test_create_edl_fqdn_entries(self):
        edl = Edl.objects.create(name='test_fqdn_1', description='Test - FQDN - 1', edl_type='fqdn')
        entries_to_add = [
            {"entry_value": "test1.com", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "test2.com", "valid_until": "2035-01-17T18:53:08.956Z"},
            {"entry_value": "test3.com", "valid_until": "2036-01-17T18:53:08.956Z"}
        ]

        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        for data in entries_to_add:
            response = self.client.post('{}{}/entries'.format(self.url, edl.name), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EdlEntry.objects.filter(edl__name='test_fqdn_1').count(), 3)


    def test_create_edl_fqdn_invalid_entries(self):
        edl = Edl.objects.create(name='test_fqdn_1', description='Test - FQDN - 1', edl_type='fqdn')
        entries_to_add = [
            {"entry_value": "test1..com", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "test2", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": ".test3.com", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": ".test4.com/", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": ".test4.com", "valid_until": "2006-01-17T18:53:08.956Z"}
        ]

        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        for data in entries_to_add:
            response = self.client.post('{}{}/entries'.format(self.url, edl.name), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EdlEntry.objects.filter(edl__name='test_fqdn_1').count(), 0)


    def test_create_edl_url(self):
        data = {"name": "test_url_1",
                "description": "Test - URL - 1",
                "edl_type": "url"}
        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Edl.objects.count(), 1)

    def test_create_edl_url_entries(self):
        print('test_create_edl_url_entries')
        edl = Edl.objects.create(name='test_url_1', description='Test - URL - 1', edl_type='url')
        entries_to_add = [
            {"entry_value": "test.com", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "test.com^", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "^test.com", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "*test.com*", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "*.test.com", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "test.*", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "test.com/", "valid_until": "2036-01-17T18:53:08.956Z"}

        ]

        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        for data in entries_to_add:
            response = self.client.post('{}{}/entries'.format(self.url, edl.name), data, format='json')
            print(data, response.status_code)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EdlEntry.objects.filter(edl__name=edl.name).count(), 7)


    def test_create_edl_url_invalid_entries(self):
        print('test_create_edl_url_invalid_entries')
        edl = Edl.objects.create(name='test_url_1', description='Test - URL - 1', edl_type='url')
        entries_to_add = [
            {"entry_value": "^test1.com^", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "test.*.com^", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "^test.com*", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": ".test.com", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "*.test.com/", "valid_until": "2036-01-17T18:53:08.956Z"},
            {"entry_value": "test.com", "valid_until": "2006-01-17T18:53:08.956Z"}
        ]

        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        for data in entries_to_add:
            response = self.client.post('{}{}/entries'.format(self.url, edl.name), data, format='json')
            print(data, response.status_code)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EdlEntry.objects.filter(edl__name=edl.name).count(), 0)


    def test_get_edl_list(self):
        Edl.objects.create(name='test_ip_list_1', description='Test - IP List - 1', edl_type='ip_address')
        Edl.objects.create(name='test_fqdn_1', description='Test - FQDN - 1', edl_type='fqdn')
        Edl.objects.create(name='test_url_1', description='Test - URL - 1', edl_type='url')
        user, token = self.create_authenticated_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Edl.objects.count())
