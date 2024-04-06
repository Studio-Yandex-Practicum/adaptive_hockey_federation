import os
from typing import Any, List

from django.conf import settings
from django.db.models import QuerySet
from openpyxl import Workbook
from openpyxl.styles import Border, Font, PatternFill, Side
from openpyxl.worksheet.worksheet import Worksheet


def column_width(workbook: Worksheet) -> None:
    for col in workbook.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        adjusted_width = (max_length + 2) * 1.2
        adjusted_width = max_length
        workbook.column_dimensions[column].width = adjusted_width


def export_excel(queryset: QuerySet, filename: str, title: str) -> None:
    """Выгрузка данных в excel. После создания файла возвращает его имя."""
    wb = Workbook()
    del wb["Sheet"]
    ws: Worksheet = wb.create_sheet("Лист1")
    ws.append([title])

    if queryset:
        headers = []
        fields = []
        for field in queryset.model._meta.fields:
            headers.append(str(field.verbose_name))
            fields.append(field.name)

        ws.append(headers)

        for obj in queryset:
            row: List[Any] = []
            for field in fields:
                value = getattr(obj, field)
                if hasattr(value, "__str__"):
                    value = value.__str__()
                row.append(value)
            ws.append(row)

        column_width(ws)

        font_title = Font(
            name="Calibri",
            size=14,
            bold=True,
            italic=False,
            vertAlign=None,
            underline="none",
            strike=False,
            color="ffffff",
        )
        fill_title = PatternFill(patternType="solid", fgColor="729fcf")
        ws.merge_cells("A1:O1")
        ws["A1"].font = font_title
        ws["A1"].fill = fill_title

        font_headers = Font(
            name="Calibri",
            size=12,
            bold=True,
            italic=True,
            vertAlign=None,
            underline="none",
            strike=False,
            color="729fcf",
        )
        fill_headers = PatternFill(patternType="solid", fgColor="ffffff")

        style_headers = Side(border_style="thin", color="000000")
        border_headers = Border(
            top=style_headers,
            bottom=style_headers,
            left=style_headers,
            right=style_headers,
        )

        list_letter = list(letter_range("A", "P"))
        for letter in list_letter:
            ws[letter + "2"].font = font_headers
            ws[letter + "2"].fill = fill_headers
            ws[letter + "2"].border = border_headers

        fill_rows = PatternFill(patternType="solid", fgColor="dee6ef")
        number_rows = int(ws.dimensions.split(":")[1][1:])
        for i in range(3, number_rows, 2):
            for letter in list_letter:
                ws[letter + str(i)].fill = fill_rows

    media_data_path = os.path.join(settings.MEDIA_ROOT, "unloads_data")
    os.makedirs(media_data_path, exist_ok=True)
    file_path = os.path.join(media_data_path, filename)
    wb.save(file_path)


def letter_range(start: str, stop: str = "{", step=1):
    for ord_ in range(ord(start.upper()), ord(stop.upper()), step):
        yield chr(ord_)
