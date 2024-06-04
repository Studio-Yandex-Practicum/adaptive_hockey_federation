from django.contrib import admin

from unloads.models import Unload


class UnloadAdmin(admin.ModelAdmin):
    """Админка для модели Выгрузки."""

    list_display = ("unload_name", "date", "user", "unload_file_slug")
    search_fields = ("name",)
    ordering = ["date"]


admin.site.register(Unload, UnloadAdmin)
