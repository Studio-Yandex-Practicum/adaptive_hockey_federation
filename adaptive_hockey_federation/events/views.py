from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from events.forms import EventForm, EventTeamForm
from events.models import Event, Team
from main.controllers.team_views import CityListMixin


class EventListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    """Представление списка соревнований."""

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
                    "is_active": event.is_in_process,
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
    """Обновление информации о соревновании."""

    model = Event
    form_class = EventForm
    template_name = "main/competitions/competition_update.html"
    permission_required = "events.change_event"
    permission_denied_message = (
        "Отсутствует разрешение на изменение карточки соревнований."
    )

    def get_success_url(self):
        return reverse_lazy(
            "events:competitions_id", kwargs={"pk": self.object.pk}
        )

    def get_object(self, queryset=None):
        return get_object_or_404(Event, id=self.kwargs["pk"])

    def get_initial(self):
        initial = {
            "city": self.object.city.name,
            "date_start": self.object.date_start.isoformat(),
            "date_end": self.object.date_end.isoformat(),
        }
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class AddTeamToEvent(
    LoginRequiredMixin, PermissionRequiredMixin, RedirectView
):
    """Представление добавления команды в соревнования.
    В данном виде не отображает какой-то отдельной страницы либо формы.
    Используется для обработки нажатия кнопки либо соответствующего
    post-запроса. Добавляет команду в соревнование, после чего делает
    редирект на страницу управления соответствующим
    соревнованием."""

    pattern_name = "events:competitions_id"
    http_method_names = ("post",)
    permission_required = "events.change_event"
    permission_denied_message = (
        "Отсутствует разрешение на изменение списка команд на соревновании."
    )

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "post":
            event = get_object_or_404(Event, id=kwargs["event_id"])
            team = get_object_or_404(Team, id=kwargs["pk"])
            event.teams.add(team)
        return super(AddTeamToEvent, self).dispatch(
            request, kwargs["event_id"]
        )


class DeleteTeamFromEvent(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    """Удаление команд из участия в соревновании."""

    object = Team
    model = Team
    permission_required = "events.change_event"
    permission_denied_message = (
        "Отсутствует разрешение на удаление команд с соревнования."
    )

    def get_object(self, queryset=None):
        team_in_event = get_object_or_404(
            Event.teams.through,
            event=self.kwargs["event_id"],
            team=self.kwargs["pk"],
        )
        return team_in_event

    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        event = get_object_or_404(Event, id=self.kwargs["event_id"])
        event.teams.remove(team)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            "events:competitions_id", kwargs={"pk": self.kwargs["event_id"]}
        )


class CreateEventView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView, CityListMixin
):
    """Представление создания соревнования."""

    model = Event
    form_class = EventForm
    template_name = "main/competitions/competition_create.html"
    permission_required = "events.add_event"

    def get_success_url(self):
        return reverse_lazy(
            "events:competitions_id", kwargs={"pk": self.object.pk}
        )

    def get_object(self, queryset=None):
        return get_object_or_404(Event, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super(CreateEventView, self).get_context_data(**kwargs)
        context["cities"] = self.get_cities()
        return context


@login_required()
@permission_required("events.list_team_event", raise_exception=True)
def event_team_manage_view(request, pk):
    """Представление для управления соревнованием.
    -   Отображает команды, участвующие в соревновании, доступные команды
        (т.е. те, которые в соревновании не участвуют),
    -   Позволяет добавлять команды в соревнование и удалять их из него.

    Использована вью-функция вместо вью-класса в связи с необходимостью
    более тонкой настройки формы для работы с промежуточной моделью.
    """

    event = get_object_or_404(Event, id=pk)

    def _get_table_data(
        event_instance: Event,
        team_queryset: QuerySet,
        button_name: str | None = None,
        button_url_name: str | None = None,
    ):
        data = [
            {
                "id": team.id,
                "name": team.name,
                "city": team.city,
                "discipline_name": team.discipline_name,
                "action_button": {
                    "name": button_name,
                    "url": reverse(
                        button_url_name,
                        kwargs={"event_id": event_instance.id, "pk": team.id},
                    ),
                },
            }
            for team in team_queryset
        ]
        return data

    def get_context():
        """Внутренний метод получения контекста."""
        # Команды, участвующие в соревнованиях
        teams_table_data = _get_table_data(
            event,
            event.teams.all(),
            button_name="Отстранить",
            button_url_name="events:competitions_id_delete",
        )

        # Команды, доступные для добавления к соревнованиям
        available_teams = Team.objects.exclude(event_teams=event)
        available_teams_table_data = _get_table_data(
            event,
            available_teams,
            button_name="Допустить",
            button_url_name="events:competitions_id_add",
        )

        _context = {
            "table_data": teams_table_data,
            "available_table_data": available_teams_table_data,
            "available_teams_list": list(
                available_teams.values_list("name", flat=True)
            ),
            "object": event,
        }
        return _context

    context = get_context()

    if request.method != "POST":
        context["form"] = EventTeamForm(event=event)
        return render(
            request, "main/competitions_id/competitions_id.html", context
        )

    form = EventTeamForm(request.POST, event=event)
    context["form"] = form

    if not form.is_valid():
        return render(
            request, "main/competitions_id/competitions_id.html", context
        )

    event_team = form.save(commit=False)
    event_team.event = event
    event_team.save()
    # return redirect("events:competitions_id", event.id)
    return render(
        request, "main/competitions_id/competitions_id.html", context
    )
