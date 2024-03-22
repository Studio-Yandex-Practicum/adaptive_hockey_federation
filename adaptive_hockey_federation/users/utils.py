def set_team_curator(user, choice_team):
    """
    Функция назначения представителя команды
    """
    from main.models import Team

    Team.objects.filter(curator=user).update(curator=None)
    if choice_team:
        team_objects = list(choice_team)
        for team in team_objects:
            team.curator = user
        Team.objects.bulk_update(team_objects, ["curator"])
