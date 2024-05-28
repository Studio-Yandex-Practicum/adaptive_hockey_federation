from typing import Any

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from games.models import Game


class GamesListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    """Список игр."""

    model = Game
    template_name = "main/games/games.html"
    permission_required = "unloads.list_view_unload"
    permission_denied_message = (
        "Отсутствует разрешение на просмотр списка игр."
    )
    context_object_name = "games"
    paginate_by = 10
    ordering = ["name"]

    def get_queryset(self) -> QuerySet[Any]:
        """Метод для получения набора QuerySet."""
        return Game.objects.all().prefetch_related("teams")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Метод для получения словаря context в шаблоне страницы."""
        context = super().get_context_data(**kwargs)
        games = context["games"]
        table_data = []
        for game in games:
            first_team, second_team = (
                game.teams.values().first(),
                game.teams.values().last(),
            )
            table_data.append(
                {
                    "pk": game.pk,
                    "name": game.name,
                    "video_link": game.video_link,
                    "first_team": first_team["name"],
                    "second_team": second_team["name"],
                },
            )
        context["table_head"] = {
            "pk": "Nr.",
            "name": "Название",
            "video_link": "Ссылка на видео",
            "first_team": "Команда 1",
            "second_team": "Команда 2",
        }
        context["table_data"] = table_data
        return context
