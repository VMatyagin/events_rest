from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Brigade, Shtab, Area

from so.serializers import BrigadeShortSerializer

BRIGADE_URL = reverse('so:brigade-list')


def sample_shtab(title='shtab title'):
    """Create and return a sample shtab"""
    return Shtab.objects.create(title=title)


def sample_area(title='Second', shortTitle='2'):
    """Create and return a sample area"""
    return Area.objects.create(title=title, shortTitle=shortTitle)


class PublicBrigadeApiTests(TestCase):
    """test the publicly available brigade api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for retrieving brigades list"""
        res = self.client.get(BRIGADE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBrigadeApiTest(TestCase):
    """test the authorized user brigade API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'pass123'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_brigade_list(self):
        """test retrieve brigade"""

        Brigade.objects.create(
            title='name',
            area=sample_area(),
            shtab=sample_shtab()
        )
        Brigade.objects.create(
            title='yname',
            area=sample_area(),
            shtab=sample_shtab()
        )
        Brigade.objects.create(
            title='aname',
            area=sample_area(),
            shtab=sample_shtab()
        )
        res = self.client.get(BRIGADE_URL)

        list = Brigade.objects.all().order_by('-title')
        serializer = BrigadeShortSerializer(list, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['items'], serializer.data)

    def test_create_brigade_successful(self):
        """test creating a new brigade"""
        area = sample_area()
        shtab = sample_shtab()
        payload = {
            "title": 'success',
            "area": area.id,
            'shtab': shtab.id
        }
        self.client.post(BRIGADE_URL, payload)
        exists = Brigade.objects.filter(
            title=payload['title']
        ).exists()
        self.assertTrue(exists)

    def test_create_brigade_invalid(self):
        """test creating a new brigade with invalid payload"""
        payload = {'title': ''}
        res = self.client.post(BRIGADE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
