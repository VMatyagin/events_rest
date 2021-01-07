from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models


def sample_user(email='test@email.com', password='testpass'):
    """create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_witht_email_sussessfull(self):
        """Test creating a new user with an email is successfulll"""
        email = 'test@test.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_noramized(self):
        """test the email for a new user is normalized"""
        email = 'test@TEST.com'
        user = get_user_model().objects.create_user(
            email,
            'test123'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test')

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@super.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

    def test_shtab_str(self):
        """test the shtab string representaion"""
        shtab = models.Shtab.objects.create(
            title='Shtab Petra'
        )

        self.assertEqual(str(shtab), shtab.title)

    def test_area_str(self):
        """test the areas string representaion"""
        area = models.Area.objects.create(
            title="First direction",
            shortTitle='DFO'
        )

        self.assertEqual(str(area), area.shortTitle)

    def test_boec_str(self):
        """test the boec's represenation"""
        boec = models.Boec.objects.create(
            firstName='firstName',
            lastName='lastName',
            middleName='middleName',
            DOB=0
        )

        self.assertEqual(
            str(boec), f"{boec.lastName} {boec.firstName} {boec.middleName}")

    def test_brigade_str(self):
        """test the brigage representation"""
        area = models.Area.objects.create(
            title="First direction",
            shortTitle='DFO'
        )
        shtab = models.Shtab.objects.create(
            title='Shtab Petra'
        )
        brigade = models.Brigade.objects.create(
            title='name',
            DOB=0,
            area=area,
            shtab=shtab
        )
        self.assertEqual(str(brigade), f"{area.shortTitle} {brigade.title}")

    def test_event_str(self):
        """test the event representation"""
        event = models.Event.objects.create(
            status=0,
            title='example name'
        )

        self.assertEqual(str(event), event.title)
