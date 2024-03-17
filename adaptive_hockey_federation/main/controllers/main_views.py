from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.urls import reverse
from django.views.generic.list import ListView
from main.models import Player


class MainView(
    LoginRequiredMixin,
    ListView,
):
    """Main_view. Поиск игроков по фамилии/имени."""

    model = Player
    template_name = "main/home/main.html"
    context_object_name = "main"
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
        query = self.request.GET.get("search")
        search_vector = SearchVector("surname", "name")
        queryset = None
        if query:
            queryset = Player.objects.annotate(search=search_vector).filter(
                Q(surname__icontains=query) | Q(name__icontains=query)
            )

            queryset = (
                queryset.select_related("diagnosis")
                .select_related("discipline")
                .order_by("surname")
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search:
            table_head = {}
            for field in self.fields:
                if field != "id":
                    table_head[field] = Player._meta.get_field(
                        field
                    ).verbose_name
            context["table_head"] = table_head
            table_data = [
                {
                    "surname": player.surname,
                    "name": player.name,
                    "birthday": player.birthday,
                    "gender": player.get_gender_display(),
                    "number": player.number,
                    "discipline": (
                        player.discipline if player.discipline else None
                    ),
                    "diagnosis": (
                        player.diagnosis.name if player.diagnosis else None
                    ),
                    "url": reverse("main:player_id", args=[player.id]),
                    "id": player.pk,
                }
                for player in context["main"]
            ]
            context["table_data"] = table_data

        return context
