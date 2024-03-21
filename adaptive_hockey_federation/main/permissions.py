from django.contrib.auth.mixins import (
    AccessMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import get_object_or_404
from main.models import Team


class AdminRequiredMixin(AccessMixin):
    """Миксин наделяющий правом доступа только администратора."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_moderator or request.user.is_agent:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CustomPermissionMixin(PermissionRequiredMixin, UserPassesTestMixin):
    """Миксин, объединяющий функционал миксинов-родителей.

    PermissionRequiredMixin и UserPassesTestMixin имеют общего родителя
    AccessMixin и оба переопределяют родительский метод dispatch(), в связи с
    чем их одновременное прямое использование во вью-классе невозможно.

    Данный класс-миксин позволяет обойти это ограничение.

    Работает следующим образом: сначала проверяется наличие общих разрешений
    (которые указываются в permission_required соответствующего представления).
    Затем производится тест пользователя на какие-то конкретные условия,
    которые определяются в методе test_func().

    !!! Во вью-классе или миксине-наследнике необходимо переопределить метод
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
    """Миксин настройки разрешений для вью-классов PlayerIdView.
    Ограничивает права представителя на доступ к представлениям игроков не
    своих команд.

    Если пользователь не является представителем (т.е. role != AGENT),
    разрешения будут определяться только общим permission_required,
    определенным во вью-классе.

    Если пользователь является представителем, то проверяется условие,
    что он имеет отношение к команде, к которой принадлежит игрок или в
    которую добавляется новый игрок.

    При создании игрока, когда request не содержит ключа "team", считается,
    что игрок добавляется в БД без связки с конкретной командой и
    представителю будет отказано в доступе."""

    def test_func(self) -> bool | None:
        request = self.__getattribute__("request")
        if not (user := request.user).is_agent:
            return True
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
    """Миксин настройки разрешений для вью-классов TeamIdView.
    Ограничивает права представителя на доступ к представлениям не своих
    команд.

    В текущем виде подходит только для страниц просмотра или редактирования
    основных данных команды, поскольку считается, что создание новой команды
    не разрешается для представителя в принципе.

    Работает аналогично PlayerIdPermissionsMixin, кроме функционала создания
    объекта."""

    def test_func(self) -> bool | None:
        user = self.__getattribute__("request").user
        team = self.__getattribute__("get_object")()
        return not user.is_agent or team.curator == user
