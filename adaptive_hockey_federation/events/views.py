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
from events.forms import EventForm
from events.models import Event, Team
from main.controllers.team_views import CityListMixin


class EventListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    """Временная view для отображения работы модели Event"""

    model = Event
    template_name = "main/competitions/competitions.html"
    permission_required = "events.list_view_event"
    permission_denied_message = (
        "Отсутствует разрешение на просмотр списка соревнований."
    )
    context_object_name = "events"
    paginate_by = 10
    ordering = ["id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = context["events"]
        table_data = []
        for event in events:
            table_data.append(
                {
                    "pk": event.pk,
                    "data": event.date_start,
                    "data_end": event.date_end,
                    "title": event.title,
                    "city": event.city,
                    "duration": event.period_duration,
                    "is_active": event.is_active,
                    "_ref_": {
                        "name": "Участники",
                        "type": "button",
                        "url": reverse(
                            "events:competitions_id", args=[event.pk]
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


class UpdateEventView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
    CityListMixin,
):
    """Обновление информации о соревнованиях."""

    model = Event
    form_class = EventForm
    template_name = "main/competitions/competition_update.html"
    permission_required = "events.change_event"
    permission_denied_message = (
        "Отсутствует разрешение на изменение карточки соревнований."
    )

    def get_success_url(self):
        return reverse_lazy(
            "events:competition_update", kwargs={"pk": self.object.pk}
        )

    def get_object(self, queryset=None):
        return get_object_or_404(Event, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super(UpdateEventView, self).get_context_data(**kwargs)
        context["form"] = self.form_class(
            instance=self.object, initial={"city": self.object.city.name}
        )
        context["cities"] = self.get_cities()
        return context


class DeleteEventView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление соревнований."""

    object = Event
    model = Event
    success_url = reverse_lazy("events:competitions")
    permission_required = "events.delete_event"
    permission_denied_message = (
        "Отсутствует разрешение на изменение карточки соревнований."
    )

    def get_object(self, queryset=None):
        return get_object_or_404(Event, id=self.kwargs["pk"])


class TeamsOnEvent(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    """Отображение команд, принимающих участие в соревновании."""

    model = Event
    template_name = "main/competitions_id/competitions_id.html"
    permission_required = "events.list_team_event"
    permission_denied_message = (
        "Отсутствует разрешение на просмотр списка команд на соревновании."
    )

    def get_success_url(self):
        return reverse_lazy(
            "events:competitions_id", kwargs={"pk": self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        teams = event.teams.all()
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
                    "events:competitions_id_delete", args=[event.id, team.id]
                ),
            }
            for team in teams
        ]
        context["table_data"] = teams_table_data
        return context


class DeleteTeamFromEvent(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    """Удаление команд из участия в соревновании."""

    object = Team
    model = Team
    permission_required = "events.delete_team_event"
    permission_denied_message = (
        "Отсутствует разрешение на удаление команд с соревнования."
    )

    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        event = get_object_or_404(Event, id=self.kwargs["event_id"])
        event.teams.remove(team)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            "events:competitions_id", kwargs={"pk": self.kwargs["event_id"]}
        )
