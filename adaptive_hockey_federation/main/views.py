from django.shortcuts import render

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


def main(request):
    return render(request, 'main/main.html')


def users(request):
    return render(request, 'main/users.html')


def teams_id(request, id):
    return render(request, 'main/teams_id.html')


def teams(request):
    return render(request, 'main/teams.html', CONTEXT_EXAMPLE)


def competitions_id(request, id):
    return render(request, 'main/competitions_id.html')


def competitions(request):
    return render(request, 'main/competitions.html')


def analytics(request):
    return render(request, 'main/analitics.html')


def unloads(request):
    return render(request, 'main/unloads.html')
