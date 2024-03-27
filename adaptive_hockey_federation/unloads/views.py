import os
from typing import Any

from django.apps import apps
from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import FileResponse
from django.utils.timezone import now
from django.views import View
from django.views.generic.list import ListView
from unloads.models import Unload
from unloads.utils import export_excel


class UnloadListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    """Список выгрузок."""

    model = Unload
    template_name = "main/unloads/unloads.html"
    permission_required = "unloads.list_view_unload"
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
            queryset = model.objects.all()

            export_excel(queryset, filename, title)

            timestamp = now().strftime("%Y%m%d%H%M%S")
            base_filename, file_extension = os.path.splitext(filename)
            file_slug = f"data/{base_filename}_{timestamp}{file_extension}"

            unload_record = Unload(
                unload_name=filename,
                user=request.user,
                unload_file_slug=file_slug,
            )
            unload_record.save()

            file_path = os.path.join(settings.MEDIA_ROOT, "data", filename)
            if os.path.exists(file_path):
                response = FileResponse(file_path)
                response["Content-Disposition"] = (
                    f'attachment; filename="{filename}"'
                )
                return response
            else:
                raise FileNotFoundError("Файл для выгрузки не найден.")
        else:
            raise Exception("Для данной страницы выгрузка не предусмотрена.")
