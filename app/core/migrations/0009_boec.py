# Generated by Django 3.1.5 on 2021-01-07 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('middleName', models.CharField(blank=True, max_length=255)),
                ('DOB', models.IntegerField()),
            ],
        ),
    ]
