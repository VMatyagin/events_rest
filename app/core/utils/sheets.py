import datetime
import logging

import event
import pygsheets
import pytz
from core.models import Boec, Conference, Event, EventWorth, Season
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from pygsheets.cell import Cell
from pygsheets.custom_types import HorizontalAlignment, VerticalAlignment
from pygsheets.datarange import DataRange


class ReportGenerator:
    def __init__(self, sheet) -> None:
        self.client = pygsheets.authorize(
            service_file="striking-ensign-271319-aa930e7c5b50.json"
        )
        self.sht = self.client.open_by_key(sheet)

    def enable_batch(self, status):
        if not status:
            self.commit()

        self.client.set_batch_mode(status)

    def commit(self):
        self.client.run_batch()

    def get_wks_url(self):
        return self.wks.url

    def get_sht_url(self):
        return self.sht.url

    def create_worksheet(self, title, cols=26, rows=1000):
        wks = self.sht.add_worksheet(title, cols=cols, rows=rows)
        self.wks = wks
        return wks


class EventReportGenerator(ReportGenerator):
    columns = 4
    zeroCell = (1, 1)
    headeing_height = 2

    last_festival = datetime.date(2020, 12, 10)

    current_row = zeroCell[1]

    def find_accepted_year(self):
        eventDate = self.object.startDate.date()

        currentYear = datetime.datetime.now().year

        yearKoef = (
            2 if (self.last_festival < eventDate < datetime.date(2021, 7, 1)) else 1
        )
        self.acceptedYear = currentYear - yearKoef

    def create(self, event):
        self.object = event

        self.find_accepted_year()

        wks = self.create_worksheet(title=str(self.object), cols=self.columns)

        wks.adjust_column_width(1, None, 300)

        self.past_header(str(event.title), self.zeroCell)
        nextRow = self.current_row + 1

        participant = Boec.objects.filter(event_participation__event=event)

        volonteers = participant.filter(event_participation__worth=1)
        organizers = participant.filter(event_participation__worth=2)
        participants = participant.filter(event_participation__worth=0)

        info_values = [
            [["Штаб-организатор"], [event.shtab.title if event.shtab else "Без штаба"]],
            [["Волонтеров"], [volonteers.count()]],
            [["Организаторов"], [organizers.count()]],
            [["Блок"], [event.get_worth_display()]],
        ]
        self.past_info_cells(nextRow, info_values)
        nextRow = self.current_row + 2

        self.past_header("Организаторы", (nextRow, self.zeroCell[1]))
        nextRow = self.current_row + 1
        self.past_boec(nextRow, organizers, 2)
        nextRow = self.current_row + 2

        self.past_header("Волонтеры", (nextRow, self.zeroCell[1]))
        nextRow = self.current_row + 1
        self.past_boec(nextRow, volonteers, 1)
        nextRow = self.current_row + 2

        self.past_header("Участники", (nextRow, self.zeroCell[1]))
        nextRow = self.current_row + 1
        self.past_boec(nextRow, participants, 0)

        self.wks.rows = self.current_row

        url = self.get_wks_url()
        return url

    def past_boec(self, nextRow, queryset, worth=0):
        params = queryset.values_list("id", "lastName", "firstName", "middleName")

        data = []
        for boec in params:
            fullName = f"{boec[1]} {boec[2]} {boec[3]}"
            lastSeason = Season.objects.filter(boec=boec[0]).order_by("year").first()
            isAccepted = worth == 0 or lastSeason.year >= self.acceptedYear
            row = [
                fullName,
                lastSeason.brigade.title,
                lastSeason.year,
                isAccepted,
            ]

            data.append(row)

        if len(data) != 0:
            self.enable_batch(True)
            style_cell = Cell((nextRow, self.zeroCell[1]), worksheet=self.wks)
            self.set_info_styles(style_cell)

            style_range = DataRange(
                start=(nextRow, self.zeroCell[1]),
                end=(nextRow + len(data) - 1, self.zeroCell[1] + self.columns - 1),
                worksheet=self.wks,
            )
            style_range.apply_format(style_cell)
            self.enable_batch(False)
            self.wks.update_values_batch(
                ranges=[
                    (
                        (nextRow, self.zeroCell[1]),
                        (nextRow + len(data) - 1, self.zeroCell[1] + self.columns - 1),
                    )
                ],
                values=[data],
                majordim="ROWS",
            )
            self.wks.set_data_validation(
                start=(nextRow, self.zeroCell[1] + self.columns - 1),
                end=(nextRow + len(data) - 1, self.zeroCell[1] + self.columns - 1),
                condition_type="BOOLEAN",
            )

            self.current_row = style_range.end_addr[0]

    def past_info_cells(self, nextRow, values):
        style_cell = Cell((nextRow, self.zeroCell[1]), worksheet=self.wks)

        self.enable_batch(True)

        self.set_info_styles(style_cell)

        style_range = DataRange(
            start=(style_cell.row, style_cell.col),
            end=(style_cell.row + len(values) - 1, style_cell.col + self.columns - 1),
            worksheet=self.wks,
        )
        style_range.apply_format(style_cell)

        ranges = []
        for index, _ in enumerate(values):
            info_cell = Cell(
                (style_cell.row + index, style_cell.col + 1), worksheet=self.wks
            )

            value_range = DataRange(
                start=(info_cell.row, info_cell.col),
                end=(info_cell.row, info_cell.col + self.columns - 2),
                worksheet=self.wks,
            )
            value_range.merge_cells("MERGE_ALL")

            ranges.append(
                [
                    (style_cell.row + index, style_cell.col),
                    (info_cell.row, info_cell.col),
                ]
            )

            self.current_row = style_cell.row + index

        self.enable_batch(False)

        self.wks.update_values_batch(ranges=ranges, values=values, majordim="COLUMNS")

    def past_header(self, title, zeroCell):
        self.enable_batch(True)

        style_cell = Cell(zeroCell, worksheet=self.wks)
        self.set_header_styles(style_cell)

        drange = DataRange(
            start=zeroCell,
            end=(
                zeroCell[0] + self.headeing_height - 1,
                zeroCell[1] + self.columns - 1,
            ),
            worksheet=self.wks,
        )
        drange.merge_cells("MERGE_ALL")
        drange.apply_format(style_cell)

        self.enable_batch(False)

        style_cell.value = title

        self.current_row = drange.end_addr[0]

    def set_header_styles(self, cell):
        cell.set_horizontal_alignment(HorizontalAlignment.CENTER)
        cell.set_vertical_alignment(VerticalAlignment.MIDDLE)
        cell.wrap_strategy = "OVERFLOW_CELL"
        cell.set_text_format("fontFamily", "Roboto")
        cell.set_text_format("fontSize", 14)
        cell.set_text_format("bold", True)
        cell.borders = {
            "top": {"style": "SOLID_THICK"},
            "bottom": {"style": "SOLID_THICK"},
            "left": {"style": "SOLID_THICK"},
            "right": {"style": "SOLID_THICK"},
        }
        cell.color = (0.937, 0.937, 0.937, 1)

    def set_info_styles(self, cell):
        cell.set_horizontal_alignment(HorizontalAlignment.CENTER)
        cell.set_vertical_alignment(VerticalAlignment.MIDDLE)
        cell.wrap_strategy = "OVERFLOW_CELL"
        cell.set_text_format("fontFamily", "Roboto")

        cell.borders = {
            "top": {"style": "SOLID"},
            "bottom": {"style": "SOLID"},
            "left": {"style": "SOLID"},
            "right": {"style": "SOLID"},
        }
        # color is required for border
        cell.color = (1, 1, 1, 1)


logger = logging.getLogger(__name__)


class EventsRatingGenerator(ReportGenerator):

    last_festival = datetime.datetime(2020, 12, 10, tzinfo=pytz.UTC)
    cursor = 1
    header_height = 2

    def check_is_accepted(self, worth, year, eventDate):

        currentYear = datetime.datetime.now().year

        yearKoef = (
            2
            if (
                self.last_festival.date() < eventDate < datetime.date(2021, 7, 1)
                and worth == 1
            )
            else 1
        )
        acceptedYear = currentYear - yearKoef

        if worth != 0:
            return year >= acceptedYear

        return True

    def create(self):
        self.events = Event.objects.filter(startDate__gte=self.last_festival)

        conference = Conference.objects.last()
        self.brigades = (
            conference.brigades.all()
            .order_by("area", "title")
            .values_list("id", "title")
        )

        rows = len(self.brigades) + self.header_height

        for value, text in EventWorth.choices:
            events_by_worth = self.events.filter(worth=value)

            if events_by_worth.count() == 0:
                continue

            self.cursor = 2

            wks = self.create_worksheet(title=str(text), rows=rows)

            wks.frozen_cols = 1
            wks.frozen_rows = 2

            self.createFirstColumn(wks=wks)

            self.render_events(events=events_by_worth, worth=value, wks=wks)

        url = self.get_sht_url()
        return url

    def createFirstColumn(self, wks):
        self.enable_batch(True)

        zeroCoords = (1, 1)
        style_cell = Cell(zeroCoords, worksheet=wks)
        self.set_header_styles(style_cell)

        drange = DataRange(
            start=zeroCoords,
            end=(
                zeroCoords[0] + self.header_height - 1,
                zeroCoords[1],
            ),
            worksheet=self.wks,
        )
        drange.apply_format(style_cell)

        brigade_zeroCoords = (self.header_height + 1, 1)
        brigade_cell = Cell(brigade_zeroCoords, worksheet=wks)
        self.set_brigade_style(brigade_cell)

        drange = DataRange(
            start=brigade_zeroCoords,
            end=(
                brigade_zeroCoords[0] + len(self.brigades) - 1,
                brigade_zeroCoords[1],
            ),
            worksheet=self.wks,
        )
        drange.apply_format(brigade_cell)

        wks.adjust_row_height(1, None, 50)
        wks.adjust_row_height(2, self.header_height, 75)
        wks.adjust_column_width(1, None, 200)

        self.enable_batch(False)

        values = [
            [["Название мероприятия", "Участник/статус"]],
        ]

        brigades_titles = [brigade[1] for brigade in self.brigades]

        ranges = [
            (zeroCoords, (zeroCoords[0] + self.header_height - 1, zeroCoords[1])),
            (
                brigade_zeroCoords,
                (brigade_zeroCoords[0] + len(self.brigades) - 1, brigade_zeroCoords[1]),
            ),
        ]

        values.append([brigades_titles])
        self.wks.update_values_batch(ranges=ranges, values=values, majordim="COLUMNS")

    def set_header_styles(self, cell):
        cell.set_horizontal_alignment(HorizontalAlignment.CENTER)
        cell.set_vertical_alignment(VerticalAlignment.MIDDLE)
        cell.wrap_strategy = "OVERFLOW_CELL"
        cell.set_text_format("fontFamily", "Roboto")
        cell.set_text_format("fontSize", 12)
        cell.borders = {
            "top": {"style": "SOLID"},
            "bottom": {"style": "SOLID"},
            "left": {"style": "SOLID"},
            "right": {"style": "SOLID"},
        }
        cell.color = (0.9882352941176471, 0.8980392156862745, 0.803921568627451, 1)

    def set_brigade_style(self, cell):
        cell.set_horizontal_alignment(HorizontalAlignment.LEFT)
        cell.set_vertical_alignment(VerticalAlignment.MIDDLE)
        cell.wrap_strategy = "OVERFLOW_CELL"
        cell.set_text_format("fontFamily", "Roboto")
        cell.set_text_format("fontSize", 12)
        cell.borders = {
            "top": {"style": "SOLID"},
            "bottom": {"style": "SOLID"},
            "left": {"style": "SOLID"},
            "right": {"style": "SOLID"},
        }
        cell.color = (0.8509803921568627, 0.9176470588235294, 0.8274509803921569, 1)

    def set_data_style(self, cell):
        cell.set_horizontal_alignment(HorizontalAlignment.CENTER)
        cell.set_vertical_alignment(VerticalAlignment.MIDDLE)
        cell.wrap_strategy = "OVERFLOW_CELL"
        cell.set_text_format("fontFamily", "Roboto")
        cell.set_text_format("fontSize", 12)
        cell.borders = {
            "top": {"style": "SOLID"},
            "bottom": {"style": "SOLID"},
            "left": {"style": "SOLID"},
            "right": {"style": "SOLID"},
        }
        cell.color = (1, 1, 1, 1)

    def get_columns(self, worth):

        values = [
            # не учитываются
            ["Волонтеры", "Организаторы"],
            # творчество
            [
                "Волонтеры",
                "Организаторы",
                "Подача заявки",
                "Участие в конкурсной программе",
                "Победа в номинации",
            ],
            # спорт
            [
                "Волонтеры",
                "Организаторы",
                "Участие в соревновании",
                "Выход в плей-офф",
                "Победа",
            ],
            # волонтерство
            ["Волонтеры", "Организаторы", "Участие"],
            # городские
            ["Волонтеры", "Организаторы"],
        ]

        return values[worth]

    def render_events(self, events, worth, wks):
        columns = self.get_columns(worth=worth)

        # форматирование
        self.enable_batch(True)

        zeroCoords = (1, 2)
        style_cell = Cell(zeroCoords, worksheet=wks)
        self.set_header_styles(style_cell)

        drange = DataRange(
            start=zeroCoords,
            end=(
                zeroCoords[0] + self.header_height - 1,
                zeroCoords[1] + (len(events) * len(columns)) - 1,
            ),
            worksheet=self.wks,
        )
        drange.apply_format(style_cell)

        data_zeroCoords = (self.header_height + 1, 2)
        data_cell = Cell(data_zeroCoords, worksheet=wks)
        self.set_data_style(data_cell)

        drange = DataRange(
            start=data_zeroCoords,
            end=(
                data_zeroCoords[0] + len(self.brigades) - 1,
                data_zeroCoords[1] + (len(events) * len(columns)) - 1,
            ),
            worksheet=self.wks,
        )
        drange.apply_format(data_cell)
        wks.adjust_column_width(
            data_zeroCoords[1],
            data_zeroCoords[1] + (len(events) * len(columns)) - 1,
            150,
        )

        self.enable_batch(False)

        # значения

        ranges = []
        values = []

        self.enable_batch(True)
        for event in events:

            title_range = DataRange(
                start=(1, self.cursor),
                end=(1, self.cursor + len(columns) - 1),
                worksheet=self.wks,
            )
            title_range.merge_cells("MERGE_ALL")

            ranges.append([(1, self.cursor), (1, self.cursor + len(columns) - 1)])
            ranges.append([(2, self.cursor), (2, self.cursor + len(columns) - 1)])
            title_values = [""] * len(columns)
            title_values[0] = event.title

            values.append([title_values])
            values.append([columns])

            data = {}
            event_participants = event.participant.all()

            eventDate = event.startDate.date()

            for participant in event_participants:
                boec_last_season = (
                    Season.objects.filter(boec=participant.boec)
                    .order_by("year")
                    .first()
                )
                is_accepted = self.check_is_accepted(
                    worth=participant.worth,
                    year=boec_last_season.year,
                    eventDate=eventDate,
                )
                if not is_accepted:
                    continue

                brigade_id = boec_last_season.brigade.id

                if brigade_id not in data:
                    data[brigade_id] = [""] * len(columns)

                data[brigade_id][participant.worth] = (
                    data[brigade_id][participant.worth]
                    if data[brigade_id][participant.worth] != ""
                    else 0
                ) + 1

            brigades_ids = [brigade[0] for brigade in self.brigades]

            for key, value in data.items():
                try:
                    current_index = brigades_ids.index(key)
                except:
                    continue
                values.append([value])

                row = self.header_height + current_index + 1
                ranges.append(
                    [(row, self.cursor), (row, self.cursor + len(columns) - 1)]
                )

            self.cursor = self.cursor + len(columns) - 1
        self.enable_batch(False)

        self.wks.update_values_batch(ranges=ranges, values=values, majordim="ROWS")
