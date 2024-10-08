from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.auth.views import PasswordResetConfirmView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from main.models import Team
from users.forms import CustomUserCreateForm, CustomUserUpdateForm
from users.utilits.send_mails import send_password_reset_email

User = get_user_model()


class UsersListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    """Представление для получения списка пользователей."""

    model = User
    template_name = "main/users/list.html"
    permission_required = "users.list_view_user"
    permission_denied_message = (
        "Отсутствует разрешение на просмотр списка пользователей."
    )
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        """Получить набор QuerySet."""
        queryset = super().get_queryset().order_by("last_name")
        search_params = self.request.GET.dict()
        search_column = search_params.get("search_column")
        search = search_params.get("search")
        if search_column:
            if search_column and search_column.lower() in ["все", "all"]:
                or_lookup = (
                    Q(first_name__icontains=search)
                    | Q(last_name__icontains=search)
                    | Q(patronymic__icontains=search)
                    | Q(role__icontains=search)
                    | Q(email__icontains=search)
                    | Q(phone__icontains=search)
                    | Q(date_joined__icontains=search)
                )
                queryset = queryset.filter(or_lookup)
            elif search_column == "name":
                queryset = queryset.filter(
                    Q(first_name__icontains=search)
                    | Q(last_name__icontains=search)
                    | Q(patronymic__icontains=search),
                )
            elif search_column == "date":
                queryset = queryset.filter(
                    Q(date_joined__year__icontains=search_params["year"])
                    & Q(
                        date_joined__month__icontains=search_params[
                            "month"
                        ].lstrip("0"),
                    )
                    & Q(
                        date_joined__day__icontains=search_params[
                            "day"
                        ].lstrip("0"),
                    ),
                )
            else:
                search_fields = {
                    "role": "role",
                    "email": "email",
                    "phone": "phone",
                }
                queryset = queryset.filter(
                    **{f"{search_fields[search_column]}__icontains": search},
                )
        return queryset.order_by("last_name")

    def get_context_data(self, **kwargs):
        """Получить словарь context для шаблона страницы."""
        context = super().get_context_data(**kwargs)
        users = context["users"]
        table_data = []
        for user in users:
            table_data.append(
                {
                    "name": user.get_full_name(),
                    "date": user.date_joined,
                    "role": user.get_role_display(),
                    "email": user.email,
                    "phone": user.phone,
                    "id": user.pk,
                },
            )
        context["table_head"] = {
            "name": "Имя",
            "date": "Дата регистрации",
            "role": "Роль",
            "email": "Email",
            "phone": "Телефон",
        }
        context["table_data"] = table_data
        return context


class UpdateUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Представление для обновления пользователя."""

    model = User
    form_class = CustomUserUpdateForm
    template_name = "main/users/user_create_edit.html"
    permission_required = "users.change_user"
    permission_denied_message = (
        "Отсутствует разрешение на изменение пользователя."
    )

    def get_success_url(self):
        """Перенаправить на указанный адрес при успешном обновлении."""
        return reverse("users:users")

    def get_object(self, queryset=None):
        """Получить объект по id или выбросить ошибку 404."""
        return get_object_or_404(User, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        """Получить словарь context для шаблона страницы."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактирование профиля пользователя"
        return context

    def form_valid(self, form):
        """Запустить валидацию формы."""
        if form.is_valid():
            user = form.save()
            Team.objects.filter(curator=user).update(curator=None)
            choice_teams = form.cleaned_data["team"]
            if choice_teams is not None:
                for team in choice_teams:
                    team.curator = user
                    team.save()
        return super().form_valid(form)


class DeleteUserView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Представление для удаления пользователя."""

    object = User
    model = User
    success_url = "/users"
    permission_required = "users.delete_user"
    permission_denied_message = (
        "Отсутствует разрешение на удаление пользователей."
    )


class CreateUserView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представление для создания пользователя."""

    model = User
    form_class = CustomUserCreateForm
    template_name = "main/users/user_create_edit.html"
    success_url = "/users"
    permission_required = "users.add_user"
    permission_denied_message = (
        "Отсутствует разрешение на создание пользователей."
    )

    def get_context_data(self, **kwargs):
        """Получить словарь context для шаблона страницы."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Создание пользователя"
        return context

    def form_valid(self, form):
        """Запустить валидацию формы."""
        if form.is_valid():
            user = form.save()
            choice_teams = form.cleaned_data["team"]
            if choice_teams is not None:
                for team in choice_teams:
                    team.curator = user
                    team.save()
            send_password_reset_email(user)
        return super().form_valid(form)


class PasswordSetView(PasswordResetConfirmView):
    """Представление для изменения пароля пользователя."""

    success_url = reverse_lazy("users:users")

    def form_valid(self, form):
        """Запустить валидацию формы."""
        response = super().form_valid(form)
        self.user.save()
        return response
