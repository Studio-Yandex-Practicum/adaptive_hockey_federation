from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView
from main.forms import PlayerForm
from main.models import Player


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


def player_id_deleted(request):
    return render(request, "main/player_id_deleted.html")
