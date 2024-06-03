from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest

from core.config.dev_settings import ADMIN_PAGE_ORDERING
from main.admin.inlines import (
    DocumentInline,
    PlayerInline,
    PlayerTeamInline,
    StaffTeamMemberTeamInline,
)
from main.forms import PlayerForm, TeamForm


class CityAdmin(admin.ModelAdmin):
    """Модель городов для административной панели Django."""

    list_display = ("pk", "name")
    search_fields = ("name",)
    ordering = ["name"]


class NosologyAdmin(admin.ModelAdmin):
    """Модель нозологий для административной панели Django."""

    list_display = ("pk", "name")
    search_fields = ("name",)
    ordering = ["name"]


class DiagnosisAdmin(admin.ModelAdmin):
    """Модель диагнозов для административной панели Django."""

    list_display = ("pk", "name", "nosology")
    search_fields = (
        "pk",
        "name",
        "nosology__name",
    )
    ordering = ["name"]


class DisciplineNameAdmin(admin.ModelAdmin):
    """Модель дисциплин для административной панели Django."""

    list_display = ("pk", "name")
    search_fields = ("name",)
    ordering = ["name"]


class DisciplineLevelAdmin(admin.ModelAdmin):
    """Модель уровня дисциплин для административной панели Django."""

    list_display = ("pk", "name")
    search_fields = ("name",)
    ordering = ["name"]


class DocumentAdmin(admin.ModelAdmin):
    """Модель документов для административной панели Django."""

    list_display = ("pk", "name", "file")
    search_fields = (
        "name",
        "file",
    )
    ordering = ["name"]


class StaffMemberAdmin(admin.ModelAdmin):
    """Модель сотрудников для административной панели Django."""

    list_display = ("pk", "surname", "name", "patronymic", "phone")
    search_fields = (
        "pk",
        "surname",
        "name",
        "patronymic",
        "phone",
    )


class StaffTeamMemberAdmin(admin.ModelAdmin):
    """Модель сотрудников команд для административной панели Django."""

    list_display = (
        "pk",
        "staff_member",
        "staff_position",
        "qualification",
        "notes",
    )
    search_fields = (
        "pk",
        "staff_member__name",
        "staff_member__surname",
        "staff_member__patronymic",
        "staff_position",
        "qualification",
        "notes",
    )


class PlayerAdmin(admin.ModelAdmin):
    """Модель игрока для административной панели Django."""

    change_form_template = "admin/custom_change_form.html"
    form = PlayerForm
    list_display = (
        "pk",
        "surname",
        "name",
        "patronymic",
        "birthday",
        "gender",
        "get_nosology",
        "diagnosis",
        "discipline_name",
        "discipline_level",
        "level_revision",
        "position",
        "number",
        "is_captain",
        "is_assistent",
        "identity_document",
    )
    search_fields = (
        "pk",
        "surname",
        "name",
        "patronymic",
        "birthday",
        "gender",
        "diagnosis__nosology__name",
        "discipline_name__name",
        "discipline_level__name",
        "level_revision",
        "position",
        "number",
        "identity_document",
    )
    ordering = ["surname", "name", "patronymic", "birthday"]
    inlines = (
        PlayerInline,
        DocumentInline,
    )
    fieldsets = (
        (
            "Персональные данные",
            {
                "classes": ("collapse",),
                "fields": (
                    (
                        "surname",
                        "name",
                    ),
                    "patronymic",
                    (
                        "gender",
                        "birthday",
                    ),
                    "identity_document",
                    "discipline_name",
                    "discipline_level",
                    "nosology",
                    "diagnosis",
                    "level_revision",
                    "addition_date",
                ),
            },
        ),
        (
            "Игровые данные",
            {
                "classes": ("collapse",),
                "fields": (
                    "position",
                    (
                        "number",
                        "is_captain",
                        "is_assistent",
                    ),
                ),
            },
        ),
    )
    readonly_fields = ("addition_date",)
    list_filter = ("addition_date",)

    @admin.display(
        description="Нозология",
        ordering="diagnosis__nosology__name",
    )
    def get_nosology(self, obj):
        """Получить название нозологии."""
        return obj.diagnosis.nosology.name


class TeamAdmin(admin.ModelAdmin):
    """Модель команд для административной панели Django."""

    form = TeamForm
    change_form_template = "admin/custom_change_form.html"
    list_display = (
        "pk",
        "name",
        "city",
        "discipline_name",
    )
    search_fields = (
        "pk",
        "name",
        "city__name",
        "discipline_name__name",
    )
    ordering = ["name"]
    inlines = (
        StaffTeamMemberTeamInline,
        PlayerTeamInline,
    )


def get_app_list(
    self: AdminSite,
    request: HttpRequest,
    app_name: str = " ",
) -> list:
    app_dict = self._build_app_dict(request)
    app_list = []

    for app_name, app in app_dict.items():
        if app_name in ADMIN_PAGE_ORDERING:
            app["models"].sort(
                key=lambda model: ADMIN_PAGE_ORDERING[app_name].index(
                    model["object_name"],
                ),
            )
        app_list.append(app)

    return app_list


AdminSite.get_app_list = get_app_list
