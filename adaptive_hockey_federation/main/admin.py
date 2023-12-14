from django.contrib import admin
from main.models import (
    Anamnesis,
    Discipline,
    Health,
    Location,
    Player,
    Position,
    RespiratoryFailure,
    Role,
    Team,
)


class TeamInline(admin.TabularInline):
    model = Team.players.through
    extra = 0
    verbose_name = 'Команда'
    verbose_name_plural = 'Команды'
    autocomplete_fields = ['team']


class HealthInline(admin.TabularInline):
    model = Health
    extra = 0
    verbose_name = 'Медицинская карта'
    verbose_name_plural = 'Медицинская карта'


class PlayerInline(admin.TabularInline):
    model = Player.team.through
    extra = 0
    verbose_name = 'Игрок'
    verbose_name_plural = 'Игроки'
    autocomplete_fields = ['player']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    inlines = [TeamInline, HealthInline]
    fields = ['name', 'surname', 'patronymic', 'birth_date']
    list_display = ['name', 'surname']
    search_fields = ['surname', 'name']


@admin.register(Anamnesis)
class AnamnesisAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """Прячем из меню админки данную модель"""
        return {}


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """Прячем из меню админки данную модель"""
        return {}


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['location', 'discipline']
    inlines = [PlayerInline]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """Прячем из меню админки данную модель"""
        return {}


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """Прячем из меню админки данную модель"""
        return {}


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """Прячем из меню админки данную модель"""
        return {}


@admin.register(RespiratoryFailure)
class RespiratoryFailureAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """Прячем из меню админки данную модель"""
        return {}
