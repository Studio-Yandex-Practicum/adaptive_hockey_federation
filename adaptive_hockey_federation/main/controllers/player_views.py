from core.constants import FILE_RESOLUTION
from core.utils import is_uploaded_file_valid
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from main.controllers.utils import errormessage
from main.forms import PlayerForm, PlayerUpdateForm
from main.mixins import FileUploadMixin
from main.models import Player
from main.permissions import PlayerIdPermissionsMixin
from main.schemas.player_schema import (
    SEARCH_FIELDS,
    get_player_fields,
    get_player_fields_personal,
    get_player_table_data,
)


class PlayersListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = Player
    template_name = "main/players/players.html"
    permission_required = "main.list_view_player"
    permission_denied_message = (
        "У Вас нет разрешения на просмотр списка игроков игрока."
    )
    context_object_name = "players"
    paginate_by = 10
    fields = [
        "id",
        "surname",
        "name",
        "birthday",
        "gender",
        "number",
        "discipline_name",
        "discipline_level",
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
                    | Q(diagnosis__name__icontains=search)
                )
                queryset = queryset.filter(or_lookup)
            else:
                search_fields = SEARCH_FIELDS
                lookup = {f"{search_fields[search_column]}__icontains": search}
                queryset = queryset.filter(**lookup)

        return (
            queryset.select_related("diagnosis")
            .select_related("discipline_name")
            .order_by("surname")
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        table_head = {}
        for field in self.fields:
            if field != "id":
                table_head[field] = Player._meta.get_field(field).verbose_name
        context["table_head"] = table_head
        context["table_data"] = get_player_table_data(context)
        return context


class PlayerIDCreateView(
    LoginRequiredMixin,
    PlayerIdPermissionsMixin,
    CreateView,
    FileUploadMixin,
):
    """Представление для создания нового игрока."""

    model = Player
    form_class = PlayerForm
    template_name = "main/player_id/player_id_create_edit.html"
    permission_required = "main.add_player"
    permission_denied_message = (
        "У Вас нет разрешения на создание карточки игрока."
    )
    team_id: int | None = None

    def form_valid(self, form):
        player = form.save()

        self.add_new_documents(
            player=player,
            new_files_names=self.request.POST.getlist("new_file_name[]"),
            new_files_paths=self.request.FILES.getlist("new_file_path[]"),
        )

        self.delete_documents(
            player=player,
            deleted_files_paths=self.request.POST.getlist(
                "deleted_file_path[]"
            ),
        )
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.team_id = request.GET.get("team", None)
        if self.team_id is not None:
            self.initial = {"team": self.team_id}
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.team_id is not None:
            context["team_id"] = self.team_id
        context["page_title"] = "Создание профиля нового игрока"
        context["file_resolution"] = ", ".join(
            ["." + res for res in FILE_RESOLUTION]
        )
        return context

    def get_success_url(self):
        if self.team_id is None:
            return reverse("main:players")
        else:
            return reverse("main:teams_id", kwargs={"team_id": self.team_id})

    def post(self, request, *args, **kwargs):
        new_files_paths = self.request.FILES.getlist("new_file_path[]")
        for file in new_files_paths:
            if not is_uploaded_file_valid(file):
                details = PlayerForm(request.POST)
                return render(
                    request,
                    self.template_name,
                    {"form": details, "errormessage": errormessage},
                )

        self.team_id = request.POST.get("team_id", None)
        return super().post(request, *args, **kwargs)


class PlayerIdView(
    LoginRequiredMixin,
    PlayerIdPermissionsMixin,
    DetailView,
):
    model = Player
    template_name = "main/player_id/player_id.html"
    permission_required = "main.view_player"
    permission_denied_message = (
        "У Вас нет разрешения на просмотр карточки игрока."
    )
    context_object_name = "player"
    fields = [
        "surname",
        "name",
        "patronymic",
        "gender",
        "birthday",
        "discipline_name",
        "discipline_level",
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
    permission_required = "main.view_player"
    permission_denied_message = (
        "У Вас нет разрешения на просмотр персональных данных игрока."
    )

    def get_object(self, queryset=None):
        return get_object_or_404(Player, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = context["player"]
        player_documents = self.get_object().player_documemts.all()
        context["player_fields_personal"] = get_player_fields_personal(player)
        context["player_fields"] = get_player_fields(player)
        context["player_documents"] = player_documents
        return context


class PlayerIDEditView(
    LoginRequiredMixin,
    FileUploadMixin,
    PlayerIdPermissionsMixin,
    UpdateView,
):
    model = Player
    template_name = "main/player_id/player_id_create_edit.html"
    form_class = PlayerUpdateForm
    permission_required = "main.change_player"
    permission_denied_message = (
        "У Вас нет разрешения на изменение персональных данных игрока."
    )

    def get_success_url(self):
        return reverse(
            "main:player_id",
            kwargs={
                "pk": self.object.pk,
            },
        )

    def get_object(self, queryset=None):
        return get_object_or_404(Player, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player_documents = self.get_object().player_documemts.all()
        context["page_title"] = "Редактирование профиля игрока"
        context["player_documents"] = player_documents
        context["file_resolution"] = ", ".join(
            ["." + res for res in FILE_RESOLUTION]
        )
        return context

    def form_valid(self, form):
        player = form.save()

        self.add_new_documents(
            player=player,
            new_files_names=self.request.POST.getlist("new_file_name[]"),
            new_files_paths=self.request.FILES.getlist("new_file_path[]"),
        )

        self.delete_documents(
            player=player,
            deleted_files_paths=self.request.POST.getlist(
                "deleted_file_path[]"
            ),
        )

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        new_files_paths = self.request.FILES.getlist("new_file_path[]")
        player_documents = self.get_object().player_documemts.all()
        for file in new_files_paths:
            if not is_uploaded_file_valid(file):
                details = PlayerForm(request.POST)
                return render(
                    request,
                    self.template_name,
                    {
                        "form": details,
                        "errormessage": errormessage,
                        "player_documents": player_documents,
                    },
                )
        self.team_id = request.POST.get("team_id", None)
        return super().post(request, *args, **kwargs)


class PlayerIDDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = Player
    object = Player
    success_url = reverse_lazy("main:players")
    permission_required = "main.delete_player"
    permission_denied_message = (
        "У Вас нет разрешения на удаление карточки игрока."
    )

    def get_object(self, queryset=None):
        return get_object_or_404(Player, id=self.kwargs["pk"])


def player_id_deleted(request):
    return render(request, "main/player_id_deleted.html")
