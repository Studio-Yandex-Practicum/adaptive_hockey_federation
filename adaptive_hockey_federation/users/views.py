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
from users.forms import CustomUserForm
from users.utilits.reset_password import send_password_reset_email
from users.utils import set_team_curator

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
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            search_column = self.request.GET.get("search_column")
            if not search_column or search_column.lower() in ["все", "all"]:
                or_lookup = (
                    Q(first_name__icontains=search)
                    | Q(last_name__icontains=search)
                    | Q(date_joined__icontains=search)
                    | Q(role__icontains=search)
                    | Q(email__icontains=search)
                    | Q(phone__icontains=search)
                )
                queryset = queryset.filter(or_lookup)
            else:
                search_fields = {
                    "date": "date_joined",
                    "role": "role",
                    "email": "email",
                    "phone": "phone",
                }
                if search_column == "name":
                    queryset = queryset.filter(
                        Q(first_name__icontains=search)
                        | Q(last_name__icontains=search)
                    )
                else:
                    queryset = queryset.filter(
                        **{
                            f"{search_fields[search_column]}__icontains": search  # noqa
                        }
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
        context["table_head"] = {
            "name": "Имя",
            "date": "Дата регистрации",
            "role": "Роль",
            "email": "Email",
            "phone": "Телефон",
        }
        context["table_data"] = table_data
        return context


class UpdateUserView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    """
    Вьюха редактирования пользователя
    """

    model = User
    form_class = CustomUserForm
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
            set_team_curator(user, form.cleaned_data["team"])
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
    form_class = CustomUserForm
    template_name = "main/users/user_create_edit.html"
    success_url = "/users"
    permission_required = "users.add_user"
    permission_denied_message = (
        "Отсутствует разрешение на создание пользователей."
    )

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            send_password_reset_email(user)
            set_team_curator(user, form.cleaned_data["team"])
        return super().form_valid(form)


class PasswordSetView(PasswordResetConfirmView):
    """Вьюха изменения пароля пользователя"""

    success_url = reverse_lazy("users:users")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.user.save()
        return response
