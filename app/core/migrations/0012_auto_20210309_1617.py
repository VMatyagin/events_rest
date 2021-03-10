# Generated by Django 3.1.7 on 2021-03-09 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210307_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='worth',
            field=models.CharField(choices=[('0', 'Не учитывается'), ('1', 'Творчество'), ('2', 'Спорт'), ('3', 'Волонтерство'), ('4', 'Городское')], default='0', max_length=5, verbose_name='Ценность блоков'),
        ),
        migrations.RemoveField(
            model_name='eventorder',
            name='brigade',
        ),
        migrations.AddField(
            model_name='eventorder',
            name='brigade',
            field=models.ManyToManyField(related_name='event_participations', to='core.Brigade'),
        ),
    ]
