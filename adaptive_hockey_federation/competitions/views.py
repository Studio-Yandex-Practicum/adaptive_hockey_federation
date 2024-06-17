from competitions.forms import (
    CompetitionForm,
    CompetitionTeamForm,
    CompetitionUpdateForm,
)
from competitions.models import Competition, Team
from competitions.schema import (
    get_competitions_table_data,
    get_competitions_table_head,
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.db.models import Case, F, Q, QuerySet, Value, When
from django.db.models.functions import Now
from django.db.models.lookups import GreaterThan, LessThan
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    DeletionMixin,
    UpdateView,
)
from django.views.generic.list import ListView
from main.controllers.team_views import CityListMixin
from main.controllers.utils import get_team_href
from users.utilits.send_mails import send_welcome_mail


class CompetitionListView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    ListView,
):
    """Представление списка соревнований."""

    model = Competition
    template_name = "main/competitions/competitions.html"
    context_object_name = "competitions"
    paginate_by = 10
    ordering = ["id"]

    def test_func(self):
        """Проверка, что пользователь является представителем команды."""
        user = self.request.user
        return user.is_authenticated and (
            user.is_agent or user.is_superuser or user.is_admin
        )

    def get_permission_denied_message(self):
        """Сообщение об отказе в доступе."""
        return "Отсутствует разрешение на просмотр списка соревнований."

    def handle_no_permission(self):
        """Обработка ситуации, когда у пользователя нет прав."""
        if not self.request.user.is_authenticated:
            return redirect_to_login(
                self.request.get_full_path(),
                self.get_login_url(),
                self.get_redirect_field_name(),
            )
        else:
            raise PermissionDenied(self.get_permission_denied_message())

    def get_queryset(self):
        """Метод для получения QuerySet с заданными параметрами."""
        queryset = super().get_queryset()
        search_params = self.request.GET.dict()
        search_column = search_params.get("search_column")
        search = search_params.get("search")
        if search_column:
            if search_column.lower() in ["все", "all"]:
                queryset = queryset.filter(
                    Q(title__icontains=search)
                    | Q(city__name__icontains=search)
                    | Q(date_start__icontains=search)
                    | Q(date_end__icontains=search)
                    | Q(pk__icontains=search),
                )
            elif search_column == "title":
                queryset = queryset.filter(title__icontains=search)
            elif search_column == "city":
                queryset = queryset.filter(city__name__icontains=search)
            elif search_column == "is_active":
                queryset = queryset.annotate(
                    is_active_view=Case(
                        When(
                            LessThan(F("date_start"), Now())
                            & GreaterThan(F("date_end"), Now()),
                            then=Value("true"),
                        ),
                        default=Value("false"),
                    ),
                ).filter(is_active_view__icontains=search_params["active"])
            elif search_column == "teams":
                queryset = queryset.filter(teams__name__icontains=search)
            elif search_column == "date":
                queryset = queryset.filter(
                    Q(date_start__year__icontains=search_params["year"])
                    & Q(
                        date_start__month__icontains=search_params[
                            "month"
                        ].lstrip("0"),
                    )
                    & Q(
                        date_start__day__icontains=search_params["day"].lstrip(
                            "0",
                        ),
                    ),
                )
            elif search_column == "date_end":
                queryset = queryset.filter(
                    Q(date_end__year__icontains=search_params["year"])
                    & Q(
                        date_end__month__icontains=search_params[
                            "month"
                        ].lstrip("0"),
                    )
                    & Q(
                        date_end__day__icontains=search_params["day"].lstrip(
                            "0",
                        ),
                    ),
                )
        return queryset

    def get_context_data(self, **kwargs):
        """Метод для получения словаря context в шаблоне страницы."""
        context = super().get_context_data(**kwargs)
        competitions = context["competitions"]
        context["page_title"] = "Редактирование соревнование"
        context["table_head"] = get_competitions_table_head
        context["table_data"] = get_competitions_table_data(competitions)
        return context


class UpdateCompetitionView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
    CityListMixin,
):
    """Обновление информации о соревновании."""

    model = Competition
    form_class = CompetitionUpdateForm
    template_name = "main/competitions/competition_create_edit.html"
    permission_required = "competitions.change_competition"
    permission_denied_message = (
        "Отсутствует разрешение на изменение карточки соревнований."
    )

    def get_success_url(self):
        """Перенаправить на указанный адрес при успешном обновлении."""
        return reverse_lazy(
            "competitions:competition_id",
            kwargs={"pk": self.object.pk},
        )

    def get_object(self, queryset=None):
        """Получить объект по id или вызвать ошибку 404."""
        return get_object_or_404(Competition, id=self.kwargs["pk"])

    def get_initial(self):
        """Вернуть словарь initial с указанными атрибутами объекта."""
        initial = {
            "city": self.object.city.name,
            "date_start": self.object.date_start.isoformat(),
            "date_end": self.object.date_end.isoformat(),
        }
        return initial

    def get_context_data(self, **kwargs):
        """Метод для получения словаря context в шаблоне страницы."""
        context = super().get_context_data(**kwargs)
        context["cities"] = self.get_cities()
        context["page_title"] = "Редактирование соревнования"
        return context


class DeleteCompetitionView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    """Удаление соревнований."""

    object = Competition
    model = Competition
    success_url = reverse_lazy("competitions:competitions")
    permission_required = "competitions.delete_competition"
    permission_denied_message = (
        "Отсутствует разрешение на изменение карточки соревнований."
    )

    def get_object(self, queryset=None):
        """Получить объект по id или вызвать ошибку 404."""
        return get_object_or_404(Competition, id=self.kwargs["pk"])


class AddTeamToCompetition(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    RedirectView,
):
    """
    Представление добавления команды в соревнования.

    В данном виде не отображает какой-то отдельной страницы либо формы.
    Используется для обработки нажатия кнопки либо соответствующего
    post-запроса. Добавляет команду в соревнование, после чего делает
    редирект на страницу управления соответствующим
    соревнованием.
    """

    pattern_name = "competitions:competition_id"
    http_method_names = ("post",)
    permission_required = "competitions.change_competition"
    permission_denied_message = (
        "Отсутствует разрешение на изменение списка команд на соревновании."
    )

    def dispatch(self, request, *args, **kwargs):
        """Обработать POST-запрос или вернуть на страницу соревнования."""
        if request.method.lower() == "post":
            competition = get_object_or_404(
                Competition,
                id=kwargs["competition_id"],
            )
            team = get_object_or_404(Team, id=kwargs["pk"])
            competition.teams.add(team)
            if team.curator and team.curator.email:
                send_welcome_mail(
                    team=team,
                    competition=competition,
                    curator_email=team.curator.email,
                )
        return super(AddTeamToCompetition, self).dispatch(
            request,
            kwargs["competition_id"],
        )


class DeleteTeamFromCompetition(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    View,
    DeletionMixin,
    SingleObjectMixin,
):
    """Удаление команд из участия в соревновании."""

    object = Competition.teams.through
    model = Competition.teams.through
    permission_required = "competitions.change_competition"
    permission_denied_message = (
        "Отсутствует разрешение на удаление команд с соревнования."
    )

    def get_object(self, queryset=None):
        """Получить объект по атрибутам или вызвать ошибку 404."""
        team_in_competition = get_object_or_404(
            Competition.teams.through,
            competition=self.kwargs["competition_id"],
            team=self.kwargs["pk"],
        )
        return team_in_competition

    def get_success_url(self):
        """Перенаправить на указанный адрес при успешном обновлении."""
        return reverse_lazy(
            "competitions:competition_id",
            kwargs={"pk": self.kwargs["competition_id"]},
        )


class CreateCompetitionView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
    CityListMixin,
):
    """Представление создания соревнования."""

    model = Competition
    form_class = CompetitionForm
    template_name = "main/competitions/competition_create_edit.html"
    permission_required = "competitions.add_competition"

    def get_success_url(self):
        """Перенаправить на указанный адрес при успешном обновлении."""
        return reverse_lazy(
            "competitions:competition_id",
            kwargs={"pk": self.object.pk},
        )

    def get_object(self, queryset=None):
        """Получить объект по id или вызвать ошибку 404."""
        return get_object_or_404(Competition, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        """Метод для получения словаря context в шаблоне страницы."""
        context = super(CreateCompetitionView, self).get_context_data(**kwargs)
        context["cities"] = self.get_cities()
        context["page_title"] = "Создать соревнование"
        return context

    def post(self, request, *args, **kwargs):
        """
        Обработать POST-запрос.

        1. Создать экземпляр формы с переданными атрибутами
        2. Вызвать валидацию полей формы.
        """
        self.disciplines = request.POST.get("disciplines", None)
        return super().post(request, *args, **kwargs)


def check_permissions(user):
    """
    Проверка прав пользователя.

    Доступ для:
    1. Представителя команды
    2. Администратора.
    """
    return user.is_authenticated and (
        user.is_agent or user.is_superuser or user.is_admin
    )


@login_required()
@user_passes_test(
    check_permissions,
    login_url="login",
    redirect_field_name=None,
)
def competition_team_manage_view(request, pk):
    """
    Представление для управления соревнованием.

    -   Отображает команды, участвующие в соревновании, доступные команды
        (т.е. те, которые в соревновании не участвуют),
    -   Позволяет добавлять команды в соревнование и удалять их из него.

    Использована вью-функция вместо вью-класса в связи с необходимостью
    более тонкой настройки формы для работы с промежуточной моделью.
    """
    competition = get_object_or_404(
        Competition.objects.prefetch_related("teams"),
        id=pk,
    )

    def _get_table_data(
        competition_instance: Competition,
        team_queryset: QuerySet,
        button_name: str | None = None,
        button_url_name: str | None = None,
    ):
        data = [
            {
                "id": team.id,
                "name": get_team_href(team),
                "city": team.city,
                "discipline_name": team.discipline_name,
                "action_button": {
                    "name": button_name,
                    "url": reverse(
                        button_url_name,
                        kwargs={
                            "competition_id": competition_instance.id,
                            "pk": team.id,
                        },
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
            competition,
            competition.teams.all(),
            button_name="Отстранить",
            button_url_name="competitions:competitions_id_delete",
        )

        # Команды, доступные для добавления к соревнованиям
        available_teams = Team.objects.exclude(competition_teams=competition)
        available_teams_table_data = _get_table_data(
            competition,
            available_teams,
            button_name="Допустить",
            button_url_name="competitions:competitions_id_add",
        )

        _context = {
            "table_data": teams_table_data,
            "available_table_data": available_teams_table_data,
            "available_teams_list": list(
                available_teams.values_list("name", flat=True),
            ),
            "object": competition,
        }
        return _context

    context = get_context()

    if request.method != "POST":
        context["form"] = CompetitionTeamForm(competition=competition)
        return render(
            request,
            "main/competitions_id/competitions_id.html",
            context,
        )

    form = CompetitionTeamForm(request.POST, competition=competition)
    context["form"] = form

    if not form.is_valid():
        return render(
            request,
            "main/competitions_id/competitions_id.html",
            context,
        )

    competition_team = form.save(commit=False)
    competition_team.competition = competition
    competition_team.save()
    return redirect("competitions:competition_id", competition.id)
