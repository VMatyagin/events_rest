import os
import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class UserManager(BaseUserManager):

    def create_user(self, vk_id, password=None, **extra_fields):
        """creates and saves a new user"""
        if not vk_id:
            raise ValueError('Users must have an vk_id')
        user = self.model(vk_id=vk_id, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)

        return user

    def create_superuser(self, vk_id, password=None):
        """creates and save a new super user"""
        if not password:
            raise ValueError('SuperUsers must have password')
        user = self.create_user(vk_id=vk_id, password=password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that support using id instead of username"""
    vk_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)
    password = models.CharField(max_length=128, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'vk_id'


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
    boec = models.ManyToManyField(Boec, blank=True, related_name='brigades')
    DOB = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


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


class Season(models.Model):
    """Season model"""
    boec = models.ForeignKey(
        Boec, on_delete=models.RESTRICT, verbose_name='ФИО', related_name='seasons')
    brigade = models.ForeignKey(
        Brigade, on_delete=models.RESTRICT, verbose_name='Отряд')
    year = models.IntegerField(verbose_name='Год выезда')

    def __str__(self):
        return f"{self.year} - {self.brigade.title} {self.boec.lastName}"
