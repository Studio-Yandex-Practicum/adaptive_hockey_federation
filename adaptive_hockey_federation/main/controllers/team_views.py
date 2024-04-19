from core.constants import TRAINER
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from main.forms import StaffTeamMemberAddToTeamForm, TeamForm
from main.models import City, Player, StaffTeamMember, Team
from main.permissions import TeamEditPermissionsMixin
from main.schemas.team_schema import (
    TEAM_SEARCH_FIELDS,
    TEAM_TABLE_HEAD,
    get_players_table,
    get_staff_table,
    get_team_table_data,
)


class StaffTeamMemberListMixin:
    """Миксин, для выбора сотрудника команды."""

    @staticmethod
    def get_staff(position: str | None = None):
        """Формирует список из сотрудников команд (StaffTeamMember).
        Формат: [["Фамилия Имя Отчество", id], [....]].
        Если передан параметр position, то выбор фильтруется по полю
        staff_position и значению этого параметра."""
        if position:
            query_set = StaffTeamMember.objects.filter(staff_position=position)
        else:
            query_set = StaffTeamMember.objects.all()
        staffs = query_set.annotate(
            fio=Concat(
                "staff_member__surname",
                Value(" "),
                "staff_member__name",
                Value(" "),
                "staff_member__patronymic",
            )
        ).values_list("fio", "id")
        return list(staffs)

    def get_coaches(self):
        return self.get_staff("тренер")

    def def_pushers(self):
        return self.get_staff("пушер-тьютор")


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
        context["new_coach_form"] = StaffTeamMemberAddToTeamForm(
            position_filter=TRAINER, team=team
        )
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
                    Q(discipline_name__name__icontains=search)
                    | Q(name__icontains=search)
                    | Q(city__name__icontains=search)
                )
                queryset = queryset.filter(or_lookup)
            elif search_column == "team_structure":
                or_lookup = team_structure_lookup
                queryset = queryset.filter(or_lookup)
            else:
                search_fields = TEAM_SEARCH_FIELDS
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
