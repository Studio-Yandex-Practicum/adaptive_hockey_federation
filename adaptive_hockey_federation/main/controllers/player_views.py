from typing import Any

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Prefetch
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from core.constants import FileConstants
from core.utils import is_uploaded_file_valid
from main.controllers.utils import errormessage
from main.forms import PlayerForm, PlayerUpdateForm
from main.mixins import FileUploadMixin
from main.models import (
    Diagnosis,
    DisciplineLevel,
    DisciplineName,
    Player,
    Team,
)
from main.permissions import PlayerIdPermissionsMixin
from main.schemas.player_schema import (
    get_player_fields,
    get_player_fields_personal,
    get_player_table_data,
)
from unloads.utils import model_get_queryset


class PlayersListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    """Представление для работы со списком игроков."""

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
        "team",
    ]

    def get_queryset(self):
        """Получить набор QuerySet."""
        queryset = super().get_queryset()
        dict_param = dict(self.request.GET)
        dict_param = {k: v for k, v in dict_param.items() if v != [""]}
        if len(dict_param) > 1 and "search_column" in dict_param:
            queryset = model_get_queryset(
                "players",
                Player,
                dict_param,
                queryset,
            )

        return (
            queryset.select_related("diagnosis")
            .select_related("discipline_name")
            .order_by("surname")
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получить словарь context для шаблона страницы."""
        context = super().get_context_data(**kwargs)
        table_head = {}
        for field in self.fields:
            if field != "id":
                table_head[field] = Player._meta.get_field(field).verbose_name
        context["table_head"] = table_head
        context["table_data"] = get_player_table_data(context)
        return context


class DiagnosisListMixin:
    """Миксин для использования в видах редактирования и создания команд."""

    @staticmethod
    def get_diagnosis():
        """Возвращает список диагнозов из БД."""
        return Diagnosis.objects.values_list("name", flat=True)


class PlayerIDCreateView(
    LoginRequiredMixin,
    PlayerIdPermissionsMixin,
    CreateView,
    DiagnosisListMixin,
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
        """Запустить валидацию формы."""
        player = form.save()

        self.add_new_documents(
            player=player,
            new_files_names=self.request.POST.getlist("new_file_name[]"),
            new_files_paths=self.request.FILES.getlist("new_file_path[]"),
        )

        self.delete_documents(
            player=player,
            deleted_files_paths=self.request.POST.getlist(
                "deleted_file_path[]",
            ),
        )
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """Обработчик GET-запроса."""
        self.team_id = request.GET.get("team", None)
        if self.team_id is not None:
            self.initial = {"team": self.team_id}
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Получить словарь context для шаблона страницы."""
        context = super().get_context_data(**kwargs)
        if self.team_id is not None:
            context["team_id"] = self.team_id
        context["page_title"] = "Создание профиля нового игрока"
        context["diagnosis"] = self.get_diagnosis()
        context["file_resolution"] = ", ".join(
            ["." + res for res in FileConstants.FILE_RESOLUTION],
        )
        return context

    def get_success_url(self):
        """Перенаправить на указанный адрес при успешном создании."""
        if self.team_id is None:
            return reverse("main:players")
        else:
            return reverse("main:teams_id", kwargs={"team_id": self.team_id})

    def post(self, request, *args, **kwargs):
        """Обработчик POST-запроса."""
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
    """Представление для отображения отдельного игрока."""

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

    def get_object(self, queryset=None):
        """Получить объект по id или выбросить ошибку 404."""
        return get_object_or_404(Player, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        """Получить словарь context для шаблона страницы."""
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
    DiagnosisListMixin,
    UpdateView,
):
    """Представление для обновления игрока."""

    model = Player
    template_name = "main/player_id/player_id_create_edit.html"
    form_class = PlayerUpdateForm
    permission_required = "main.change_player"
    permission_denied_message = (
        "У Вас нет разрешения на изменение персональных данных игрока."
    )

    def get_success_url(self):
        """Перенаправить на указанный адрес при успешном обновлении."""
        return reverse(
            "main:player_id",
            kwargs={
                "pk": self.object.pk,
            },
        )

    def get_object(self, queryset=None):
        """Получить объект по id или выбросить ошибку 404."""
        return get_object_or_404(Player, id=self.kwargs["pk"])

    def get_initial(self):
        """Добавить в словарь initial объект диагноза."""
        initial = {
            "diagnosis": self.object.diagnosis.name,
        }
        return initial

    def get_context_data(self, **kwargs):
        """Получить словарь context для шаблона страницы."""
        context = super().get_context_data(**kwargs)
        player_documents = self.get_object().player_documemts.all()
        context["page_title"] = "Редактирование профиля игрока"
        context["player_documents"] = player_documents
        context["diagnosis"] = self.get_diagnosis()
        context["file_resolution"] = ", ".join(
            ["." + res for res in FileConstants.FILE_RESOLUTION],
        )
        context["help_text_role"] = "Команды игрока"
        return context

    def form_valid(self, form):
        """Запустить валидацию формы."""
        player = form.save()
        self.add_new_documents(
            player=player,
            new_files_names=self.request.POST.getlist("new_file_name[]"),
            new_files_paths=self.request.FILES.getlist("new_file_path[]"),
        )

        self.delete_documents(
            player=player,
            deleted_files_paths=self.request.POST.getlist(
                "deleted_file_path[]",
            ),
        )

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """Обработчик POST-запросов."""
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
    """Представление для удаления игрока."""

    model = Player
    object = Player
    success_url = reverse_lazy("main:players")
    permission_required = "main.delete_player"
    permission_denied_message = (
        "У Вас нет разрешения на удаление карточки игрока."
    )

    def get_object(self, queryset=None):
        """Получить объект по id или выбросить ошибку 404."""
        return get_object_or_404(Player, id=self.kwargs["pk"])


class PlayerGamesVideo(
    LoginRequiredMixin,
    PlayerIdPermissionsMixin,
    ListView,
):
    """Список видео игр с участием игрока."""

    model = Player
    template_name = "main/player_id/player_id_video_games.html"
    permission_required = "main.view_player"
    permission_denied_message = (
        "У Вас нет разрешения на просмотр видео игр с участием игрока."
    )
    context_object_name = "player"

    def get_queryset(self) -> Player | None:  # type: ignore[override]
        """Получить набор QuerySet с играми команды игрока."""
        teams_games = Prefetch(
            "team",
            queryset=Team.objects.prefetch_related("game_teams"),
        )
        player = Player.objects.prefetch_related(teams_games).filter(
            id=self.kwargs["pk"],
        )
        if not player.exists():
            raise Http404("Игрока не существует")
        return player.first()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Получить словарь context для шаблона страницы."""
        context = super().get_context_data(**kwargs)
        player = context["player"]
        data_key = ("pk", "name", "video_link")
        table_data = []
        for team in player.team.all():
            table_data.extend(
                [
                    {key: getattr(game, key) for key in data_key}
                    for game in team.game_teams.all()
                ],
            )

        context["table_head"] = {
            "pk": "Nr.",
            "name": "Название",
            "video_link": "Ссылка на видео",
        }
        context["table_data"] = table_data
        return context


def player_id_deleted(request):
    """View для отображения информации об успешном удалении игрока."""
    return render(request, "main/player_id/player_id_deleted.html")


def load_discipline_levels(request):
    """
    Представление для получения списка уровней дисциплин по ID дисциплины.

    Используется в формах создания/редактирования данных игрока.
    """
    discipline_level_id = request.GET.get("discipline_level_id")
    try:
        discipline_statuses = DisciplineLevel.objects.filter(
            discipline_name_id=discipline_level_id,
        ).all()
    except ValueError:
        return JsonResponse([], safe=False)
    else:
        return JsonResponse(
            list(discipline_statuses.values("id", "name")),
            safe=False,
        )


def filter_duscipline_search(request):
    """Представления для поиска, получения списка дисциплин."""
    disciplines = DisciplineName.objects.all().values("name")
    return JsonResponse(list(disciplines), safe=False)
