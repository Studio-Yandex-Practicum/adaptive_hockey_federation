from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render
from events.models import Event
from unloads.utils import export_excel


@login_required
def main(request):
    return render(request, "main/home/main.html")


@login_required
def unloads(request):
    """
    Функция времена изменена для теста обработчика.
    Возвращается файл excel с данными Event.
    """
    queryset = Event.objects.all()
    filename = "data.xlsx"
    export_excel(queryset, filename)
    file = open(filename, "rb")
    response = FileResponse(file)
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(
        filename
    )
    return response
