from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from main.models import Player


class MainView(
    LoginRequiredMixin,
    ListView,
):
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
                or_lookup = Q(surname__icontains=search) | Q(
                    name__icontains=search
                )
                queryset = queryset.filter(or_lookup)
            else:
                search_fields = {
                    "surname": "surname",
                    "name": "name",
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
                "diagnosis": (
                    player.diagnosis.name if player.diagnosis else None
                ),  # Noqa
                "url": reverse("main:player_id", args=[player.id]),
                "id": player.pk,
            }
            for player in context["players"]
        ]

        context["table_data"] = table_data
        return context


@login_required
def main(request):
    return render(request, "main/home/main.html")


@login_required
def unloads(request):
    return render(request, "main/unloads/unloads.html")
