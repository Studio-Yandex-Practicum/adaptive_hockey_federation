import os
from typing import Any
from urllib.parse import parse_qs, urlparse

from django.apps import apps
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from unloads.models import Unload
from unloads.utils import export_excel


class UnloadListView(
    LoginRequiredMixin,
    ListView,
):
    """Список выгрузок."""

    # TODO: (Добавить пермишенны.)
    # TODO: Реализовать удаление файлов с диска
    model = Unload
    template_name = "main/unloads/unloads.html"
    context_object_name = "unloads"
    paginate_by = 10
    ordering = ["date"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        unloads = context["unloads"]
        table_data = []
        for unload in unloads:
            table_data.append(
                {
                    "pk": unload.pk,
                    "date": unload.date,
                    "unload_name": unload.unload_name,
                    "user": unload.user,
                    "_ref_": {
                        "name": "Посмотреть/Excel",
                        "type": "button",
                        "url": (
                            f"{settings.MEDIA_URL}/{unload.unload_file_slug}"
                        ),
                    },
                }
            )
        context["table_head"] = {
            "pk": "Nr.",
            "date": "Дата",
            "unload_name": "Наименование",
            "user": "Автор",
            "unload_file_slug": "Просмотр/Excel",
        }
        context["table_data"] = table_data
        return context


class DeleteUnloadView(
    LoginRequiredMixin,
    DeleteView,
):
    """Удаление выгрузок."""

    object = Unload
    model = Unload
    success_url = reverse_lazy("main:unloads")
    permission_required = "main.delete_unload"
    permission_denied_message = "Отсутствует разрешение на удаление выгрузки."

    def get_object(self, queryset=None):
        return get_object_or_404(Unload, id=self.kwargs["pk"])


class DataExportView(LoginRequiredMixin, View):
    """Выгрузка данных в Excel."""

    # TODO: (Если требуется выгрузка других моделей,
    # нужно добавить их в словарь(model_mapping)
    # и дополнить шаблон base/footer.html.)
    model_mapping = {
        "players": ("main", "Player", "players_data.xlsx", "Данные игроков"),
        "teams": ("main", "Team", "teams_data.xlsx", "Данные команд"),
        "competitions": (
            "competitions",
            "Competition",
            "competitions_data.xlsx",
            "Данные соревнований",
        ),
    }

    def get(self, request, *args, **kwargs):
        page_name = kwargs.get("page_name")

        if page_name in self.model_mapping:
            app_label, model_name, filename, title = self.model_mapping[
                page_name
            ]
            model = apps.get_model(app_label, model_name)
            last_url = request.META.get('HTTP_REFERER')
            parsed = urlparse(last_url)
            params = parse_qs(parsed.query)
            if 'search' in params:
                search_column = ""
                # было search, сделал s т.к. 123 строка больше 80
                # как перенести не понял :-)
                s = parse_qs(parsed.query)['search'][0]
                if 'search_column' in params:
                    search_column = parse_qs(parsed.query)['search_column'][0]

                if (search_column == ""
                        or search_column.lower() in ["все", "all"]):
                    or_lookup = (
                        Q(surname__icontains=s)
                        | Q(name__icontains=s)
                        | Q(birthday__icontains=s)
                        | Q(gender__icontains=s)
                        | Q(number__icontains=s)
                        | Q(discipline__discipline_name_id__name__icontains=s)
                        | Q(diagnosis__name__icontains=s)
                    )
                    queryset = model.objects.filter(or_lookup)
                else:
                    search_fields = {
                        "surname": "surname",
                        "name": "name",
                        "birthday": "birthday",
                        "gender": "gender",
                        "number": "surname",
                        "discipline": "discipline__discipline_name_id__name",
                        "diagnosis": "diagnosis__name",
                    }
                    lookup = {
                        f"{search_fields[search_column]}__icontains": s
                    }
                    queryset = model.objects.filter(**lookup)

                filename = "players_search.xlsx"
            else:
                queryset = model.objects.all()
                filename = "players_all.xlsx"

            export_excel(queryset, filename, title)
            file_slug = f"data/{filename}"

            unload_record = Unload(
                unload_name=filename,
                user=request.user,
                unload_file_slug=file_slug,
            )
            unload_record.save()

            file_path = os.path.join(settings.MEDIA_ROOT, "data", filename)
            if os.path.exists(file_path):
                file_unload = open(file_path, 'rb')
                response = FileResponse(file_unload)
                response["Content-Disposition"] = (
                    f'attachment; filename="{filename}"'
                )
                return response
            else:
                raise FileNotFoundError("Файл для выгрузки не найден.")
        else:
            raise Exception("Для данной страницы выгрузка не предусмотрена.")
