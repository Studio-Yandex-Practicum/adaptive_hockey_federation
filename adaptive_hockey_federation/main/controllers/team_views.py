from core.constants import StaffPosition
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from main.forms import StaffTeamMemberAddToTeamForm, TeamFilterForm, TeamForm
from main.models import City, Player, StaffTeamMember, Team
from main.permissions import CustomPermissionMixin, TeamEditPermissionsMixin
from main.schemas.team_schema import (
    TEAM_TABLE_HEAD,
    get_players_table,
    get_staff_table,
    get_team_table_data,
)
from unloads.utils import model_get_queryset


class StaffTeamMemberListMixin:
    """Миксин, для выбора сотрудника команды."""

    @staticmethod
    def get_staff(
        position: str | None = None,
        team_to_exclude: Team | None = None,
    ):
        """
        Формирует кортеж из сотрудников команд (StaffTeamMember).

        Формат элемента кортежа: "Фамилия Имя Отчество, должность (ID: id)",
        Если передан параметр position, то выбор фильтруется по полю
        staff_position и значению этого параметра.
        """
        filters = {"staff_position": position} if position else {}
        exclude = {"team": team_to_exclude} if team_to_exclude else {}
        query_set = StaffTeamMember.objects.filter(**filters).exclude(
            **exclude,
        )
        staffs = query_set.annotate(
            fio=Concat(
                "staff_member__surname",
                Value(" "),
                "staff_member__name",
                Value(" "),
                "staff_member__patronymic",
            ),
        ).values("fio", "staff_position", "id")
        return tuple(
            f"{i['fio']}, " f"{i['staff_position']} " f"(ID: {i['id']})"
            for i in staffs
        )

    def get_coaches(self, team_to_exclude: Team | None = None):
        """Получить сотрудника команды с позицией тренер."""
        return self.get_staff("тренер", team_to_exclude=team_to_exclude)

    def get_pushers(self, team_to_exclude: Team | None = None):
        """Получить сотрудника команды с позицией пушер-тьютор."""
        return self.get_staff("пушер-тьютор", team_to_exclude=team_to_exclude)


class TeamIdView(
    PermissionRequiredMixin,
    DetailView,
    StaffTeamMemberListMixin,
):
    """
    Вид команды.

    Детальный просмотр команды по игрокам и сотрудникам.
    """

    model = Team
    form_class = TeamForm
    template_name = "main/teams_id/teams_id.html"
    success_url = "/teams/"
    permission_required = "main.view_team"
    permission_denied_message = (
        "Отсутствует разрешение на просмотр карточки команды."
    )

    def get_object(self, queryset=None):
        """Получить объект по id или выбросить ошибку 404."""
        return get_object_or_404(Team, id=self.kwargs["team_id"])

    def update_context_with_staff_add_form(
        self,
        context: dict,
        position_filter: str | None = None,
        staff_table_index: int = 0,
        data_list: tuple[str, ...] = ("",),
        data_list_id: str = "available_staffs",
    ):
        """Обновить словарь context с помощью StaffTeamMemberAddToTeamForm."""
        new_staff_form = StaffTeamMemberAddToTeamForm(
            position_filter=position_filter,
            team=self.get_object(),
        )
        update_data = {
            "add_staff_form": new_staff_form,
            "data_list": data_list,
            "add_staff_field_data_list_id": data_list_id,
        }
        context["staff_table"][staff_table_index].update(update_data)

    def update_context_with_additional_forms(self, context):
        """
        Добавляет в контекст формы добавления тренера и пушера в команду.

        Также добавляет соответствующие списки для инкрементного поиска в
        поле форм.
        - context: параметр по ссылке, т.е. данная переменная будет изменена в
        вызывающей функции.
        """
        data_list = self.get_coaches(team_to_exclude=self.object)
        self.update_context_with_staff_add_form(
            context,
            StaffPosition.TRAINER,
            0,
            data_list,
            "available_coaches",
        )

        data_list = self.get_pushers(team_to_exclude=self.object)
        self.update_context_with_staff_add_form(
            context,
            StaffPosition.OTHER,
            1,
            data_list,
            "available_pushers",
        )

    def get_context_data(self, **kwargs):
        """Получить словарь context для шаблона страницы."""
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
        self.update_context_with_additional_forms(context)
        return context

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса от форм добавления тренера или пушера."""
        form_index = int(request.POST["btn_add_staff"])
        position_filter = (StaffPosition.TRAINER, StaffPosition.OTHER)[
            form_index
        ]
        new_staff_form = StaffTeamMemberAddToTeamForm(
            data=request.POST,
            team=self.get_object(),
            position_filter=position_filter,
        )
        if new_staff_form.is_valid():
            staff_team_member_team = new_staff_form.save(commit=False)
            staff_team_member_team.team = self.get_object()
            staff_team_member_team.save()
            return redirect(
                "main:teams_id",
                team_id=self.kwargs["team_id"],
            )
        self.object = self.get_object()
        context = self.get_context_data()
        context["staff_table"][form_index]["add_staff_form"] = new_staff_form
        return render(request, self.template_name, context)


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
    ordering = ["name"]

    def get_queryset(self):
        """Получить набор QuerySet."""
        queryset = super().get_queryset()
        return model_get_queryset(
            "teams",
            Team,
            dict(self.request.GET),
            queryset,
        )

    def get_context_data(self, **kwargs):
        """Получить словарь context для шаблона страницы."""
        context = super().get_context_data(**kwargs)
        teams = context["teams"]
        user = self.request.user
        context["form_filter"] = TeamFilterForm(self.request.GET or None)
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
        """Получить объект по id или выбросить ошибку 404."""
        team_id = self.kwargs.get("team_id")
        return get_object_or_404(Team, pk=team_id)

    def get_form_kwargs(self):
        """Получить аргументы для формы."""
        kwargs = super(UpdateTeamView, self).get_form_kwargs()
        kwargs.update(
            initial={"city": self.object.city.name},
            user=self.request.user,
        )
        return kwargs

    def get_context_data(self, **kwargs):
        """Получить словарь context для шаблона страницы."""
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
        """Получить объект по id или выбросить ошибку 404."""
        team_id = self.kwargs.get("team_id")
        return get_object_or_404(Team, pk=team_id)


class CreateTeamView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
    CityListMixin,
):
    """Вид с формой создания новой спортивной команды."""

    model = Team
    form_class = TeamForm
    template_name = "main/teams/team_create_edit.html"
    success_url = "/teams/"
    permission_required = "main.add_team"
    permission_denied_message = "Отсутствует разрешение на создание команд."

    def form_valid(self, form):
        """Запустить валидацию формы."""
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Получить словарь context для шаблона страницы."""
        context = super(CreateTeamView, self).get_context_data(**kwargs)
        context["cities"] = self.get_cities()
        context["page_title"] = "Создание команды"
        return context


class FireStaffFromTeam(
    LoginRequiredMixin,
    CustomPermissionMixin,
    DeleteView,
):
    """Вид для удаления сотрудника из команды (связи сотрудник-команда)."""

    model = StaffTeamMember.team.through
    permission_required = "main.change_team"
    object = StaffTeamMember.team.through

    def get_success_url(self):
        """Перенаправить на указанный адрес при успешном удалении."""
        team_id = self.kwargs["team_id"]
        return reverse("main:teams_id", args=[team_id])

    def get_object(self):
        """Получить объект по id team и staff или выбросить ошибку 404."""
        team_id = self.kwargs["team_id"]
        staff_team_member_id = self.kwargs["staff_team_member_id"]
        return get_object_or_404(
            self.model,
            team__id=team_id,
            staffteammember__id=staff_team_member_id,
        )

    def test_func(self):
        """Выполнить проверку разрешения на доступ к объекту."""
        team = get_object_or_404(Team, id=self.kwargs["team_id"])
        user = self.request.user
        return not user.is_agent or team.curator == user
