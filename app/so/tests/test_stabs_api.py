from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Shtab

from so.serializers import ShtabSerializer

SHTAB_URL = reverse('so:shtab-list')


class PublicShtabApiTests(TestCase):
    """test the publicly available shtab api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for retrieving tags"""
        res = self.client.get(SHTAB_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateShtabApiTest(TestCase):
    """test the authorized user shtab API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'pass123'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_shtab_list(self):
        """test retrieve shtab"""
        Shtab.objects.create(title='First')
        Shtab.objects.create(title='Second')

        res = self.client.get(SHTAB_URL)

        list = Shtab.objects.all().order_by('-title')
        serializer = ShtabSerializer(list, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_shtab_successful(self):
        """test creating a new shtab"""
        payload = {
            'title': 'test title'
        }
        self.client.post(SHTAB_URL, payload)
        exists = Shtab.objects.filter(
            title=payload['title']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """test creating a new shtab with invalid payload"""
        payload = {'title': ''}
        res = self.client.post(SHTAB_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
