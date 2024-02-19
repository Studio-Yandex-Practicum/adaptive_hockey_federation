from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from main.forms import TeamForm
from main.models import Player, Team


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
                if player.diagnosis
                else None,
                "discipline": player.discipline if player.discipline else None,
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


class UpdateTeamView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "main/users/user_update.html"
    success_url = "/teams/"
    permission_required = "team.change_team"

    def get_object(self, queryset=None):
        team_id = self.kwargs.get("team_id")
        return get_object_or_404(Team, pk=team_id)

    def get_context_data(self, **kwargs):
        context = super(UpdateTeamView, self).get_context_data(**kwargs)
        context["form"] = self.form_class(
            instance=self.object, initial=self.get_initial()
        )
        return context


class DeleteTeamView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    object = Team
    model = Team
    success_url = "/teams/"
    permission_required = "team.delete_team"

    def get_object(self, queryset=None):
        team_id = self.kwargs.get("team_id")
        return get_object_or_404(Team, pk=team_id)


class CreateTeamView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = "includes/user_create.html"
    permission_required = "team.add_team"
    success_url = "/teams"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
