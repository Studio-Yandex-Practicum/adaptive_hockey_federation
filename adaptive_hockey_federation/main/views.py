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
from main.forms import DocumentForm, PlayerForm, TeamForm
from main.models import Player, Team

# пример рендера таблиц, удалить после реализации вьюх
CONTEXT_EXAMPLE = {
    "table_head": {"id": "Идентификатор", "name": "Имя", "surname": "Фамилия"},
    "table_data": [
        {"id": 1, "name": "Иван", "surname": "Иванов"},
        {"id": 2, "name": "Пётр", "surname": "Петров"},
    ],
}


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
        context = self.get_context_data()
        files = context["player_documents"]

        self.object = form.save()

        if files.is_valid():
            files.instance = self.object
            files.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            images_form = DocumentForm(
                self.request.POST, self.request.FILES
            )
        else:
            images_form = DocumentForm()
        print(images_form)
        print(self.object)
        context['formset'] = images_form
        context['player'] = self.object
        return context

    # def get_success_url(self):
    #     return reverse("main:player_id", kwargs={"pk": self.object.pk})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     player = self.get_object()

    #     player_fields = [
    #         ("Команда", ", ".join(
    # [team.name for team in player.team.all()])),
    #         ("Уровень ревизии", player.level_revision),
    #         ("Капитан", player.is_captain),
    #         ("Ассистент", player.is_assistent),
    #         ("Игровая позиция", player.position),
    #         ("Номер игрока", player.number),
    #     ]

    #     player_fields_doc = [("Документ", player.identity_document)]
    #     player_documents = player.player_documemts.all()
    #     context["player_documents"] = player_documents
    #     context["player_fields_personal"] = player_fields_personal
    #     context["player_fields"] = player_fields
    #     context["player_fields_doc"] = player_fields_doc
    #     return context


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


class TeamIdView(DetailView):
    model = Team
    form_class = TeamForm
    template_name = "main/teams_id/teams_id.html"
    success_url = "/teams/"

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
        staff_list = team.team_members.all()
        staff_table_head = {
            "number": "№",
            "surname": "Фамилия",
            "name": "Имя",
            "function": "Должность",
            "position": "Квалификация",
            "note": "Примечание",
        }
        staff_table_data = [
            {
                "number": i + 1,
                "surname": staff.staff_member.surname,
                "name": staff.staff_member.name,
                "function": staff.staff_position,
                "position": staff.qualification,
                "note": staff.notes,
            }
            for i, staff in enumerate(staff_list)
        ]
        players_table_head = {
            "number": "№",
            "surname": "Фамилия",
            "name": "Имя",
            "birthday": "Д.Р.",
            "gender": "Пол",
            "position": "Квалификация",
            "diagnosis": "Диагноз",
        }

        players_table_data = [
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

        context["table_head"] = players_table_head
        context["table_data"] = players_table_data
        context["staff_table_head"] = staff_table_head
        context["staff_table_data"] = staff_table_data
        context["team"] = team

        return context


class TeamListView(LoginRequiredMixin, ListView):
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


class UpdateTeamView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
        UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "main/users/user_update.html"
    success_url = '/teams/'
    permission_required = 'team.change_team'

    def get_object(self, queryset=None):
        team_id = self.kwargs.get("team_id")
        return get_object_or_404(Team, pk=team_id)

    def get_context_data(self, **kwargs):
        context = super(UpdateTeamView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(
            instance=self.object,
            initial=self.get_initial()
        )
        return context


class DeleteTeamView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
        DeleteView):
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
        CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'includes/user_create.html'
    permission_required = 'team.add_team'
    success_url = '/teams'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


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
