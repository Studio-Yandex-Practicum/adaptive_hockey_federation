from django.contrib.auth.mixins import LoginRequiredMixin
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
                    "url": '',
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
