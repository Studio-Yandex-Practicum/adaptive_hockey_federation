# File path: adaptive_hockey_federation/users/urls.py
# Description: URL patterns для приложения users.

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

User = get_user_model()


@login_required
def users_list(request):
    template = 'users/list.html'
    users = User.objects.all()
    table_data = []
    for user in users:
        table_data.append({
            'name': user.first_name,
            'surname': user.last_name,
            'email': user.email,
        })
    context = {
        'table_head': {
            'name': 'Имя',
            'surname': 'Фамилия',
            'email': 'email',
        },
        'table_data': table_data,
    }
    return render(request, template, context)
