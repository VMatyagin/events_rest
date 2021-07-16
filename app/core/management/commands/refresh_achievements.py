import json

from core.models import Achievement, Activity, Boec, Brigade, Season, User
from django.core.management.base import BaseCommand
from so.views import generateBoecProgess


class Command(BaseCommand):
    """Parse JSON file and load data to DB"""

    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:
            try:
                boec = Boec.objects.get(vkId=user.vkId)
            except (Boec.DoesNotExist):
                continue

            progress = generateBoecProgess(pk=boec.id)

            achievements = Achievement.objects.all()

            for ach in achievements:
                user_progress = progress.get(ach.type, 0)

                # если достижение еще не выдано юзеру, то выдаем и генерим уведомление
                if (
                    user_progress >= ach.goal
                    and not ach.boec.filter(id=boec.id).exists()
                ):
                    ach.boec.add(boec)
                    Activity.objects.create(type=2, boec=boec, achievement=ach)
                    boec.unreadActivityCount += 1

            boec.save()
