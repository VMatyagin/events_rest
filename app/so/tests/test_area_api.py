from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Area

from so.serializers import AreaSerializer

AREA_URL = reverse('so:area-list')


class PublicAreaApiTests(TestCase):
    """test the publicly available area api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for retrieving areas"""
        res = self.client.get(AREA_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAreaApiTest(TestCase):
    """test the authorized user area API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'pass123'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_areas_list(self):
        """test retrieve area"""
        Area.objects.create(title='First', shortTitle='100')
        Area.objects.create(title='Second', shortTitle='2')

        res = self.client.get(AREA_URL)

        list = Area.objects.all().order_by('-shortTitle')
        serializer = AreaSerializer(list, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['items'], serializer.data)

    def test_create_area_successful(self):
        """test creating a new area"""
        payload = {
            'title': 'new area',
            'shortTitle': 'short'
        }
        self.client.post(AREA_URL, payload)
        exists = Area.objects.filter(
            title=payload['title']
        ).exists()
        self.assertTrue(exists)

    def test_create_area_invalid(self):
        """test creating a new area with invalid payload"""
        payload = {'title': ''}
        res = self.client.post(AREA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
