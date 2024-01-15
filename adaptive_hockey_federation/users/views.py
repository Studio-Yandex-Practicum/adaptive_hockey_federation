from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

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
                'name': user.get_full_name(),
                'date': user.date_joined,
                'role': user.role,
                'email': user.email,
                'phone': user.phone,
                'id': user.pk,
            })
        context['table_head'] = {
            'name': 'Имя',
            'date': 'Дата',
            'role': 'Роль',
            'email': 'Email',
            'phone': 'Телефон',
        }
        context['table_data'] = table_data
        return context
