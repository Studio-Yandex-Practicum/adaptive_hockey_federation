from core.constants import OTHER, TRAINER
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import RedirectView
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
        """Формирует кортеж из сотрудников команд (StaffTeamMember).
        Формат элемента кортежа: "Фамилия Имя Отчество, должность (ID: id)",
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
        ).values("fio", "staff_position", "id")
        return tuple(
            (f"{i['fio']}, " f"{i['staff_position']} " f"(ID: {i['id']})")
            for i in staffs
        )

    def get_coaches(self):
        return self.get_staff("тренер")

    def get_pushers(self):
        return self.get_staff("пушер-тьютор")


class TeamIdView(
    PermissionRequiredMixin, DetailView, StaffTeamMemberListMixin
):
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

    def get_new_staff_form(
        self, form_name_in_context: str, position_filter: str | None = None
    ):
        """Возвращает форму добавления нового сотрудника.
        Параметры:
            - form_name_in_context: наименование формы в контексте,
            по которому будет производиться поиск наличия этой формы в
            self.kwargs;
            - position_filter: фильтрация для списка сотрудников в поле
            поиска."""
        new_staff_form = self.kwargs.get(form_name_in_context, None)
        new_staff_form = new_staff_form or StaffTeamMemberAddToTeamForm(
            position_filter=position_filter, team=self.get_object()
        )
        return new_staff_form

    def update_context_with_additional_forms(self, context):
        new_coach_form = self.get_new_staff_form(
            "new_coach_form", position_filter=TRAINER
        )
        new_pusher_form = self.get_new_staff_form(
            "new_pusher_form", position_filter=OTHER
        )
        context["new_coach_form"] = new_coach_form
        context["new_pusher_form"] = new_pusher_form

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
        # new_coach_form = self.kwargs.get("new_coach_form", None)
        # new_pusher_form = self.kwargs.get("new_pusher_form", None)
        #
        # new_coach_form = new_coach_form or StaffTeamMemberAddToTeamForm(
        #     position_filter=TRAINER, team=self.get_object()
        # )
        # context["new_coach_form"] = new_coach_form
        self.update_context_with_additional_forms(context)
        context["available_coaches_list"] = self.get_coaches()
        context["available_pushers_list"] = self.get_pushers()
        return context

    def post(self, request, *args, **kwargs):
        new_coach_form = StaffTeamMemberAddToTeamForm(
            data=request.POST, team=self.get_object(), position_filter=TRAINER
        )
        if new_coach_form.is_valid():
            staff_team_member_team = new_coach_form.save(commit=False)
            staff_team_member_team.team = self.get_object()
            staff_team_member_team.save()
            return redirect(
                "main:teams_id",
                team_id=self.kwargs["team_id"],
            )
        self.object = self.get_object()
        context = self.get_context_data()
        context["new_coach_form"] = new_coach_form
        # return redirect(
        #     "main:teams_id", team_id=self.kwargs["team_id"],
        #     **context
        # )
        return render(request, self.template_name, context)


class AddStaffView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    """Представление добавления сотрудника в команду.
    В данном виде не отображает какой-то отдельной страницы либо формы.
    Используется для обработки нажатия кнопки либо соответствующего
    post-запроса. Добавляет сотрудника в команду, после чего делает
    редирект на страницу управления соответствующей командой."""

    pattern_name = "main:teams_id"
    http_method_names = ("post",)
    permission_required = "main.change_team"

    def post(self, request, *args, **kwargs):
        staff_team_member = get_object_or_404(
            StaffTeamMember, id=kwargs.get("staff_team_member_id", 0)
        )
        team = get_object_or_404(Team, id=kwargs.get("team_id"))
        staff_team_member.team.add(team)
        return super().post(request, *args, **kwargs)


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
