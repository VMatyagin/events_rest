import os
import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
import reversion

from django.utils.translation import ugettext_lazy as _


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


@reversion.register()
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


@reversion.register()
class Shtab(models.Model):
    """Shtab object"""

    class Meta:
        verbose_name = 'Штаб'
        verbose_name_plural = 'Штабы'

    title = models.CharField(max_length=255)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


@reversion.register()
class Area(models.Model):
    """Area (direction) object"""

    class Meta:
        verbose_name = 'Направления'
        verbose_name_plural = 'Направления'

    title = models.CharField(max_length=255)
    shortTitle = models.CharField(max_length=10)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    def __str__(self):
        return self.shortTitle


@reversion.register()
class Boec(models.Model):
    """Boec object"""

    class Meta:
        verbose_name = 'Боец'
        verbose_name_plural = 'Бойцы'

    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    middleName = models.CharField(max_length=255, blank=True)
    DOB = models.DateField(null=True, blank=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.lastName} {self.firstName} {self.middleName}"


@reversion.register()
class Brigade(models.Model):
    """Brigade object"""

    class Meta:
        verbose_name = 'Отряд'
        verbose_name_plural = 'Отряды'

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


@reversion.register()
class Event(models.Model):
    """Event model"""

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    class EventStatus(models.IntegerChoices):
        JUST_CREATED = 0, _('Мероприятие создано')
        PASSED = 1, _('Мероприятие прошло')
        NOT_PASSED = 2,  _('Мероприятие не прошло')

    class EventWorth(models.TextChoices):
        UNSET = "0", _('Не учитывается')
        ART = "1", _('Творчество')
        SPORT = "2", _('Спорт')
        VOLONTEER = "3", _('Волонтерство')
        CITY = "4", _('Городское')

    status = models.IntegerField(
        choices=EventStatus.choices, default=EventStatus.JUST_CREATED,
        verbose_name='Статус мероприятия'
    )
    worth = models.CharField(
        choices=EventWorth.choices, default=EventWorth.UNSET,
        verbose_name='Ценность блоков',
        max_length=5
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Описание'
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Место проведение'
    )
    shtab = models.ForeignKey(
        Shtab,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Штаб'
    )
    startDate = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата начала'
    )
    startTime = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Время начала'
    )
    organizer = models.ManyToManyField(
        Boec, blank=True,
        related_name='organizers_list',
        verbose_name='Организаторы'
    )
    volonteer = models.ManyToManyField(
        Boec, blank=True,
        related_name='volonteers_list',
        verbose_name='Волонтеры'
    )
    visibility = models.BooleanField(
        default=False,
        verbose_name='Видимость'
    )

    def __str__(self):
        return self.title


@reversion.register()
class Season(models.Model):
    """Season model"""

    class Meta:
        verbose_name = 'Выезжавший на сезон'
        verbose_name_plural = 'Выезжавшие на сезон'

    boec = models.ForeignKey(
        Boec, on_delete=models.RESTRICT, verbose_name='ФИО',
        related_name='seasons')
    brigade = models.ForeignKey(
        Brigade, on_delete=models.RESTRICT, verbose_name='Отряд')
    year = models.IntegerField(verbose_name='Год выезда')

    def __str__(self):
        return f"{self.year} - {self.brigade.title} {self.boec.lastName}"


@reversion.register()
class EventOrder(models.Model):
    class Meta:
        verbose_name = 'Заявка на мероприятие'
        verbose_name_plural = 'Заявки на мероприятие'

    class Place(models.TextChoices):
        FIRST = "1", _('Первое место')
        SECOND = "2", _('Второе место')
        THIRD = "3", _('Третье место')

    brigades = models.ManyToManyField(
        Brigade, related_name='event_participations'
    )
    participations = models.ManyToManyField(
        Boec, blank=True, related_name='event_participations'
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Название'
    )
    event = models.ForeignKey(
        Event, blank=True,
        related_name='orders',
        verbose_name='Мероприятие',
        on_delete=models.RESTRICT
    )
    isСontender = models.BooleanField(
        default=False,
        verbose_name='Прошел в конкурсную программу (или плей-офф)'
    )
    place = models.CharField(
        choices=Place.choices,
        null=True,
        blank=True,
        verbose_name='Занятое место',
        max_length=5
    )

    def __str__(self):
        name = f"- {self.title or 'Без названия'} - "
        for brigade in self.brigades.all():
            name += f"{brigade.title} "
        return f"{self.event} {name}"
