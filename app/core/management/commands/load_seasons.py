import json

from django.core.management.base import BaseCommand

from core.models import Boec, Brigade, Season


class Command(BaseCommand):
    """Parse JSON file and load data to DB"""

    def handle(self, *args, **options):
        with open('data.json', encoding='utf-8') as json_file:
            data = json.load(json_file)
        for item in data:
            try:
                fio = item['name'].split()

                middleName = fio[2] if len(fio) > 2 else ''
                lastName = fio[0] if len(fio) > 1 else ''
                firstName = fio[1] if len(fio) > 1 else ''

                boecList = Boec.objects.filter(
                    firstName=firstName, lastName=lastName,
                    middleName=middleName
                )

                if (not boecList.exists()):
                    Boec.objects.create(
                        firstName=firstName, lastName=lastName,
                        middleName=middleName
                    )

                brigade = Brigade.objects.get(title=item['brigade'])
                boec = Boec.objects.get(
                    firstName=firstName, lastName=lastName,
                    middleName=middleName
                )

                if (not Season.objects.filter(
                    boec=boec, brigade=brigade, year=int(item['year'])
                ).exists()):
                    Season.objects.create(
                        boec=boec, brigade=brigade, year=int(item['year']))
            except Exception:
                print(item)
