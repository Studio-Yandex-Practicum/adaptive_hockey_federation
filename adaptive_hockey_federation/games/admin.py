from django.contrib import admin
from games.models import Game, GamePlayer, GameTeam


class GameTeamsInLine(admin.StackedInline):
    """Инлайн для команд, участвующих в игре."""

    model = GameTeam
    extra = 0


class GamePlayersInLine(admin.TabularInline):
    """Инлайн для игроков, участвующих в игре."""

    model = GamePlayer
    extra = 0
    readonly_fields = ("name", "number", "game_team")
    can_delete = False


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Админка для модели игр."""

    list_display = ("name", "date", "competition", "video_link")
    list_filter = ("date", "competition")
    search_fields = ("name",)
    ordering = ["name"]
    inlines = [GameTeamsInLine]


@admin.register(GameTeam)
class GameTeamAdmin(admin.ModelAdmin):
    """Админка для модели команды, участвующей в игре."""

    list_display = ("name", "discipline_name", "game")
    list_filter = ("game",)
    search_fields = ("name",)
    ordering = ["name"]
    inlines = [GamePlayersInLine]


@admin.register(GamePlayer)
class GamePlayerAdmin(admin.ModelAdmin):
    """Админка для модели игроков, участвующих в игре."""

    list_display = ("name", "number", "game_team")
    list_filter = ("game_team",)
    search_fields = ("name",)
    ordering = ["name"]
