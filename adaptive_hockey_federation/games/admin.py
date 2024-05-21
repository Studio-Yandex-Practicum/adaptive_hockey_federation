from django.contrib import admin
from games.models import Game, GameTeam


class GameTeamInline(admin.StackedInline):
    model = GameTeam
    extra = 2


class GameAdmin(admin.ModelAdmin):
    """Админка для модели Выгрузки."""
    inlines = [GameTeamInline]
    list_display = ("name", "video_link")
    search_fields = ("name",)
    ordering = ["name"]


admin.site.register(Game, GameAdmin)
