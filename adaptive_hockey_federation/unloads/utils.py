import os
from typing import Any, List

from django.conf import settings
from django.db.models import QuerySet
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from .constants import (
    ALIGNMENT_CENTER,
    HEADERS_BORDER,
    HEADERS_FILL,
    HEADERS_FONT,
    HEADERS_HEIGHT,
    ROWS_FILL,
    TITLE_FILL,
    TITLE_FONT,
    TITLE_HEIGHT,
)


def column_width(workbook: Worksheet) -> None:
    for col in workbook.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        adjusted_width = max_length + 2
        workbook.column_dimensions[column].width = adjusted_width


def export_excel(queryset: QuerySet, filename: str, title: str) -> None:
    """Выгрузка данных в excel. После создания файла возвращает его имя."""
    wb = Workbook()
    del wb["Sheet"]
    ws: Worksheet = wb.create_sheet("Лист1")
    ws.append(['', title])

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

        ws.row_dimensions[1].fill = TITLE_FILL  # type: ignore
        ws.row_dimensions[1].height = TITLE_HEIGHT  # type: ignore
        ws.row_dimensions[1].font = TITLE_FONT  # type: ignore
        ws.row_dimensions[1].alignment = ALIGNMENT_CENTER  # type: ignore

        ws.row_dimensions[2].fill = HEADERS_FILL  # type: ignore
        ws.row_dimensions[2].height = HEADERS_HEIGHT  # type: ignore
        ws.row_dimensions[2].font = HEADERS_FONT  # type: ignore
        ws.row_dimensions[2].alignment = ALIGNMENT_CENTER  # type: ignore
        ws.row_dimensions[2].border = HEADERS_BORDER  # type: ignore

        number_rows = int(ws.dimensions.split(":")[1][1:])
        for i in range(3, number_rows, 2):
            ws.row_dimensions[i].fill = ROWS_FILL  # type: ignore

    media_data_path = os.path.join(settings.MEDIA_ROOT, "unloads_data")
    os.makedirs(media_data_path, exist_ok=True)
    file_path = os.path.join(media_data_path, filename)
    wb.save(file_path)


def letter_range(start: str, stop: str = "{", step=1):
    for ord_ in range(ord(start.upper()), ord(stop.upper()), step):
        yield chr(ord_)
