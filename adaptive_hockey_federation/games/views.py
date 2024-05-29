from typing import Any

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from games.forms import GameForm
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
        return Game.objects.all().prefetch_related("game_teams")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Метод для получения словаря context в шаблоне страницы."""
        context = super().get_context_data(**kwargs)
        games = context["games"]
        table_data = []
        for game in games:
            first_team, second_team = (
                game.game_teams.values().first(),
                game.game_teams.values().last(),
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


class GameCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представление для создания объекта игры."""

    model = Game
    form_class = GameForm
    template_name = "main/games/game_create_edit.html"
    permission_required = "games.add_game"
    permission_denied_message = "Отсутствует разрешение на создание игры."
    success_url = reverse_lazy("games:games")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Метод для получения словаря context в шаблоне страницы."""
        context = super(GameCreateView, self).get_context_data(**kwargs)
        return dict(
            **context,
            page_title="Создание игры",
            help_text_role="Выбранные команды",
        )

    # def get_success_url(self) -> str:
    #     """
    #     Метод для получения URL-адреса для перенаправления по
    #     успешному заполнению формы.
    #     """
    #     return reverse(
    #         "games:game_id", kwargs={"pk": self.object.pk}
    #     )
    # TODO: раскомментировать, когда появится представление для просмотра/
    #  редактирования игры

    def post(self, request, *args, **kwargs) -> Any:
        """Метод для обработки POST-запроса."""
        self.game_teams = request.POST.get("game_teams", None)
        return super().post(request, *args, **kwargs)
