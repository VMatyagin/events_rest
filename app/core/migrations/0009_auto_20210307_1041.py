# Generated by Django 3.1.7 on 2021-03-07 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210306_1118'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'verbose_name': 'Направления', 'verbose_name_plural': 'Направления'},
        ),
        migrations.AlterModelOptions(
            name='boec',
            options={'verbose_name': 'Боец', 'verbose_name_plural': 'Бойцы'},
        ),
        migrations.AlterModelOptions(
            name='brigade',
            options={'verbose_name': 'Отряд', 'verbose_name_plural': 'Отряды'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Мероприятие', 'verbose_name_plural': 'Мероприятия'},
        ),
        migrations.AlterModelOptions(
            name='eventorder',
            options={'verbose_name': 'Заявка на мероприятие', 'verbose_name_plural': 'Заявки на мероприятие'},
        ),
        migrations.AlterModelOptions(
            name='season',
            options={'verbose_name': 'Выезжавший на сезон', 'verbose_name_plural': 'Выезжавшие на сезон'},
        ),
        migrations.AlterModelOptions(
            name='shtab',
            options={'verbose_name': 'Штаб', 'verbose_name_plural': 'Штабы'},
        ),
        migrations.AddField(
            model_name='eventorder',
            name='title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='eventorder',
            name='isСontender',
            field=models.BooleanField(default=False, verbose_name='Прошел в конкурсную программу (или плей-офф)'),
        ),
        migrations.AlterField(
            model_name='eventorder',
            name='place',
            field=models.IntegerField(blank=True, choices=[(1, 'Первое место'), (2, 'Второе место'), (3, 'Третье место')], null=True, verbose_name='Занятое место'),
        ),
    ]
