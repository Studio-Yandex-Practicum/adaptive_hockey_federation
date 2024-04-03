from core.constants import STAFF_POSITION_CHOICES
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from main.controllers.utils import get_player_href
from main.forms import TeamForm
from main.models import City, Player, Team
from main.permissions import TeamEditPermissionsMixin


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
            .select_related("discipline")
            .all()
        )
        staff_table = [
            {
                "position": staff_position[1].title(),
                "head": {
                    "number": "№",
                    "surname": "Фамилия",
                    "name": "Имя",
                    "position": "Квалификация",
                    "note": "Примечание",
                },
                "data": [
                    {
                        "number": i + 1,
                        "surname": staff.staff_member.surname,
                        "name": staff.staff_member.name,
                        "position": staff.qualification,
                        "note": staff.notes,
                        "id": staff.id,
                    }
                    for i, staff in enumerate(
                        team.team_members.filter(
                            staff_position=staff_position[1]
                        )
                    )
                ],
            }
            for staff_position in STAFF_POSITION_CHOICES
        ]
        players_table = {
            "name": "Игроки",
            "head": {
                "full_name": "Фамилия, Имя",
                "birthday": "Д.Р.",
                "gender": "Пол",
                "position": "Квалификация",
                "diagnosis": "Диагноз",
                "number": "№",
                "level_revision": "Уровень ревизии",
            },
            "data": [
                {
                    "full_name_link": get_player_href(player),
                    "birthday": player.birthday,
                    "gender": player.get_gender_display(),
                    "position": player.get_position_display(),
                    "diagnosis": (
                        player.diagnosis.name if player.diagnosis else None
                    ),
                    "number": player.number,
                    "level_revision": player.level_revision,
                    "id": player.pk,
                }
                for player in players
            ],
        }

        context["players_table"] = players_table
        context["staff_table"] = staff_table
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
        search = self.request.GET.get("search")
        if search:
            search_column = self.request.GET.get("search_column")
            team_structure_lookup = (
                Q(team_players__name__icontains=search)
                | Q(team_players__surname__icontains=search)
                | Q(team_players__patronymic__icontains=search)
                | Q(team_members__staff_member__name__icontains=search)
                | Q(team_members__staff_member__surname__icontains=search)
                | Q(team_members__staff_member__patronymic__icontains=search)
            )
            if not search_column or search_column.lower() in ["все", "all"]:
                or_lookup = (
                    Q(discipline_name_id__name__icontains=search)
                    | Q(name__icontains=search)
                    | Q(city__name__icontains=search)
                )
                queryset = queryset.filter(or_lookup)
            elif search_column == "team_structure":
                or_lookup = team_structure_lookup
                queryset = queryset.filter(or_lookup)
            else:
                search_fields = {
                    "discipline_name": "discipline_name_id__name",
                    "name": "name",
                    "city": "city__name",
                }
                lookup = {f"{search_fields[search_column]}__icontains": search}
                queryset = queryset.filter(**lookup)

        return (
            queryset.select_related("discipline_name")
            .select_related("city")
            .order_by("name")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = context["teams"]

        table_data = []
        for team in teams:
            team_data = {
                "id": team.id,
                "name": team.name,
                "discipline_name": team.discipline_name,
                "city": team.city,
                "_ref_": {
                    "name": "Посмотреть",
                    "type": "button",
                    "url": reverse("main:teams_id", args=[team.id]),
                },
            }
            table_data.append(team_data)

        context["table_head"] = {
            "name": "Название",
            "discipline_name": "Дисциплина",
            "city": "Город",
            "team_structure": "Состав команды",
        }
        context["table_data"] = table_data
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
    template_name = "main/teams/team_update.html"
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
    template_name = "main/teams/team_create.html"
    success_url = "/teams/?page=last"
    permission_required = "main.add_team"
    permission_denied_message = "Отсутствует разрешение на создание команд."

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateTeamView, self).get_context_data(**kwargs)
        context["cities"] = self.get_cities()
        return context
