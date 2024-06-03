from typing import Any, Union

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from games.constants import Errors, Literals, NumericalValues
from games.forms import GameForm, GameUpdateForm
from games.mixins import GameCreateUpdateMixin
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
    permission_denied_message = Errors.PERMISSION_MISSING.format(
        action=Errors.GAME_LIST_VIEW,
    )
    context_object_name = "games"
    paginate_by = NumericalValues.PAGINATION_BASE_VALUE
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
            "pk": Literals.GAME_NUMBER,
            "name": Literals.GAME_NAME,
            "video_link": Literals.GAME_VIDEO_LINK,
            "first_team": Literals.GAME_FIRST_TEAM,
            "second_team": Literals.GAME_SECOND_TEAM,
        }
        context["table_data"] = table_data
        return context


class GameCreateView(GameCreateUpdateMixin, CreateView):
    """Представление для создания объекта игры."""

    form_class = GameForm
    permission_required = "games.add_game"
    permission_denied_message = Errors.PERMISSION_MISSING.format(
        action=Errors.CREATE_GAME,
    )

    def post(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> Union[HttpResponseRedirect, HttpResponse]:
        """Метод для обработки POST-запроса."""
        self.game_teams = request.POST.get("game_teams")
        return super().post(request, *args, **kwargs)


class GameEditView(GameCreateUpdateMixin, UpdateView):
    """Представление для редактирования объекта игры."""

    form_class = GameUpdateForm
    permission_required = "games.edit_game"
    permission_denied_message = Errors.PERMISSION_MISSING.format(
        action=Errors.EDIT_GAME,
    )

    def get_object(self, queryset: QuerySet = None) -> Game:
        """Получить объект по id или выбросить ошибку 404."""
        return get_object_or_404(Game, id=self.kwargs["game_id"])


class GameDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Представление для удаления объекта игры."""

    model = Game
    success_url = reverse_lazy("games:games")
    template_name = "main/games/game_edit_delete_buttons.html"

    permission_required = "games.delete_game"
    permission_denied_message = Errors.PERMISSION_MISSING.format(
        action=Errors.DELETE_GAME,
    )

    def get_object(self, queryset: QuerySet = None) -> Game:
        """Получить объект по id или выбросить ошибку 404."""
        return get_object_or_404(Game, id=self.kwargs["game_id"])
