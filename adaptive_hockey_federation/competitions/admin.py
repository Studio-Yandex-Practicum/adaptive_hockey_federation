from django.contrib import admin
from competitions.models import Competition


class CompetitionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title'
    )
    search_fields = ('title',)
    ordering = ['title']


admin.site.register(Competition, CompetitionAdmin)
