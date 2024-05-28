from django.contrib import admin
from games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Админка для модели игр."""

    list_display = ("name", "date", "competition", "video_link")
    list_filter = ("date", "competition")
    search_fields = ("name",)
    ordering = ["name"]
