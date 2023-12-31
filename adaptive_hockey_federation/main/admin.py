from django.contrib import admin
from main.models import (
    City,
    Diagnosis,
    Discipline,
    DisciplineLevel,
    DisciplineName,
    Document,
    Nosology,
    Player,
    StaffMember,
    StaffTeamMember,
    Team,
)


class CityAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )
    search_fields = ('name',)
    ordering = ['name']


class NosologyAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )
    search_fields = ('name',)
    ordering = ['name']


class DiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'nosology'
    )
    search_fields = (
        'pk', 'name', 'nosology',)
    ordering = ['name']


class DisciplineNameAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )
    search_fields = ('name',)
    ordering = ['name']


class DisciplineLevelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )
    search_fields = ('name',)
    ordering = ['name']


class DisciplineAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'discipline_name',
        'discipline_level'
    )
    search_fields = ('discipline_name', 'discipline_level',)
    ordering = ['discipline_name']


class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'file'
    )
    search_fields = ('name', 'file',)
    ordering = ['name']


class StaffMemberAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'surname',
        'name',
        'patronymic',
        'phone'
    )
    search_fields = ('pk', 'surname', 'name', 'patronymic', 'phone',)


class StaffTeamMemberAdmin(StaffMemberAdmin):
    list_display = (
        'pk',
        'staff_member',
        'staff_position',
        'qualification',
        'notes'
    )
    search_fields = (
        'pk',
        'staff_member',
        'staff_position',
        'qualification',
        'notes'
    )


class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'surname',
        'name',
        'patronymic',
        'birthday',
        'gender',
        'diagnosis',
        'discipline',
        'level_revision',
        'position',
        'number',
        'is_captain',
        'is_assistent',
        'identity_document',
    )
    search_fields = (
        'pk',
        'surname',
        'name',
        'patronymic',
        'birthday',
        'gender',
        'diagnosis',
        'discipline',
        'level_revision',
        'position',
        'number',
        'identity_document',
    )
    ordering = ['surname', 'name', 'patronymic', 'birthday']


class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'city',
        'staff_team_member',
        'discipline_name'
    )
    search_fields = (
        'pk',
        'name',
        'city',
        'staff_team_member',
        'discipline_name'
    )
    ordering = ['name']


admin.site.register(City, CityAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(DisciplineLevel, DisciplineLevelAdmin)
admin.site.register(DisciplineName, DisciplineNameAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Nosology, NosologyAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(StaffTeamMember, StaffTeamMemberAdmin)
admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.register(Team, TeamAdmin)
