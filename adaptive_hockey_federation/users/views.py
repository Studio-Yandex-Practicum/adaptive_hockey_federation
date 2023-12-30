from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import UpdateUserForm

User = get_user_model()


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = context['users']
        table_data = []
        id_data = []

        for user in users:
            table_data.append({
                'id': user.pk,
                'name': user.first_name,
                'surname': user.last_name,
                'email': user.email,
            })
        context['table_head'] = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'email': 'Email',
        }
        context['table_data'] = table_data
        context['id_data'] = id_data
        return context


class UpdateUserView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        UpdateView):
    model = User
    template_name = 'users/list_update.html'
    permission_required = 'users.change_user'
    context_object_name = 'user'
    success_url = '/users'
    form_class = UpdateUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class DeleteUserView(
        LoginRequiredMixin,
        PermissionRequiredMixin,
        DeleteView):
    model = User
    success_url = reverse_lazy('users:list')
    permission_required = 'users.delete_user'
