# Generated by Django 3.1.12 on 2021-06-09 19:12

import core.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Area",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("shortTitle", models.CharField(max_length=10)),
                ("created_at", models.DateField(default=django.utils.timezone.now)),
                (
                    "updated_at",
                    core.models.AutoDateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={
                "verbose_name": "Направления",
                "verbose_name_plural": "Направления",
            },
        ),
        migrations.CreateModel(
            name="Boec",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("firstName", models.CharField(max_length=255)),
                ("lastName", models.CharField(max_length=255)),
                ("middleName", models.CharField(blank=True, max_length=255)),
                ("DOB", models.DateField(blank=True, null=True)),
                ("created_at", models.DateField(default=django.utils.timezone.now)),
                (
                    "updated_at",
                    core.models.AutoDateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "vkId",
                    models.IntegerField(
                        blank=True, null=True, unique=True, verbose_name="VK id"
                    ),
                ),
            ],
            options={
                "verbose_name": "Боец",
                "verbose_name_plural": "Бойцы",
            },
        ),
        migrations.CreateModel(
            name="Brigade",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("DOB", models.DateTimeField(blank=True, null=True)),
                ("status", models.BooleanField(default=True)),
                ("created_at", models.DateField(default=django.utils.timezone.now)),
                (
                    "updated_at",
                    core.models.AutoDateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "area",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="brigades",
                        to="core.area",
                    ),
                ),
                (
                    "boec",
                    models.ManyToManyField(
                        blank=True, related_name="brigades", to="core.Boec"
                    ),
                ),
            ],
            options={
                "verbose_name": "Отряд",
                "verbose_name_plural": "Отряды",
            },
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "Мероприятие создано"),
                            (1, "Мероприятие прошло"),
                            (2, "Мероприятие не прошло"),
                        ],
                        default=0,
                        verbose_name="Статус мероприятия",
                    ),
                ),
                (
                    "worth",
                    models.CharField(
                        choices=[
                            ("0", "Не учитывается"),
                            ("1", "Творчество"),
                            ("2", "Спорт"),
                            ("3", "Волонтерство"),
                            ("4", "Городское"),
                        ],
                        default="0",
                        max_length=5,
                        verbose_name="Ценность блоков",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Описание"
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Место проведение"
                    ),
                ),
                (
                    "startDate",
                    models.DateField(blank=True, null=True, verbose_name="Дата начала"),
                ),
                (
                    "startTime",
                    models.TimeField(
                        blank=True, null=True, verbose_name="Время начала"
                    ),
                ),
                (
                    "visibility",
                    models.BooleanField(default=False, verbose_name="Видимость"),
                ),
                (
                    "organizer",
                    models.ManyToManyField(
                        blank=True,
                        related_name="organizers_list",
                        to="core.Boec",
                        verbose_name="Организаторы",
                    ),
                ),
            ],
            options={
                "verbose_name": "Мероприятие",
                "verbose_name_plural": "Мероприятия",
            },
        ),
        migrations.CreateModel(
            name="Shtab",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("created_at", models.DateField(default=django.utils.timezone.now)),
                (
                    "updated_at",
                    core.models.AutoDateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={
                "verbose_name": "Штаб",
                "verbose_name_plural": "Штабы",
            },
        ),
        migrations.CreateModel(
            name="Season",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.IntegerField(verbose_name="Год выезда")),
                (
                    "boec",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="seasons",
                        to="core.boec",
                        verbose_name="ФИО",
                    ),
                ),
                (
                    "brigade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="seasons",
                        to="core.brigade",
                        verbose_name="Отряд",
                    ),
                ),
            ],
            options={
                "verbose_name": "Выезжавший на сезон",
                "verbose_name_plural": "Выезжавшие на сезон",
            },
        ),
        migrations.CreateModel(
            name="Position",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "position",
                    models.IntegerField(
                        choices=[
                            (0, "Работник"),
                            (1, "Комендант"),
                            (2, "Методист"),
                            (3, "Мастер"),
                            (4, "Комиссар"),
                            (5, "Командир"),
                        ],
                        verbose_name="Должность",
                    ),
                ),
                ("fromDate", models.DateTimeField(default=django.utils.timezone.now)),
                ("toDate", models.DateTimeField(blank=True, null=True)),
                (
                    "boec",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="positions",
                        to="core.boec",
                        verbose_name="Боец",
                    ),
                ),
                (
                    "brigade",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="positions",
                        to="core.brigade",
                        verbose_name="Отряд",
                    ),
                ),
                (
                    "shtab",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="positions",
                        to="core.shtab",
                        verbose_name="Штаб",
                    ),
                ),
            ],
            options={
                "verbose_name": "Должность",
                "verbose_name_plural": "Должности",
            },
        ),
        migrations.CreateModel(
            name="EventOrder",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Название"
                    ),
                ),
                (
                    "isСontender",
                    models.BooleanField(
                        default=False,
                        verbose_name="Прошел в конкурсную программу (или плей-офф)",
                    ),
                ),
                (
                    "place",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("1", "Первое место"),
                            ("2", "Второе место"),
                            ("3", "Третье место"),
                        ],
                        max_length=5,
                        null=True,
                        verbose_name="Занятое место",
                    ),
                ),
                (
                    "brigades",
                    models.ManyToManyField(
                        related_name="event_participations", to="core.Brigade"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="orders",
                        to="core.event",
                        verbose_name="Мероприятие",
                    ),
                ),
                (
                    "participations",
                    models.ManyToManyField(
                        blank=True, related_name="event_participations", to="core.Boec"
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка на мероприятие",
                "verbose_name_plural": "Заявки на мероприятие",
            },
        ),
        migrations.AddField(
            model_name="event",
            name="shtab",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.shtab",
                verbose_name="Штаб",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="volonteer",
            field=models.ManyToManyField(
                blank=True,
                related_name="volonteers_list",
                to="core.Boec",
                verbose_name="Волонтеры",
            ),
        ),
        migrations.AddField(
            model_name="brigade",
            name="shtab",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="core.shtab"
            ),
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without "
                        "explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("vkId", models.IntegerField(unique=True)),
                ("name", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("created_at", models.DateField(default=django.utils.timezone.now)),
                (
                    "updated_at",
                    core.models.AutoDateTimeField(default=django.utils.timezone.now),
                ),
                ("password", models.CharField(blank=True, max_length=128)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all "
                        "permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
