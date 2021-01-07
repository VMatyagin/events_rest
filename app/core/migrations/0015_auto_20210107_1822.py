# Generated by Django 3.1.5 on 2021-01-07 18:22

import core.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_brigade_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='area',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='boec',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='boec',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='brigade',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='brigade',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='shtab',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='shtab',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=core.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
    ]