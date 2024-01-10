from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import CreateUserForm, UpdateUserForm

User = get_user_model()


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = context['users']
        table_data = []
        for user in users:
            table_data.append({
                'id': user.pk,
                'name': user.get_full_name(),
                'email': user.email,
                'phone': user.phone,
                'date': user.date_joined,
                'role': user.role
            })
        context['table_head'] = {
            'name': 'Имя',
            'date': 'Дата',
            'role': 'Роль',
            'email': 'Email',
            'phone': 'Телефон'
        }
        context['table_data'] = table_data
        return context


class UpdateUserView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        UpdateView):
    model = User
    template_name = 'includes/user_update.html'
    permission_required = 'users.change_user'
    form_class = UpdateUserForm
    success_url = '/users'


class DeleteUserView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        DeleteView):
    model = User
    success_url = reverse_lazy('users:users')
    permission_required = 'users.delete_user'


class CreateUserView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'includes/user_create.html'
    success_url = '/users'
    permission_required = 'users.create_user'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
