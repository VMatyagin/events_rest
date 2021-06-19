from core.models import Area, Boec, Brigade, Season, Shtab
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from so.serializers import SeasonSerializer

SEASON_URL = reverse("so:season-list")


def sample_shtab(title="shtab title"):
    """Create and return a sample shtab"""
    return Shtab.objects.create(title=title)


def sample_area(title="Second", shortTitle="2"):
    """Create and return a sample area"""
    return Area.objects.create(title=title, shortTitle=shortTitle)


def sample_boec(firstName="Name", lastName="LastName", middleName=""):
    """Create and return a sample boec"""
    return Boec.objects.create(
        firstName=firstName, lastName=lastName, middleName=middleName
    )


def sample_brigade(title="title"):
    """Create and return a sample area"""
    return Brigade.objects.create(title=title, area=sample_area(), shtab=sample_shtab())


class PublicAreaApiTests(TestCase):
    """test the publicly available area api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for retrieving areas"""
        res = self.client.get(SEASON_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAreaApiTest(TestCase):
    """test the authorized user area API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user("test@email.com", "pass123")

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_seasons_list(self):
        """test retrieve seasons"""
        Season.objects.create(boec=sample_boec(), brigade=sample_brigade(), year=2020)

        Season.objects.create(boec=sample_boec(), brigade=sample_brigade(), year=2020)

        res = self.client.get(SEASON_URL)

        lst = Season.objects.all()
        serializer = SeasonSerializer(lst, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["items"], serializer.data)

    def test_create_season_successful(self):
        """test creating a new season"""

        brigade = sample_brigade()
        boec = sample_boec()

        payload = {"boec": boec.id, "brigade_id": brigade.id, "year": 2020}
        self.client.post(SEASON_URL, payload)
        exists = Season.objects.filter(boec=payload["boec"]).exists()
        self.assertTrue(exists)

    def test_create_area_invalid(self):
        """test creating a new season with invalid payload"""
        payload = {}
        res = self.client.post(SEASON_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
