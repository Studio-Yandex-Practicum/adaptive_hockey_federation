from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import get_object_or_404
from main.models import Team


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


class PlayerIdPermissionsMixin(CustomPermissionMixin):
    """Миксин настройки разрешений для вью-классов PlayerIdView."""

    def test_func(self) -> bool | None:
        request = self.__getattribute__("request")
        user = request.user
        if self.__getattribute__("kwargs").get("pk", None):
            player = self.__getattribute__("get_object")()
            return player.team.filter(curator=user).exists()
        if team_id := (
            request.GET.get("team", None) or request.POST.get("team", None)
        ):
            team = get_object_or_404(Team, id=team_id)
            return team.curator == user
        return False


class TeamEditPermissionsMixin(CustomPermissionMixin):
    """Миксин настройки разрешений для вью-классов TeamIdView."""

    def test_func(self) -> bool | None:
        user = self.__getattribute__("request").user
        team = self.__getattribute__("get_object")()
        return team.curator == user
