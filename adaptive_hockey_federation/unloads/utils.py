import os
from typing import Any, List

from django.conf import settings
from django.db.models import QuerySet
from django.utils.timezone import now
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


def export_excel(queryset: QuerySet, filename: str, title: str) -> None:
    """Выгрузка данных в excel."""
    wb = Workbook()
    del wb["Sheet"]
    ws: Worksheet = wb.create_sheet("Лист1")

    ws.append([title])

    if queryset:
        headers = [field.name for field in queryset.model._meta.fields]
        ws.append(headers)

        for obj in queryset:
            row: List[Any] = []
            for field in headers:
                value = getattr(obj, field)
                if hasattr(value, "__str__"):
                    value = value.__str__()
                row.append(value)
            ws.append(row)
    timestamp = now().strftime("%Y%m%d%H%M%S")
    base_filename, file_extension = os.path.splitext(filename)
    filename_with_timestamp = f"{base_filename}_{timestamp}{file_extension}"

    media_data_path = os.path.join(settings.MEDIA_ROOT, "unloads_data")
    os.makedirs(media_data_path, exist_ok=True)
    file_path = os.path.join(media_data_path, filename_with_timestamp)
    wb.save(file_path)
