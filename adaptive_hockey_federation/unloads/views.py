import os
from typing import Any
from urllib.parse import parse_qs, urlparse

from core.utils import export_excel
from django.apps import apps
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from unloads.mapping import model_mapping
from unloads.models import Unload
from unloads.utils import model_get_queryset


class UnloadListView(
    LoginRequiredMixin,
    ListView,
):
    """Список выгрузок."""

    # TODO: (Добавить пермишенны.)
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
    success_url = reverse_lazy("unloads:unloads")
    permission_required = "unloads.delete_unload"
    permission_denied_message = "Отсутствует разрешение на удаление выгрузки."

    def get_object(self, queryset=None):
        return get_object_or_404(Unload, id=self.kwargs["pk"])


class DataExportView(LoginRequiredMixin, View):
    """Выгрузка данных в Excel."""

    def get(self, request, *args, **kwargs):
        page_name = kwargs.get("page_name")
        if page_name in model_mapping:
            app_label, model_name, title = model_mapping[page_name]
            model = apps.get_model(app_label, model_name)
            last_url = request.META.get("HTTP_REFERER")
            parsed = urlparse(last_url)
            params = parse_qs(parsed.query)
            if len(params) > 0:
                queryset = model_get_queryset(page_name, model, params, None)
                filename = page_name + "_search.xlsx"
            else:
                queryset = model.objects.all()
                filename = page_name + "_all.xlsx"
            if model_name == "User":
                excluded_fields = ["id", "password", "is_active"]
                fields_order = [
                    "last_name",
                    "first_name",
                    "patronymic",
                    "email",
                    "phone",
                    "role",
                    "is_staff",
                    "date_joined",
                ]
            else:
                excluded_fields = []
                fields_order = []
            filename = export_excel(
                queryset, filename, title, excluded_fields, fields_order
            )
            file_slug = f"unloads_data/{filename}"

            unload_record = Unload(
                unload_name=filename,
                user=request.user,
                unload_file_slug=file_slug,
            )
            unload_record.save()

            file_path = os.path.join(
                settings.MEDIA_ROOT, "unloads_data", filename
            )
            if os.path.exists(file_path):
                file_unload = open(file_path, "rb")
                response = FileResponse(file_unload)
                response["Content-Disposition"] = (
                    f'attachment; filename="{filename}"'
                )
                return response
            else:
                raise FileNotFoundError("Файл для выгрузки не найден.")
        else:
            raise Exception("Для данной страницы выгрузка не предусмотрена.")
