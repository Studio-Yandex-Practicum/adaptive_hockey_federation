import os
from typing import Any, List

from django.db.models import QuerySet
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
    os.makedirs("data", exist_ok=True)
    filename = os.path.join("data", filename)
    wb.save(filename)
