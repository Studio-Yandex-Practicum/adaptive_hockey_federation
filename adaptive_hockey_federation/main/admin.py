from django.contrib import admin
from main.models import (
    City,
    Competition,
    Diagnosis,
    Discipline,
    Gender,
    Player,
    PlayerTeam,
    Position,
    Qualification,
    Team,
    TeamCompetition,
    Trainer,
    TrainerTeam,
)


class PlayerInline(admin.TabularInline):
    model = PlayerTeam


class TrainerInline(admin.TabularInline):
    model = TrainerTeam


class CityAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )
    search_fields = ('name',)


class GenderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )
    search_fields = ('name',)


class DisciplineAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )
    search_fields = ('name',)


class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )
    search_fields = ('name',)


class QualificationAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )
    search_fields = ('name',)


class TrainerTeamAdmin(admin.ModelAdmin):
    list_display = (
        'trainer',
        'team',
    )
    search_fields = ('trainer', 'team',)


class TrainerAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'surname',
        'name',
        'patronymic',
        'description',
    )
    search_fields = ('pk', 'surname', 'name', 'patronymic', 'description',)


class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'surname',
        'name',
        'patronymic',
        'date_of_birth',
        'diagnosis',
        'gender',
        'identification_card',
    )
    search_fields = (
        'pk',
        'surname',
        'name',
        'patronymic',
        'date_of_birth',
        'diagnosis',
        'gender',
        'identification_card',
    )


class DiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'class_name',
        'is_wheeled',
        'description',
    )
    search_fields = (
        'pk', 'class_name', 'description',)


class PlayerTeamAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'player',
        'team',
        'qualification',
        'number',
        'is_captain',
        'is_assistent',
    )
    search_fields = (
        'pk', 'player', 'team', 'qualification',)


class CompetitionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'city',
        'number',
        'date',
        'duration',
        'is_active',
    )
    search_fields = (
        'pk', 'city', 'number', 'duration',)
    list_filter = ('date',)


class TeamCompetitionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'team',
        'competition',
    )
    search_fields = (
        'pk', 'team', 'competition',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'city',
        'discipline',
        'composition',
        'age',
        'pk',
    )
    search_fields = [
        'pk', 'name', 'city', 'discipline', 'composition', 'age']
    autocomplete_fields = ['city', 'discipline']
    inlines = [PlayerInline, TrainerInline]


admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Position, PositionAdmin)
# admin.site.register(Team, TeamAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(PlayerTeam, PlayerTeamAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(TrainerTeam, TrainerTeamAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(TeamCompetition, TeamCompetitionAdmin)
