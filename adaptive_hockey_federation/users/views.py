from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from main.models import Team
from unloads.utils import model_get_queryset
from users.forms import CustomUserCreateForm, CustomUserUpdateForm
from users.schemas import USER_TABLE_HEAD
from users.utilits.send_mails import send_password_reset_email

User = get_user_model()


class UsersListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = User
    template_name = "main/users/list.html"
    permission_required = "users.list_view_user"
    permission_denied_message = (
        "Отсутствует разрешение на просмотр списка пользователей."
    )
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by("last_name")
        dict_param = dict(self.request.GET)

        dict_param = {k: v for k, v in dict_param.items() if v != [""]}
        if len(dict_param) > 1 and "search_column" in dict_param:
            queryset = model_get_queryset(
                "users", User, dict_param, queryset
            )

        return queryset.order_by("last_name")

    def get_context_data(self, **kwargs):
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
                }
            )
        context["table_head"] = USER_TABLE_HEAD
        context["table_data"] = table_data
        return context


class UpdateUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Вьюха редактирования пользователя
    """

    model = User
    form_class = CustomUserUpdateForm
    template_name = "main/users/user_create_edit.html"
    permission_required = "users.change_user"
    permission_denied_message = (
        "Отсутствует разрешение на изменение пользователя."
    )

    def get_success_url(self):
        return reverse("users:users")

    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактирование профиля пользователя"
        return context

    def form_valid(self, form):
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
    """
    Вьюха удаления пользователя
    """

    object = User
    model = User
    success_url = "/users"
    permission_required = "users.delete_user"
    permission_denied_message = (
        "Отсутствует разрешение на удаление пользователей."
    )


class CreateUserView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Вьюха создания пользователя
    """

    model = User
    form_class = CustomUserCreateForm
    template_name = "main/users/user_create_edit.html"
    success_url = "/users"
    permission_required = "users.add_user"
    permission_denied_message = (
        "Отсутствует разрешение на создание пользователей."
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Создание пользователя"
        return context

    def form_valid(self, form):
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
    """Вьюха изменения пароля пользователя"""

    success_url = reverse_lazy("users:users")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.user.save()
        return response
