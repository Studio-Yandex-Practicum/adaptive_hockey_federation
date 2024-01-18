from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from main.forms import TeamForm
from main.models import Player, Team

# пример рендера таблиц, удалить после реализации вьюх
CONTEXT_EXAMPLE = {
    "table_head": {
        "id": "Идентификатор",
        "name": "Имя",
        "surname": "Фамилия",
    },
    "table_data": [
        {"id": 1, "name": "Иван", "surname": "Иванов"},
        {"id": 2, "name": "Пётр", "surname": "Петров"},
    ],
}


@login_required
def main(request):
    return render(request, "main/main.html")


class PlayersCardView(LoginRequiredMixin, ListView):
    model = Player
    template_name = "main/players.html"
    context_object_name = "players"
    paginate_by = 10
    fields = [
        "surname",
        "name",
        "birthday",
        "gender",
        "number",
        "discipline",
        "diagnosis",
    ]

    def get_queryset(self):
        return super().get_queryset().order_by("surname").values(*self.fields)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table_head = {}
        for field in self.fields:
            table_head[field] = Player._meta.get_field(field).verbose_name
        context["table_head"] = table_head
        return context


class TeamIdView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "main/teams_id.html"
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

        table_head = {
            "surname": "Фамилия",
            "name": "Имя",
            "birthday": "День рождения",
            "diagnosis": "Диагноз",
            "discipline": "Дисциплина",
            "gender": "Пол",
            "level_revision": "Уровень ревизии",
            "position": "Игровая позиция",
            "number": "Номер игрока",
        }

        table_data = [
            {
                "surname": player.surname,
                "name": player.name,
                "birthday": player.birthday,
                "diagnosis": player.diagnosis.name if player.diagnosis else None,
                "discipline": player.discipline if player.discipline else None,
                "gender": player.get_gender_display(),
                "level_revision": player.level_revision,
                "position": player.get_position_display(),
                "number": player.number,
            }
            for player in players
        ]

        context = {
            "table_head": table_head,
            "table_data": table_data,
            "team": team,
        }

        return context


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = "main/teams.html"
    context_object_name = "teams"
    paginate_by = 10
    ordering = ["id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = context["teams"]

        table_data = []
        for team in teams:
            team_data = {
                "name": team.name,
                "city": team.city,
                "staff_team_member": team.staff_team_member,
                "discipline_name": team.discipline_name,
                "curator": team.curator.get_full_name,
                "players": "",
                "_ref_": {
                    "name": "Игроки",
                    "type": "button",
                    "url": reverse("main:teams_id", args=[team.id]),
                },
            }
            players = Player.objects.filter(team=team)
            team_data["players"] = ", ".join(map(str, players))
            table_data.append(team_data)

        context["table_head"] = {
            "name": "Название",
            "city": "Город",
            "staff_team_member": "Сотрудник команды",
            "discipline_name": "Дисциплина",
            "curator": "Куратор",
            "players": "Состав",
            "players_reference": "Игроки",
        }
        context["table_data"] = table_data
        return context


@login_required
def competitions_id(request, id):
    return render(request, "main/competitions_id.html")


@login_required
def competitions(request):
    return render(request, "main/competitions.html")


@login_required
def analytics(request):
    return render(request, "main/analitics.html")


@login_required
def unloads(request):
    return render(request, "main/unloads.html")
