from http import HTTPStatus
from typing import Any

import pytest
from competitions.models import Competition
from core import constants
from core.constants import Role
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from main.data_factories.factories import (
    CompetitionFactory,
    DiagnosisFactory,
    PlayerFactory,
)
from main.models import City, Diagnosis, DisciplineName, Player, Team
from tests.fixture_user import (
    test_email,
    test_lastname,
    test_name,
    test_password,
    test_role_admin,
    test_role_user,
)
from tests.utils import UrlToTest
from users.models import ProxyGroup, User

TEST_GROUP_NAME = "no_permission_group"


class TestAuthUrls:
    """Тесты авторизации пользователей."""

    @pytest.mark.django_db(transaction=True)
    def test_auth_urls(self, client):
        """Тесты на логин и логаут пользователя."""
        urls = {"/auth/login/": 200, "/auth/logout/": 302}
        for url, status in urls.items():
            try:
                response = client.post(url)
            except Exception as e:
                raise AssertionError(
                    f"Страница {url} работает неправильно. Ошибка: {e}",
                )
            assert response.status_code != 404, (
                f"Страница {url} не найдена, проверьте этот адрес в "
                f"*urls.py*"
            )
            assert response.status_code == status, (
                f"Ошибка {response.status_code} при открытии {url}. "
                f"Проверьте ее view-функцию"
            )


class TestUrls(TestCase):
    """Тесты на проверку url-путей."""

    user: User | Any = None
    user_agent: User | Any = None
    team: Team | Any = None
    team_2: Team | Any = None
    competition: Competition | Any = None
    diagnosis: Diagnosis | Any = None
    player: Player | Any = None
    player_2: Player | Any = None

    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает необходимые сущности (объекты моделей БД).

        Запускается только один раз (в отличие от метода setUp),
        не сбрасывается после каждого теста, что помогает
        избежать многократного создания сущностей и, как следствие, смены id
        каждой сущности после каждого теста.
        """
        super().setUpClass()
        ProxyGroup.objects.create(name=TEST_GROUP_NAME).save()
        constants.GROUPS_BY_ROLE[test_role_user] = TEST_GROUP_NAME
        cls.user = User.objects.create_user(
            password=test_password,
            first_name="cls_" + test_name,
            last_name="cls_" + test_lastname,
            role=test_role_user,
            email="cls_" + test_email,
        )

        cls.user_agent = User.objects.create_user(
            password=test_password,
            first_name="Иван",
            last_name="Агент",
            role=Role.AGENT,
            email="agent_" + test_email,
        )

        cls.team = Team.objects.create(
            name="cls_Test Team",
            city=City.objects.create(name="cls_Test City"),
            discipline_name=DisciplineName.objects.create(
                name="cls_Test DisciplineName",
            ),
            curator=cls.user,
        )

        cls.team_2 = Team.objects.create(
            name="Team 2",
            city=City.objects.create(name="cls_Test City_2"),
            discipline_name=DisciplineName.objects.create(
                name="cls_Test DisciplineName_2",
            ),
            curator=cls.user_agent,
        )

        cls.competition = CompetitionFactory.create()
        cls.diagnosis = DiagnosisFactory.create()
        cls.player = PlayerFactory.create()
        cls.player_2 = PlayerFactory.create()
        cls.player.team.clear()
        cls.player_2.team.clear()
        cls.player_2.team.add(cls.team_2)

    def setUp(self):
        """Метод для базовой настройки тестов класса."""
        self.client = Client()
        self.user = User.objects.create_user(
            password=test_password,
            first_name=test_name,
            last_name=test_lastname,
            role=test_role_user,
            email=test_email,
        )
        self.permissions = {
            "view_team": Permission.objects.get(codename="view_team"),
        }

    def delete_user(self, user_id):
        """Метод для запуска удаления пользователя."""
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    def test_create_user(self):
        """Тест - создание пользователя."""
        self.assertEqual(self.user.first_name, test_name)
        self.assertEqual(self.user.last_name, test_lastname)
        self.assertEqual(self.user.role, test_role_user)
        self.assertEqual(self.user.email, test_email)

    def test_edit_user(self):
        """Тест - редактирование существующего пользователя."""
        new_name = "Test"
        new_lastname = "User"
        new_role = test_role_admin
        new_email = "test@example.com"

        self.user.first_name = new_name
        self.user.last_name = new_lastname
        self.user.role = new_role
        self.user.email = new_email
        self.user.save()

        edited_user = User.objects.get(email=new_email)
        self.assertEqual(edited_user.first_name, new_name)
        self.assertEqual(edited_user.last_name, new_lastname)
        self.assertEqual(edited_user.role, new_role)
        self.assertEqual(edited_user.email, new_email)

    def test_delete_user(self):
        """Тест - удаление пользователя."""
        delete_result = self.delete_user(self.user.id)
        self.assertTrue(delete_result, "Ошибка при удалении пользователя")

    def test_main_urls(self):
        """
        Тесты основных урл.

        Для тестирования нового урл - добавить соответствующий объект класса
        UrlToTest в список urls (см. документацию к классу UrlToTest).
        """
        urls = [
            UrlToTest("/"),
            UrlToTest(
                "/admin/",
                admin_only=True,
                unauthorized_code_estimated=HTTPStatus.FOUND,
            ),
            UrlToTest("/auth/login/", authorized_only=False),
            UrlToTest(
                "/auth/logout/",
                code_estimated=HTTPStatus.FOUND,
                use_post=True,
            ),
            UrlToTest("/auth/password_change/"),
            UrlToTest("/auth/password_reset/", authorized_only=False),
            UrlToTest("/analytics/", permission_required="list_view_player"),
            # TODO Нужно доработать тесты соревнования согласно правам доступа.
            # UrlToTest(
            # "/competitions/", permission_required="list_view_competition"
            # ),
            # TODO Раскомментировать при доработке пермишенов для страниц с
            #  соревнованиями.
            # UrlToTest(
            # "/competitions/1/", permission_required="list_team_competition"
            # ),
            # TODO Раскомментировать при доработке пермишенов для страниц с
            #  игроками.
            UrlToTest("/players/create/", permission_required="add_player"),
            UrlToTest("/players/", permission_required="list_view_player"),
            # TODO Раскомментировать при доработке пермишенов для страниц с
            #  игроками.
            UrlToTest("/players/1/", permission_required="view_player"),
            UrlToTest("/players/1/edit/", permission_required="change_player"),
            UrlToTest("/teams/", permission_required="list_view_team"),
            UrlToTest("/teams/1/", permission_required="view_team"),
            UrlToTest("/teams/1/edit/", permission_required="change_team"),
            UrlToTest("/teams/create/", permission_required="add_team"),
            UrlToTest("/unloads/", permission_required="list_view_unload"),
            # TODO Раскомментировать при доработке пермишенов для страниц с
            #  пользователями.
            UrlToTest("/users/create/", permission_required="add_user"),
            UrlToTest("/users/", permission_required="list_view_user"),
            UrlToTest("/users/1/edit/", permission_required="change_user"),
        ]
        urls_responses_results = []

        for url in urls:
            urls_responses_results += url.execute_tests(self.client, self.user)

        for fact, estimated, message in urls_responses_results:
            with self.subTest(msg=message, fact=fact, estimated=estimated):
                if isinstance(estimated, (str, int)):
                    self.assertEqual(fact, estimated, message)
                elif isinstance(estimated, (list, tuple)):
                    self.assertIn(fact, estimated, message)

    def test_agent_has_access(self):
        """Доступ представителя к своей команде, ее игрокам и т.д."""
        # TODO: Добавить урлы тренеров и пушер-тьюторов по аналогии,
        #  когда функционал ограничения доступа к этим сущностям будет
        #  разработан.
        urls_agent_has_access_to = {
            f"/teams/{self.team_2.id}/edit/": (
                "страница /teams/<team_id>/edit/ редактирования общих "
                "сведений этой команды (ожидается ответ со статусом 200)"
            ),
            f"/players/{self.player_2.id}/": (
                "страница просмотра подробных сведений об игроке из этой "
                "команды (страница /players/<player_id>/ должна вернуть "
                "ответ со статусом 200)"
            ),
            f"/players/{self.player_2.id}/edit/": (
                "страница редактирования игрока из этой команды (страница "
                "/players/<player_id>/edit/ должна вернуть ответ со статусом "
                "200)"
            ),
            f"/players/create/?team={self.team_2.id}": (
                "страница создания игрока из этой команды (страница "
                "/players/create/?team=<team_id> должна вернуть ответ со "
                "статусом 200)"
            ),
        }
        self.client.force_login(self.user_agent)
        for url, message in urls_agent_has_access_to.items():
            with self.subTest(msg=message, url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    msg=(
                        f"Представителю команды должна"
                        f"быть доступна {message}"
                    ),
                )

    def test_agent_has_no_access(self):
        """Запрет доступа представителя к чужой команде, игрокам и т.д."""
        # TODO: Добавить урлы тренеров и пушер-тьюторов по аналогии,
        #  когда функционал ограничения доступа к этим сущностям будет
        #  разработан.
        urls_agent_has_no_access_to = {
            f"/teams/{self.team.id}/edit/": (
                "страница /teams/<team_id>/edit/ редактирования общих "
                "сведений ЧУЖОЙ команды (ожидается ответ со статусом 403)"
            ),
            f"/players/{self.player.id}/": (
                "страница просмотра подробных сведений об игроке ЧУЖОЙ "
                "команды (страница /players/<player_id>/ должна вернуть "
                "ответ со статусом 403)"
            ),
            f"/players/{self.player.id}/edit/": (
                "страница редактирования игрока ЧУЖОЙ команды (страница "
                "/players/<player_id>/edit должна вернуть ответ со статусом "
                "403)"
            ),
            f"/players/create/?team={self.team.id}": (
                "страница создания игрока с привязкой к ЧУЖОЙ команде "
                "(страница /players/create/?team=<team_id> должна вернуть "
                "ответ со статусом 403)"
            ),
            "/players/create/": (
                "страница создания игрока без привязки к какой-либо команде "
                "(страница /players/create/ должна вернуть ответ со "
                "статусом 403)"
            ),
        }
        self.client.force_login(self.user_agent)
        for url, message in urls_agent_has_no_access_to.items():
            with self.subTest(msg=message, url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.FORBIDDEN,
                    msg=(
                        f"Представителю команды НЕ должна "
                        f"быть доступна {message}"
                    ),
                )
