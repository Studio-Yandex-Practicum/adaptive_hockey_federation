from django.contrib import admin
from main.forms import PlayerTeamForm, StaffTeamMemberTeamForm
from main.models import Document, Player, StaffTeamMember


class PlayerInline(admin.StackedInline):
    model = Player.team.through
    form = PlayerTeamForm
    insert_after = "position"
    verbose_name = "Команда"
    verbose_name_plural = "Участие в командах"
    extra = 0
    min_num = 1
    template = "admin/custom_stacked.html"


class PlayerTeamInline(PlayerInline):
    insert_after = ""
    verbose_name = "Игрок"
    verbose_name_plural = "Игроки команды"
    classes = ("collapse",)


class DocumentInline(admin.TabularInline):
    model = Document
    verbose_name = "Документ"
    verbose_name_plural = "Документы"
    extra = 0
    min_num = 1


class StaffTeamMemberTeamInline(admin.StackedInline):
    model = StaffTeamMember.team.through
    form = StaffTeamMemberTeamForm
    verbose_name = "Сотрудник"
    verbose_name_plural = "Административый состав команды"
    classes = ("collapse",)
    extra = 0
    min_num = 1
    template = "admin/custom_stacked.html"
