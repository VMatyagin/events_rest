from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Boec

from so.serializers import BoecShortSerializer

BOEC_URL = reverse('so:boec-list')


class PublicBoecApiTests(TestCase):
    """test the publicly available boec api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for retrieving boec's list"""
        res = self.client.get(BOEC_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBoecApiTest(TestCase):
    """test the authorized user boec API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'pass123'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_boec_list(self):
        """test retrieve boec"""
        Boec.objects.create(
            firstName='firstName',
            lastName='lastName',
            middleName='middleName',
        )
        Boec.objects.create(
            firstName='YfirstName',
            lastName='lastName',
            middleName='middleName',
        )
        Boec.objects.create(
            firstName='AfirstName',
            lastName='lastName',
            middleName='middleName',
        )

        res = self.client.get(BOEC_URL)

        list = Boec.objects.all().order_by('-id')
        serializer = BoecShortSerializer(list, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['items'], serializer.data)

    def test_create_boec_successful(self):
        """test creating a new boec"""
        payload = {
            "firstName": 'AfirstName',
            "lastName": 'lastName',
            "middleName": 'middleName',
        }
        self.client.post(BOEC_URL, payload)
        exists = Boec.objects.filter(
            firstName=payload['firstName']
        ).exists()
        self.assertTrue(exists)

    def test_create_boec_invalid(self):
        """test creating a new boec with invalid payload"""
        payload = {'lastName': ''}
        res = self.client.post(BOEC_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
