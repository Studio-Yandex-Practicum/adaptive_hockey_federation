from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.models import AnonymousUser
from main.models import Player
from users.models import User


def agent_has_player_permission(user: User | AnonymousUser, player: Player):
    """Проверка, имеет ли представитель право доступа к игроку.
    Проверяет только пользователей с role == agent. Остальным просто выдает
    разрешение."""
    if isinstance(user, AnonymousUser):
        return False
    if not user.is_agent:
        return True
    return player.team.filter(curator=user).exists()


class CustomPermissionMixin(PermissionRequiredMixin, UserPassesTestMixin):
    """Миксин, объединяющий функционал миксинов-родителей.

    PermissionRequiredMixin и UserPassesTestMixin имеют общего родителя
    AccessMixin и оба переопределяют родительский метод dispatch(), в связи с
    чем их одновременное прямое использование во вью-классе невозможно.

    Данный класс позволяет обойти это ограничение.

    !!! Во вью-классе или классе-наследнике необходимо переопределить метод
        test_func() либо get_test_func()."""

    def dispatch(self, request, *args, **kwargs):
        if not (
            PermissionRequiredMixin.has_permission(self)
            and UserPassesTestMixin.get_test_func(self)()
        ):
            return self.handle_no_permission()
        return super(PermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )
