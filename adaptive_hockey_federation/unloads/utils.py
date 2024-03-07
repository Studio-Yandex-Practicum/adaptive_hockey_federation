from openpyxl import Workbook


def export_excel(queryset, filename):
    """Выгрузка данных в excel."""
    wb = Workbook()

    ws = wb.active

    if queryset:
        headers = [field.name for field in queryset.model._meta.fields]
        ws.append(headers)

        for obj in queryset:
            row = []
            for field in headers:
                value = getattr(obj, field)
                if hasattr(value, "__str__"):
                    value = value.__str__()
                row.append(value)
            ws.append(row)
    wb.save(filename)
