from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from events.models import Event


class EventListView(LoginRequiredMixin, ListView):
    """Временная view для отображения работы модели Event"""
    model = Event
    template_name = "main/competitions/competitions.html"
    context_object_name = "events"
    paginate_by = 10
    ordering = ["id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = context["events"]
        table_data = []
        for event in events:
            table_data.append({
                "Nr.": event.pk,
                "data": event.date_start,
                "title": event.title,
                "city": event.city,
                "duration": event.period_duration,
                "is_active": event.is_active,
                "_ref_": {
                    "name": "Состав",
                    "type": "button",
                    "url": reverse("events:competitions_id", args=[event.pk]),
                },
            })

        context["table_head"] = {
            "id": "Nr.",
            "data": "Дата",
            "title": "Наименование",
            "city": "Город",
            "duration": "Длительность",
            "is_active": "Активно",
            "teams": "Состав",
        }
        context["table_data"] = table_data
        return context


class TeamsOnEvent(DetailView):
    """Отображение команд, принимающих участие в соревновании."""

    model = Event
    template_name = "main/competitions_id/competitions_id.html"
    # success_url = "/competitions/"

    def get_success_url(self):
        return reverse_lazy(
            'events:competitions_id', kwargs={'pk': self.object.pk}
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
                    "name": "Игроки",
                    "type": "button",
                    "url": reverse("main:teams_id", args=[team.id]),
                },
            }
            for team in teams
        ]
        context["table_data"] = teams_table_data
        return context
