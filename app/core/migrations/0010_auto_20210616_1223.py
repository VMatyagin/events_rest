# Generated by Django 3.1.12 on 2021-06-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0009_competition_title")]

    operations = [
        migrations.AddField(
            model_name="competitionparticipant",
            name="brigade",
            field=models.ManyToManyField(
                related_name="competition_participation", to="core.Brigade"
            ),
        ),
        migrations.AlterField(
            model_name="competitionparticipant",
            name="boec",
            field=models.ManyToManyField(
                related_name="competition_participation", to="core.Boec"
            ),
        ),
    ]
