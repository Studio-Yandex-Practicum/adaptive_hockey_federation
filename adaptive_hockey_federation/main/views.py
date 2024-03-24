import os

from competitions.models import Competition
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render
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
    # TODO: Нужно изменить функцию Выгрузки,
    # чтоб ее работа соотвествовала тех. заданию
    queryset = Competition.objects.all()
    filename = "data.xlsx"
    title = "Данные соревнований"
    export_excel(queryset, filename, title)
    file_path = os.path.join(settings.MEDIA_ROOT, "data", filename)
    file = open(file_path, "rb")
    response = FileResponse(file)
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(
        filename
    )
    return response
