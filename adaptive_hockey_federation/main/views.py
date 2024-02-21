from core.constants import STAFF_POSITION_CHOICES
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from main.forms import PlayerForm, TeamForm
from main.models import City, Document, Player, Team

from adaptive_hockey_federation.core.utils import generate_file_name


@login_required
def main(request):
    return render(request, "main/home/main.html")


class PlayerCreateView(CreateView):
    '''View-класс для создания нового игрока.'''
    model = Player
    form_class = PlayerForm
    template_name = "main/player_id/player_id_create.html"
    success_url = "/players"

    def form_valid(self, form):
        player = form.save()
        for iter, file in enumerate(self.request.FILES.getlist('documents')):
            file.name = generate_file_name(file.name, player.name, iter)
            Document.objects.create(
                player=player, file=file, name=file.name
            )
        return super().form_valid(form)


class PlayersListView(LoginRequiredMixin, ListView):
    model = Player
    template_name = "main/players/players.html"
    context_object_name = "players"
    paginate_by = 10
    fields = [
        "id",
        "surname",
        "name",
        "birthday",
        "gender",
        "number",
        "discipline",
        "diagnosis",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            search_column = self.request.GET.get("search_column")
            if not search_column or search_column.lower() in ["все", "all"]:
                or_lookup = (
                    Q(surname__icontains=search)
                    | Q(name__icontains=search)
                    | Q(birthday__icontains=search)
                    | Q(gender__icontains=search)
                    | Q(number__icontains=search)
                    | Q(discipline__discipline_name_id__name__icontains=search)
                    | Q(diagnosis__name__icontains=search)
                )
                queryset = queryset.filter(or_lookup)
            else:
                search_fields = {
                    "surname": "surname",
                    "name": "name",
                    "birthday": "birthday",
                    "gender": "gender",
                    "number": "surname",
                    "discipline": "discipline__discipline_name_id__name",
                    "diagnosis": "diagnosis__name",
                }
                lookup = {f"{search_fields[search_column]}__icontains": search}
                queryset = queryset.filter(**lookup)

        return (
            queryset.select_related("diagnosis")
            .select_related("discipline")
            .order_by("surname")
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        table_head = {}
        for field in self.fields:
            if field != "id":
                table_head[field] = Player._meta.get_field(field).verbose_name
        context["table_head"] = table_head

        table_data = [
            {
                "surname": player.surname,
                "name": player.name,
                "birthday": player.birthday,
                "gender": player.get_gender_display(),
                "number": player.number,
                "discipline": player.discipline if player.discipline else None,
                "diagnosis": player.diagnosis.name
                if player.diagnosis
                else None,  # Noqa
                "url": reverse("main:player_id", args=[player.id]),
                "id": player.pk,
            }
            for player in context["players"]
        ]

        context["table_data"] = table_data
        return context


class PlayerIdView(DetailView):
    model = Player
    template_name = "main/player_id/player_id.html"
    context_object_name = "player"
    fields = [
        "surname",
        "name",
        "patronymic",
        "gender",
        "birthday",
        "discipline",
        "diagnosis",
        "level_revision",
        "identity_document",
        "team",
        "is_captain",
        "is_assistent",
        "position",
        "number",
        "document",
    ]

    def get_object(self, queryset=None):
        return get_object_or_404(Player, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = context["player"]

        player_fields_personal = [
            ("Фамилия", player.surname),
            ("Имя", player.name),
            ("Отчество", player.patronymic),
            ("Пол", player.gender),
            ("Дата рождения", player.birthday),
            ("Удостоверение личности", player.identity_document),
            ("Дисциплина", player.discipline),
            ("Диагноз", player.diagnosis),
        ]

        player_fields = [
            ("Команда", ", ".join([team.name for team in player.team.all()])),
            ("Уровень ревизии", player.level_revision),
            ("Капитан", player.is_captain),
            ("Ассистент", player.is_assistent),
            ("Игровая позиция", player.position),
            ("Номер игрока", player.number),
        ]

        player_fields_doc = [("Документ", player.identity_document)]

        context["player_fields_personal"] = player_fields_personal
        context["player_fields"] = player_fields
        context["player_fields_doc"] = player_fields_doc
        return context


class PlayerIDEditView(UpdateView):
    model = Player
    template_name = "main/player_id/player_id_edit.html"
    form_class = PlayerForm

    def get_success_url(self):
        return reverse("main:player_id", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(Player, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.get_object()

        player_fields_personal = [
            ("Фамилия", player.surname),
            ("Имя", player.name),
            ("Отчество", player.patronymic),
            ("Пол", player.gender),
            ("Дата рождения", player.birthday),
            ("Удостоверение личности", player.identity_document),
            ("Дисциплина", player.discipline),
            ("Диагноз", player.diagnosis),
        ]

        player_fields = [
            ("Команда", ", ".join([team.name for team in player.team.all()])),
            ("Уровень ревизии", player.level_revision),
            ("Капитан", player.is_captain),
            ("Ассистент", player.is_assistent),
            ("Игровая позиция", player.position),
            ("Номер игрока", player.number),
        ]

        player_fields_doc = [("Документ", player.identity_document)]
        player_documents = player.player_documemts.all()
        context["player_documents"] = player_documents
        context["player_fields_personal"] = player_fields_personal
        context["player_fields"] = player_fields
        context["player_fields_doc"] = player_fields_doc
        return context


class PlayerIDDeleteView(DeleteView):
    model = Player
    success_url = reverse_lazy("main:players")

    def get_object(self, queryset=None):
        return get_object_or_404(Player, id=self.kwargs["pk"])


class TeamIdView(PermissionRequiredMixin, DetailView):
    """Вид команды.
    Детальный просмотр команды по игрокам и сотрудникам."""

    model = Team
    form_class = TeamForm
    template_name = "main/teams_id/teams_id.html"
    success_url = "/teams/"
    permission_required = "main.view_team"
    permission_denied_message = ("Отсутствует разрешение на просмотр "
                                 "содержимого.")

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
                    "function": "Должность",
                    "position": "Квалификация",
                    "note": "Примечание",
                },
                "data": [
                    {
                        "number": i + 1,
                        "surname": staff.staff_member.surname,
                        "name": staff.staff_member.name,
                        "function": staff.staff_position,
                        "position": staff.qualification,
                        "note": staff.notes,
                    }
                    for i, staff in enumerate(
                        team.team_members.filter(
                            staff_position=staff_position[1].title()
                        )
                    )
                ]
            }
            for staff_position in STAFF_POSITION_CHOICES
        ]
        players_table = {
            "name": "Игроки",
            "head": {
                "number": "№",
                "surname": "Фамилия",
                "name": "Имя",
                "birthday": "Д.Р.",
                "gender": "Пол",
                "position": "Квалификация",
                "diagnosis": "Диагноз",
                "discipline": "Дисциплина",
                "level_revision": "Уровень ревизии",
            },
            "data": [
                {
                    "number": player.number,
                    "surname": player.surname,
                    "name": player.name,
                    "birthday": player.birthday,
                    "gender": player.get_gender_display(),
                    "position": player.get_position_display(),
                    "diagnosis": player.diagnosis.name
                    if player.diagnosis else None,
                    "discipline": player.discipline
                    if player.discipline else None,
                    "level_revision": player.level_revision,
                }
                for player in players
            ]
        }

        context["players_table"] = players_table
        context["staff_table"] = staff_table
        context["team"] = team

        return context


class TeamListView(LoginRequiredMixin, ListView):
    """Список спортивных команд."""

    model = Team
    template_name = "main/teams/teams.html"
    context_object_name = "teams"
    paginate_by = 10
    ordering = ["id"]

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
                    "name": "Игроки",
                    "type": "button",
                    "url": reverse("main:teams_id", args=[team.id]),
                },
            }
            table_data.append(team_data)

        context["table_head"] = {
            "name": "Название",
            "discipline_name": "Дисциплина",
            "city": "Город",
            "players_reference": "Игроки",
        }
        context["table_data"] = table_data
        return context


class CityListMixin:
    """Миксин для использования в видах редактирования и создания команд."""

    @staticmethod
    def get_cities():
        """Возвращает список имен всех городов из БД."""
        return City.objects.values_list('name', flat=True)


class UpdateTeamView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
    CityListMixin
):
    """Вид с формой изменения основных данных спортивной команды."""

    model = Team
    form_class = TeamForm
    template_name = "main/teams/team_update.html"
    success_url = '/teams/'
    permission_required = 'main.change_team'

    def get_object(self, queryset=None):
        team_id = self.kwargs.get("team_id")
        return get_object_or_404(Team, pk=team_id)

    def get_context_data(self, **kwargs):
        context = super(UpdateTeamView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(
            instance=self.object,
            initial={'city': self.object.city.name}
        )
        context['cities'] = self.get_cities()
        return context


class DeleteTeamView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    """Вид удаления спортивной команды."""

    object = Team
    model = Team
    success_url = '/teams/'
    permission_required = 'team.delete_team'

    def get_object(self, queryset=None):
        team_id = self.kwargs.get('team_id')
        return get_object_or_404(Team, pk=team_id)


class CreateTeamView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
    CityListMixin
):
    """Вид с формой создания новой спортивной команды."""

    model = Team
    form_class = TeamForm
    template_name = 'main/teams/team_create.html'
    permission_required = 'team.add_team'
    success_url = '/teams/?page=last'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateTeamView, self).get_context_data(**kwargs)
        context['cities'] = self.get_cities()
        return context


@login_required
def competitions_id(request, id):
    return render(request, "main/competitions_id/competitions_id.html")


@login_required
def analytics(request):
    return render(request, "main/analytics/analitics.html")


@login_required
def unloads(request):
    return render(request, "main/unloads/unloads.html")


def player_id_deleted(request):
    return render(request, "main/player_id_deleted.html")
