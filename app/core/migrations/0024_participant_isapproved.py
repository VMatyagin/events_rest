# Generated by Django 3.1.13 on 2021-07-15 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_participant_brigade"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="isApproved",
            field=models.BooleanField(default=False),
        ),
    ]
