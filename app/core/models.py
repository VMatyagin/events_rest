import uuid
import os

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """creates and save a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that support using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """tag to be user for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Shtab(models.Model):
    """Shtab object"""
    title = models.CharField(max_length=255)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Area(models.Model):
    """Area (direction) object"""
    title = models.CharField(max_length=255)
    shortTitle = models.CharField(max_length=10)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    def __str__(self):
        return self.shortTitle


class Boec(models.Model):
    """Boec object"""
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    middleName = models.CharField(max_length=255, blank=True)
    DOB = models.DateField(null=True, blank=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.lastName} {self.firstName} {self.middleName}"


class Brigade(models.Model):
    """Brigade object"""
    title = models.CharField(max_length=255)
    area = models.ForeignKey(Area, on_delete=models.RESTRICT)
    shtab = models.ForeignKey(Shtab, on_delete=models.RESTRICT)
    boec = models.ManyToManyField(Boec, blank=True)
    DOB = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.area.shortTitle} {self.title}"


class Event(models.Model):
    """Event model"""
    class EventStatus(models.IntegerChoices):
        JUST_CREATED = 0
        PASSED = 1
        NOT_PASSED = 2

    status = models.IntegerField(
        choices=EventStatus.choices, default=EventStatus.JUST_CREATED)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    shtab = models.ForeignKey(Shtab, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    organizer = models.ManyToManyField(
        Boec, blank=True, related_name='organizers_list')
    volonteer = models.ManyToManyField(
        Boec, blank=True, related_name='volonteers_list')
    visibility = models.BooleanField(default=False)

    def __str__(self):
        return self.title
