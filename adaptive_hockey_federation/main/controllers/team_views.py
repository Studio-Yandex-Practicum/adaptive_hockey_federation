from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from main.forms import TeamForm
from main.models import City, Player, Team
from main.permissions import TeamEditPermissionsMixin
from main.schemas.team_schema import (
    TEAM_SEARCH_FIELDS,
    TEAM_TABLE_HEAD,
    get_players_table,
    get_staff_table,
    get_team_table_data,
)
from unloads.utils import models_get_queryset


class TeamIdView(PermissionRequiredMixin, DetailView):
    """Вид команды.
    Детальный просмотр команды по игрокам и сотрудникам."""

    model = Team
    form_class = TeamForm
    template_name = "main/teams_id/teams_id.html"
    success_url = "/teams/"
    permission_required = "main.view_team"
    permission_denied_message = (
        "Отсутствует разрешение на просмотр карточки команды."
    )

    def get_object(self, queryset=None):
        return get_object_or_404(Team, id=self.kwargs["team_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.object
        players = (
            Player.objects.filter(team=self.kwargs["team_id"])
            .select_related("diagnosis")
            .select_related("discipline_name")
            .all()
        )
        context["players_table"] = get_players_table(players)
        context["staff_table"] = get_staff_table(team)
        context["team"] = team
        return context


class TeamListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    """Список спортивных команд."""

    model = Team
    template_name = "main/teams/teams.html"
    permission_required = "main.list_view_team"
    permission_denied_message = (
        "Отсутствует разрешение на просмотр списка команд."
    )
    context_object_name = "teams"
    paginate_by = 10
    ordering = ["id"]

    def get_queryset(self):
        queryset = super().get_queryset()
        dict_param = dict(self.request.GET)
        dict_param = {k: v for k, v in dict_param.items() if v != [""]}
        if len(dict_param) > 1:
            queryset = models_get_queryset(
                Team, dict_param, queryset, TEAM_SEARCH_FIELDS
            )

        return (
            queryset.select_related("discipline_name")
            .select_related("city")
            .order_by("name")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = context["teams"]
        user = self.request.user
        context["table_head"] = TEAM_TABLE_HEAD
        context["table_data"] = get_team_table_data(teams, user)
        return context


class CityListMixin:
    """Миксин для использования в видах редактирования и создания команд."""

    @staticmethod
    def get_cities():
        """Возвращает список имен всех городов из БД."""
        return City.objects.values_list("name", flat=True)


class UpdateTeamView(
    LoginRequiredMixin,
    TeamEditPermissionsMixin,
    UpdateView,
    CityListMixin,
):
    """Вид с формой изменения основных данных спортивной команды."""

    model = Team
    form_class = TeamForm
    template_name = "main/teams/team_create_edit.html"
    success_url = "/teams/"
    permission_required = "main.change_team"
    permission_denied_message = "Отсутствует разрешение на изменение команд."

    def get_object(self, queryset=None):
        team_id = self.kwargs.get("team_id")
        return get_object_or_404(Team, pk=team_id)

    def get_form_kwargs(self):
        kwargs = super(UpdateTeamView, self).get_form_kwargs()
        kwargs.update(
            initial={"city": self.object.city.name},
            user=self.request.user,
        )
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UpdateTeamView, self).get_context_data(**kwargs)
        context["cities"] = self.get_cities()
        context["page_title"] = "Редактирование данных команды"
        return context


class DeleteTeamView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Вид удаления спортивной команды."""

    object = Team
    model = Team
    success_url = "/teams/"
    permission_required = "main.delete_team"
    permission_denied_message = "Отсутствует разрешение на удаление команд."

    def get_object(self, queryset=None):
        team_id = self.kwargs.get("team_id")
        return get_object_or_404(Team, pk=team_id)


class CreateTeamView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView, CityListMixin
):
    """Вид с формой создания новой спортивной команды."""

    model = Team
    form_class = TeamForm
    template_name = "main/teams/team_create_edit.html"
    success_url = "/teams/"
    permission_required = "main.add_team"
    permission_denied_message = "Отсутствует разрешение на создание команд."

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateTeamView, self).get_context_data(**kwargs)
        context["cities"] = self.get_cities()
        context["page_title"] = "Создание команды"
        return context
