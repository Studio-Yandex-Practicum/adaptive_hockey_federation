def set_default_permission_group(sender, **kwargs) -> None:
    """Функция для назначение прав группам пользователей"""
    from django.contrib.auth.models import Permission
    from users.constants import AGENTS_PERMS, GROUP_NAMES, MODERATORS_PERMS
    from users.models import ProxyGroup

    for group in GROUP_NAMES:
        group_obj, created = ProxyGroup.objects.get_or_create(name=group)
        if group == "Администраторы":
            for perm in Permission.objects.all():
                group_obj.permissions.add(perm)
        elif group == "Модераторы":
            for codename in MODERATORS_PERMS:
                group_obj.permissions.add(
                    Permission.objects.get(codename=codename)
                )
        elif group == "Представители команд":
            for codename in AGENTS_PERMS:
                group_obj.permissions.add(
                    Permission.objects.get(codename=codename)
                )
        group_obj.save()


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
