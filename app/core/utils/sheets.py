import datetime

import pygsheets
from core.models import Boec, Season
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

        wks = self.create_worksheet()

        wks.adjust_column_width(1, None, 300)

        self.past_header(str(event.title), self.zeroCell)
        nextRow = self.current_row + 1

        participant = Boec.objects.filter(event_participation__event=event)

        volonteers = participant.filter(event_participation__worth=1)
        organizers = participant.filter(event_participation__worth=2)

        info_values = [
            [["Штаб-организатор"], [event.shtab.title]],
            [["Волонтеров"], [volonteers.count()]],
            [["Организаторов"], [organizers.count()]],
            [["Блок"], [event.get_worth_display()]],
        ]
        self.past_info_cells(nextRow, info_values)
        nextRow = self.current_row + 2

        self.past_header("Организаторы", (nextRow, self.zeroCell[1]))
        nextRow = self.current_row + 1
        self.past_boec(nextRow, organizers)
        nextRow = self.current_row + 2

        self.past_header("Волонтеры", (nextRow, self.zeroCell[1]))
        nextRow = self.current_row + 1
        self.past_boec(nextRow, volonteers)

        url = self.get_wks_url()
        return url

    def past_boec(self, nextRow, queryset):
        params = queryset.values_list("id", "lastName", "firstName", "middleName")

        data = []
        for boec in params:
            fullName = f"{boec[1]} {boec[2]} {boec[3]}"
            lastSeason = Season.objects.filter(boec=boec[0]).order_by("year").first()
            isAccepted = lastSeason.year >= self.acceptedYear
            row = [
                [fullName],
                [lastSeason.brigade.title],
                [lastSeason.year],
                [isAccepted],
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
                values=data,
                majordim="COLUMNS",
            )
            self.wks.set_data_validation(
                start=(nextRow, self.zeroCell[1] + self.columns - 1),
                end=(nextRow + len(data) - 1, self.zeroCell[1] + self.columns - 1),
                condition_type="BOOLEAN",
            )

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
            "top": {
                "style": "SOLID_THICK",
            },
            "bottom": {
                "style": "SOLID_THICK",
            },
            "left": {
                "style": "SOLID_THICK",
            },
            "right": {
                "style": "SOLID_THICK",
            },
        }
        cell.color = (0.937, 0.937, 0.937, 1)

    def set_info_styles(self, cell):
        cell.set_horizontal_alignment(HorizontalAlignment.CENTER)
        cell.set_vertical_alignment(VerticalAlignment.MIDDLE)
        cell.wrap_strategy = "OVERFLOW_CELL"
        cell.set_text_format("fontFamily", "Roboto")

        cell.borders = {
            "top": {
                "style": "SOLID",
            },
            "bottom": {
                "style": "SOLID",
            },
            "left": {
                "style": "SOLID",
            },
            "right": {
                "style": "SOLID",
            },
        }
        # color is required for border
        cell.color = (1, 1, 1, 1)

    def get_wks_url(self):
        return self.wks.url

    def create_worksheet(self):
        wks = self.sht.add_worksheet(str(self.object), cols=self.columns)
        self.wks = wks
        return wks
