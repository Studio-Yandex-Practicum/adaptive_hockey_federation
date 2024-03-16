import os
from typing import Any, List

from django.db.models import QuerySet
from openpyxl import Workbook


def export_excel(queryset: QuerySet, filename: str, title: str) -> None:
    """Выгрузка данных в excel."""
    wb = Workbook()

    ws = wb.active

    if ws is None:
        ws = wb.create_sheet()

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
