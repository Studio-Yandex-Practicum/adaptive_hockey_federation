import logging
from dataclasses import dataclass

from typing import Any
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    FormView,
    UpdateView,
)
from django.views.generic.list import ListView

from games.constants import Errors, Literals, NumericalValues
from games.forms import EditTeamPlayersNumbersForm, GameForm, GameUpdateForm
from games.mixins import GameCreateUpdateMixin
from games.models import Game, GamePlayer, GameTeam
from core.logging import configure_logging


configure_logging()
logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Сообщение с уровнем важности."""

    level: int
    text: str


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
        queryset = (
            super()
            .get_queryset()
            .prefetch_related("game_teams", "competition")
        )
        search_params = self.request.GET.dict()
        search_column = search_params.get("search_column")
        search = search_params.get("search")
        if search_column and search:
            if search_column == "name":
                queryset = queryset.filter(name__icontains=search)
            elif search_column == "team":
                queryset = queryset.filter(game_teams__name__icontains=search)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Метод для получения словаря context в шаблоне страницы."""
        context = super().get_context_data(**kwargs)
        context["games"] = self.get_queryset()
        games = context["games"]
        table_data = []
        for game in games:
            first_team, second_team = (
                game.game_teams.first(),
                game.game_teams.last(),
            )
            table_data.append(
                {
                    "pk": game.pk,
                    "competition": (
                        game.competition.title if game.competition else None
                    ),
                    "name": game.name,
                    "video_link": game.video_link,
                    "first_team": first_team.name if first_team else None,
                    "second_team": second_team.name if second_team else None,
                },
            )
        context["table_head"] = {
            "pk": Literals.GAME_NUMBER,
            "competition": Literals.GAME_COMPETITION,
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


class GamesInfoView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    """Представление для получения деталей игры."""

    model = Game
    form_class = GameForm
    template_name = "main/games/game_detail.html"
    permission_required = "games.delete_game"
    permission_denied_message = Errors.PERMISSION_MISSING.format(
        action=Errors.DELETE_GAME,
    )

    def get_object(self, queryset: QuerySet = None) -> Game:
        """Получить объект по id или выбросить ошибку 404."""
        return get_object_or_404(Game, id=self.kwargs["game_id"])

    def get_teams(self, queryset: QuerySet = None) -> Game:
        """Получить список объектов команд, связанных с игрой."""
        return GameTeam.objects.filter(game=self.kwargs["game_id"])

    def get_context_data(self, **kwargs):
        """Метод для получения словаря context в шаблоне страницы."""
        context = super().get_context_data(**kwargs)

        teams = self.get_teams()

        for team in teams:
            players = GamePlayer.objects.filter(game_team=team)
            team.players = players

        context["teams"] = teams
        return context


class EditTeamPlayersNumbersView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    FormView,
):
    """Представление для редактирования номеров команды, участвующей в игре."""

    template_name = "main/games/player_number_edit.html"
    form_class = EditTeamPlayersNumbersForm
    permission_required = "games.edit_player_number"
    permission_denied_message = Errors.PERMISSION_MISSING.format(
        action=Errors.CREATE_GAME,
    )

    def get_form_kwargs(self):
        """Передача дополнительных аргументов в форму."""
        kwargs = super().get_form_kwargs()
        game_team = get_object_or_404(
            GameTeam,
            gameteam_id=self.kwargs["game_team"],
        )
        kwargs["game_team"] = game_team
        if self.request.method == "POST":
            kwargs["data"] = self.request.POST
        return kwargs

    def form_valid(self, form):
        """Обработка валидной формы."""
        form.save()
        return redirect(
            reverse_lazy(
                "games:game_info",
                kwargs={"game_id": form.game_team.game.id},
            ),
        )

    def get_context_data(self, **kwargs):
        """Метод для получения словаря context в шаблоне страницы."""
        context = super().get_context_data(**kwargs)
        context["game_team"] = get_object_or_404(
            GameTeam,
            gameteam_id=self.kwargs["game_team"],
        )
        context["page_title"] = "Редактирование номеров игроков команды"
        return context
