from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.list import ListView
from main.models import Player, Team
from pprint import pprint
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


class PlayersCardView(LoginRequiredMixin, ListView):
    model = Player
    template_name = 'main/players.html'
    context_object_name = 'players'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('surname')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        players = context['players']

        for player in players:
            if player.team:
                player.team_name = player.team.name
            else:
                player.team_name = 'Нет команды'
            if player.discipline:
                player.discipline_name = player.discipline.name
            else:
                player.discipline_name = 'Нет дисциплины'
        pprint(context)
        return context


@login_required
def teams_id(request, id):
    return render(request, 'main/teams_id.html')


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'main/teams.html'
    context_object_name = 'teams'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = context['teams']
        table_head = {}
        for field in Team._meta.get_fields():
            if hasattr(field, 'verbose_name') and field.name != 'id':
                table_head[field.name] = field.verbose_name
        table_head['players'] = 'Состав'

        table_data = []
        for team in teams:
            team_data = {}
            for field in Team._meta.get_fields():
                if hasattr(field, 'verbose_name') and field.name != 'id':
                    team_data[field.name] = getattr(team, field.name)
            players = Player.objects.filter(team=team)
            team_data['players'] = ', '.join(map(str, players))
            table_data.append(team_data)

        context = {
            'table_head': table_head,
            'table_data': table_data
        }
        return context


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
