def set_team_curator(user, choice_team):
    """
    Функция назначения представителя команды
    """
    from main.models import Team

    Team.objects.filter(curator=user).update(curator=None)
    if choice_team is not None:
        team = Team.objects.get(id=choice_team.id)
        team.curator = user
        team.save()
