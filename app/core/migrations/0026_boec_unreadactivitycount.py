# Generated by Django 3.1.13 on 2021-07-16 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0025_activity_warning"),
    ]

    operations = [
        migrations.AddField(
            model_name="boec",
            name="unreadActivityCount",
            field=models.IntegerField(default=0),
        ),
    ]