# Generated by Django 3.1.12 on 2021-06-15 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0007_auto_20210615_1459")]

    operations = [
        migrations.CreateModel(
            name="Competition",
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
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="competitions",
                        to="core.event",
                        verbose_name="Мероприятие",
                    ),
                ),
            ],
            options={
                "verbose_name": "Конкурс мероприятия",
                "verbose_name_plural": "Конкурсы мероприятий",
            },
        ),
        migrations.CreateModel(
            name="CompetitionParticipant",
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
                    "worth",
                    models.IntegerField(
                        choices=[
                            (0, "Заявка"),
                            (1, "Участие/плей-офф"),
                            (2, "Призовое место/номинация"),
                            (3, "Без рейтинговое(ая) призовое/номинация"),
                        ],
                        default=0,
                        verbose_name="Статус участника",
                    ),
                ),
                (
                    "boec",
                    models.ManyToManyField(
                        blank=True,
                        related_name="competition_participation",
                        to="core.Boec",
                    ),
                ),
                (
                    "competition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="competition_participation",
                        to="core.competition",
                        verbose_name="Конкурс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка на мероприятие",
                "verbose_name_plural": "Заявки на мероприятие",
            },
        ),
        migrations.RemoveField(model_name="nomination", name="event"),
        migrations.AlterField(
            model_name="participant",
            name="boec",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="event_participation",
                to="core.boec",
                verbose_name="Боец",
            ),
        ),
        migrations.AlterField(
            model_name="participant",
            name="worth",
            field=models.IntegerField(
                choices=[(0, "Участник"), (1, "Волонтер"), (2, "Организатор")],
                default=0,
                verbose_name="Статус участия",
            ),
        ),
        migrations.DeleteModel(name="BrigadeParticipant"),
        migrations.AddField(
            model_name="nomination",
            name="competition",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="nominations",
                to="core.competition",
                verbose_name="Конкурс",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="nomination",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="nomination",
                to="core.competitionparticipant",
                verbose_name="Получатель",
            ),
        ),
    ]