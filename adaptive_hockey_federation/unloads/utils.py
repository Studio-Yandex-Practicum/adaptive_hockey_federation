import os
from typing import Any, List

from django.conf import settings
from django.db.models import QuerySet
from django.utils.timezone import now
from openpyxl import Workbook
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


def export_excel(queryset: QuerySet, filename: str, title: str) -> str:
    """Выгрузка данных в excel. После создания файла возвращает его имя"""
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

    timestamp = now().strftime("%Y%m%d%H%M%S")
    base_filename, file_extension = os.path.splitext(filename)
    filename_with_timestamp = f"{base_filename}_{timestamp}{file_extension}"

    media_data_path = os.path.join(settings.MEDIA_ROOT, "data")
    os.makedirs(media_data_path, exist_ok=True)
    file_path = os.path.join(media_data_path, filename_with_timestamp)
    wb.save(file_path)

    return filename_with_timestamp
