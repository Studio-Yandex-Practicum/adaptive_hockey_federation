from django.contrib import admin

from main.forms import PlayerTeamForm, StaffTeamMemberTeamForm
from main.models import Document, Player, StaffTeamMember


class PlayerInline(admin.StackedInline):
    """Inline-класс для отображения игрока в админке."""

    model = Player.team.through
    form = PlayerTeamForm
    insert_after = "position"
    verbose_name = "Команда"
    verbose_name_plural = "Участие в командах"
    extra = 0
    min_num = 1
    template = "admin/custom_stacked.html"


class PlayerTeamInline(PlayerInline):
    """Inline-класс для отображения игрока команды в админке."""

    insert_after = ""
    verbose_name = "Игрок"
    verbose_name_plural = "Игроки команды"
    classes = ("collapse",)


class DocumentInline(admin.TabularInline):
    """Inline-класс для отображения документа в админке."""

    model = Document
    verbose_name = "Документ"
    verbose_name_plural = "Документы"
    extra = 0
    min_num = 1


class StaffTeamMemberTeamInline(admin.StackedInline):
    """Inline-класс для отображения сотрудника команды в админке."""

    model = StaffTeamMember.team.through
    form = StaffTeamMemberTeamForm
    verbose_name = "Сотрудник"
    verbose_name_plural = "Административый состав команды"
    classes = ("collapse",)
    extra = 0
    min_num = 1
    template = "admin/custom_stacked.html"
