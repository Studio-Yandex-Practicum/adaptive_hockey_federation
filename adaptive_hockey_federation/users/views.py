from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.auth.views import PasswordResetConfirmView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from users.forms import UpdateUserForm, UsersCreationForm

User = get_user_model()


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'main/users/list.html'
    context_object_name = 'users'
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
                    "phone": "phone"
                }
                if search_column == "name":
                    queryset = queryset.filter(
                        Q(first_name__icontains=search)
                        | Q(last_name__icontains=search)
                    )
                else:
                    queryset = queryset.filter(**{
                        f"{search_fields[search_column]}__icontains": search
                    })

        return (
            queryset
            .order_by("last_name")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = context['users']
        table_data = []
        for user in users:
            table_data.append({
                'name': user.get_full_name(),
                'date': user.date_joined,
                'role': user.get_role_display(),
                'email': user.email,
                'phone': user.phone,
                'id': user.pk,
            })
        context['table_head'] = {
            'name': 'Имя',
            'date': 'Дата регистрации',
            'role': 'Роль',
            'email': 'Email',
            'phone': 'Телефон',
        }
        context['table_data'] = table_data
        return context


class UpdateUserView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        UpdateView):
    """
    Вьюха редактирования пользователя
    """
    model = User
    template_name = 'main/users/user_update.html'
    permission_required = 'users.change_user'
    form_class = UpdateUserForm
    success_url = '/users'

    def get_context_data(self, **kwargs):
        context = super(UpdateUserView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(
            instance=self.object,
            initial=self.get_initial()
        )
        return context


class DeleteUserView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        DeleteView):
    """
    Вьюха удаления пользователя
    """
    object = User
    model = User
    success_url = '/users'
    permission_required = 'users.delete_user'


class CreateUserView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        CreateView):
    """
    Вьюха создания пользователя
    """
    model = User
    form_class = UsersCreationForm
    template_name = 'main/users/user_create.html'
    success_url = '/users'
    permission_required = 'users.create_user'


class PasswordSetView(PasswordResetConfirmView):
    """Вьюха изменения пароля пользователя"""
    success_url = reverse_lazy("users:users")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.user.save()
        return response
