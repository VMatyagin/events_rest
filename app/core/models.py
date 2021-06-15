import os
import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError
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

    def create_user(self, vkId, password=None, **extra_fields):
        """creates and saves a new user"""
        if not vkId:
            raise ValueError('Users must have an vkId')
        user = self.model(vkId=vkId, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)

        return user

    def create_superuser(self, vkId, password=None):
        """creates and save a new super user"""
        if not password:
            raise ValueError('SuperUsers must have password')
        user = self.create_user(vkId=vkId, password=password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


@reversion.register()
class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that support using id instead of username"""
    vkId = models.IntegerField(unique=True)

    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)
    password = models.CharField(max_length=128, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'vkId'

    def __str__(self):
        return f"{self.vkId}"


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

    @property
    def brigades_count(self):
        return self.brigades.count()

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
    vkId = models.IntegerField(
        verbose_name='VK id', blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.lastName} {self.firstName} {self.middleName}"


@reversion.register()
class Brigade(models.Model):
    """Brigade object"""

    class Meta:
        verbose_name = 'Отряд'
        verbose_name_plural = 'Отряды'

    title = models.CharField(max_length=255)
    area = models.ForeignKey(
        Area, on_delete=models.RESTRICT, related_name='brigades')
    shtab = models.ForeignKey(Shtab, on_delete=models.RESTRICT)
    boec = models.ManyToManyField(Boec, blank=True, related_name='brigades')
    DOB = models.DateTimeField(null=True, blank=True)
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

    class EventWorth(models.IntegerChoices):
        UNSET = 0, _('Не учитывается')
        ART = 1, _('Творчество')
        SPORT = 2, _('Спорт')
        VOLONTEER = 3, _('Волонтерство')
        CITY = 4, _('Городское')

    status = models.IntegerField(
        choices=EventStatus.choices, default=EventStatus.JUST_CREATED,
        verbose_name='Статус мероприятия'
    )
    worth = models.IntegerField(
        choices=EventWorth.choices, default=EventWorth.UNSET,
        verbose_name='Ценность блоков',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Место проведение'
    )
    shtab = models.ForeignKey(
        Shtab,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Штаб'
    )
    startDate = models.DateTimeField(
        verbose_name='Дата начала'
    )
    startTime = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Время начала'
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
        Boec, on_delete=models.CASCADE, verbose_name='ФИО',
        related_name='seasons')
    brigade = models.ForeignKey(
        Brigade, on_delete=models.RESTRICT, verbose_name='Отряд', related_name='seasons')
    year = models.IntegerField(verbose_name='Год выезда')

    def __str__(self):
        return f"{self.year} - {self.brigade.title} {self.boec.lastName}"


@reversion.register()
class Position(models.Model):
    """Position model"""

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    class PositionEnum(models.IntegerChoices):
        WORKER = 0, _('Работник')
        KOMENDANT = 1, _('Комендант')
        METODIST = 2, _('Методист')
        MASTER = 3, _('Мастер')
        KOMISSAR = 4, _('Комиссар')
        KOMANDIR = 5,  _('Командир')

    position = models.IntegerField(
        choices=PositionEnum.choices,
        verbose_name='Должность'
    )

    boec = models.ForeignKey(
        Boec,
        on_delete=models.RESTRICT,
        verbose_name='Боец',
        related_name='positions',
    )

    brigade = models.ForeignKey(
        Brigade,
        on_delete=models.RESTRICT,
        verbose_name='Отряд',
        related_name='positions',
        null=True,
        blank=True
    )
    shtab = models.ForeignKey(
        Shtab,
        on_delete=models.RESTRICT,
        verbose_name='Штаб',
        related_name='positions',
        null=True,
        blank=True
    )
    fromDate = models.DateTimeField(default=timezone.now)
    toDate = models.DateTimeField(null=True, blank=True)

    def validate(self, data):
        if not data['brigade'] and not data['shtab']:
            raise ValidationError(
                {'error': 'Even one of brigade or shtab should have a value.'})

    def __str__(self):
        additionalMsg = _('Действующий') if (not self.toDate) else ""
        return f"{self.get_position_display()} | {self.brigade.title} | {self.boec} | {additionalMsg}"


@reversion.register()
class Participant(models.Model):
    """Participant model"""

    class Meta:
        verbose_name = 'Участник мероприятия'
        verbose_name_plural = 'Участники мероприятия'

    boec = models.ForeignKey(
        Boec, on_delete=models.RESTRICT, verbose_name='Участник',
        related_name='participation'
    )

    event = models.ForeignKey(
        Event, on_delete=models.RESTRICT, verbose_name='Мероприятие',
        related_name='participant'
    )

    class WorthEnum(models.IntegerChoices):
        VOLONTEER = 0, _('Волонтер')
        ORGANIZER = 1, _('Организатор')
        DEFAULT = 3, _('Участник')

    worth = models.IntegerField(
        choices=WorthEnum.choices,
        verbose_name='Статус участия',
        default=WorthEnum.DEFAULT
    )

    def __str__(self):
        return f"{self.boec.lastName} | {self.worth} | {self.event.title}"
