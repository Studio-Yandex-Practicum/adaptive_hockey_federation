from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.models import Team

# пример рендера таблиц, удалить после реализации вьюх
CONTEXT_EXAMPLE = {
    'table_head': {
        'id': 'Идентификатор',
        'name': 'Имя',
        'surname': 'Фамилия',
    },
    'table_data': [
        {'id': 1, 'name': 'Иван', 'surname': 'Иванов'},
        {'id': 2, 'name': 'Пётр', 'surname': 'Петров'},
    ],
}


@login_required
def main(request):
    return render(request, 'main/main.html')


@login_required
def users(request):
    return render(request, 'main/users.html')


@login_required
def teams_id(request, id):
    return render(request, 'main/teams_id.html')


@login_required
def teams(request):
    list_teams = Team.objects.all()
    context = {
        'table_head': {
            'name': 'Название команды',
            'city': 'Город',
            'discipline_name': 'Дисциплина',
            'staff_team_member': 'Сотрудник команды'
        },
        'table_data': [],
    }

    for team in list_teams:
        context['table_data'].append({
            'name': team.name,
            'city': team.city,
            'discipline_name': team.discipline_name,
            'staff_team_member': team.staff_team_member,
        })
    return render(request, 'main/teams.html', context)


@login_required
def competitions_id(request, id):
    return render(request, 'main/competitions_id.html')


@login_required
def competitions(request):
    return render(request, 'main/competitions.html')


@login_required
def analytics(request):
    return render(request, 'main/analitics.html')


@login_required
def unloads(request):
    return render(request, 'main/unloads.html')
