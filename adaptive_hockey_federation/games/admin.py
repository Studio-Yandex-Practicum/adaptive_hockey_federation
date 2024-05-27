from django.contrib import admin
from games.models import Game, GameTeam


class GameTeamInline(admin.StackedInline):
    model = GameTeam
    extra = 2


class GameAdmin(admin.ModelAdmin):
    """Админка для модели Выгрузки."""

    inlines = [GameTeamInline]
    list_display = ("name", "video_link", "get_teams")
    search_fields = ("name",)
    ordering = ["name"]

    def get_teams(self, obj):
        return ", ".join([team.name for team in obj.teams.all()])
    get_teams.short_description = "Teams"  # type: ignore[attr-defined]


admin.site.register(Game, GameAdmin)
