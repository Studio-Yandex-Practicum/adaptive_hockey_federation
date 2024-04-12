import os
from datetime import datetime

from django.db.models import QuerySet
from openpyxl import Workbook

from core.constants import (
    FILE_RESOLUTION,
    MAX_UPLOAD_SIZE,
    TIME_FORMAT,
    MAX_AGE_PlAYER,
    MIN_AGE_PlAYER,
)
from django.core.files.uploadedfile import InMemoryUploadedFile
from core.settings.openpyxl_settings import (
    ALIGNMENT_CENTER,
    HEADERS_BORDER,
    HEADERS_FILL,
    HEADERS_FONT,
    HEADERS_HEIGHT,
    ROWS_FILL,
    TITLE_FILL,
    TITLE_FONT,
    TITLE_HEIGHT
)

from openpyxl.worksheet.worksheet import Worksheet
from typing import Any, List
from django.conf import settings


def generate_file_name(filename: str, prefix: str) -> str:
    filename, file_extension = os.path.splitext(filename)
    return (
        f"{prefix}-{datetime.now().strftime(TIME_FORMAT)}" f"{file_extension}"
    )


def is_uploaded_file_valid(file: InMemoryUploadedFile) -> bool:
    if (
        file.content_type
        and file.size
        and file.content_type.split("/")[1] in FILE_RESOLUTION
        and file.size <= MAX_UPLOAD_SIZE
    ):
        return True
    return False


def min_date():
    now = datetime.now()
    month_day = format(now.strftime("%m-%d"))
    return f"{str(now.year - MAX_AGE_PlAYER)}-{month_day}"


def max_date():
    now = datetime.now()
    month_day = format(now.strftime("%m-%d"))
    return f"{str(now.year - MIN_AGE_PlAYER)}-{month_day}"

def column_width(workbook: Worksheet) -> None:
    for col in workbook.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        adjusted_width = max_length + 2
        workbook.column_dimensions[column].width = adjusted_width

def export_excel(queryset: QuerySet, filename: str, title: str) -> str:
    """Выгрузка данных в excel (формат xlsx).
    После создания файла возвращает его имя."""
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
                if type(value)==bool:
                    value = 'Да' if value == True else 'Нет'
                else:
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

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base_filename, file_extension = os.path.splitext(filename)
    filename_with_timestamp = f"{base_filename}_{timestamp}{file_extension}"
    file_path = os.path.join(media_data_path, filename_with_timestamp)
    wb.save(file_path)

    return filename_with_timestamp