from competitions.models import Competition
from django.contrib import admin


class CompetitionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
    )
    search_fields = ("title",)
    ordering = ["title"]


admin.site.register(Competition, CompetitionAdmin)
