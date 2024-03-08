from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView
from main.controllers.team_views import CityListMixin
from competitions.forms import CompetitionForm
from competitions.models import Competition, Team


class CompetitionListView(
    LoginRequiredMixin,
    ListView
):
    """Временная view для отображения работы модели Competition"""

    model = Competition
    template_name = "main/competitions/competitions.html"
    context_object_name = "competitions"
    paginate_by = 10
    ordering = ["id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competitions = context["competitions"]
        table_data = []
        for competition in competitions:
            table_data.append(
                {
                    "pk": competition.pk,
                    "data": competition.date_start,
                    "data_end": competition.date_end,
                    "title": competition.title,
                    "city": competition.city,
                    "duration": competition.period_duration,
                    "is_active": competition.is_active,
                    "_ref_": {
                        "name": "Участники",
                        "type": "button",
                        "url": reverse(
                            "competitions:competitions_id", args=[
                                competition.pk
                            ]
                        ),
                    },
                }
            )

        context["table_head"] = {
            "pk": "Nr.",
            "data": "Начало соревнований",
            "data_end": "Конец соревнований",
            "title": "Наименование",
            "city": "Город",
            "duration": "Длительность",
            "is_active": "Активно",
            "teams": "Участники",
        }
        context["table_data"] = table_data
        return context


class UpdateCompetitionView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
    CityListMixin
):
    """Обновление информации о соревнованиях."""

    model = Competition
    form_class = CompetitionForm
    template_name = "main/competitions/competition_update.html"
    permission_required = "competitions.competition_update"

    def get_success_url(self):
        return reverse_lazy(
            "competitions:competition_update", kwargs={"pk": self.object.pk}
        )

    def get_object(self, queryset=None):
        return get_object_or_404(Competition, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super(UpdateCompetitionView, self).get_context_data(**kwargs)
        context["form"] = self.form_class(
            instance=self.object, initial={"city": self.object.city.name}
        )
        context["cities"] = self.get_cities()
        return context


class DeleteCompetitionView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    """Удаление соревнований."""

    object = Competition
    model = Competition
    success_url = reverse_lazy("competitions:competitions")
    permission_required = "competitions.competition_delete"

    def get_object(self, queryset=None):
        return get_object_or_404(Competition, id=self.kwargs["pk"])


class TeamsOnCompetition(DetailView):
    """Отображение команд, принимающих участие в соревновании."""

    model = Competition
    template_name = "main/competitions_id/competitions_id.html"

    def get_success_url(self):
        return reverse_lazy(
            "competitions:competitions_id", kwargs={"pk": self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        competition = self.get_object()
        teams = competition.teams.all()
        teams_table_data = [
            {
                "id": team.id,
                "name": team.name,
                "city": team.city,
                "discipline_name": team.discipline_name,
                "ref": {
                    "name": "Посмотреть",
                    "type": "button",
                    "url": reverse("main:teams_id", args=[team.id]),
                },
                "delete_url": reverse(
                    "competitions:competitions_id_delete", args=[
                        competition.id,
                        team.id
                    ]
                ),
            }
            for team in teams
        ]
        context["table_data"] = teams_table_data
        return context


class DeleteTeamFromCompetition(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    """Удаление команд из участия в соревновании."""

    object = Team
    model = Team
    permission_required = "competitions.competitions_id_delete"

    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        competition = get_object_or_404(
            Competition, id=self.kwargs["competition_id"]
        )
        competition.teams.remove(team)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            "competitions:competitions_id", kwargs={
                "pk": self.kwargs["competition_id"]
            }
        )
