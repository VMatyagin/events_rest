import json
import pygsheets
import numpy as np
import datetime

from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):

        client = pygsheets.authorize()

        sht = client.open_by_key(
            '1s_NVTmYxG5GloDaOOw4d7eh7P_zAcobTmIRseYHsg3g')
        sht.add_worksheet(f"{datetime.date.today()}")
