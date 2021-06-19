import json

from core.models import Area, Brigade, Shtab
from django.core.management.base import BaseCommand
from django.utils.encoding import force_str
from django.utils.translation import ugettext_lazy as _


class Command(BaseCommand):
    """Parse JSON file and load data to DB"""

    area = None
    shtab = None

    def findArea(self, area):
        areaList = Area.objects.filter(shortTitle=area)
        if not areaList.exists():
            Area.objects.create(title=force_str(""), shortTitle=_(area))

        self.area = Area.objects.get(shortTitle=_(area))

    def findShtab(self, shtab):
        shtabList = Shtab.objects.filter(title=shtab)

        if not shtabList.exists():
            Shtab.objects.create(title=shtab)

        self.shtab = Shtab.objects.get(title=shtab)

    def handle(self, *args, **options):
        with open(
            "brigades.json", encoding="utf-8", errors="surrogateescape"
        ) as json_file:
            data = json.load(json_file)
        for item in data:
            self.findArea(item["direction"])
            self.findShtab(item["shtab"])

            brigade = Brigade.objects.filter(title=item["name"])

            if not brigade.exists():
                Brigade.objects.create(
                    title=item["name"], area=self.area, shtab=self.shtab
                )
