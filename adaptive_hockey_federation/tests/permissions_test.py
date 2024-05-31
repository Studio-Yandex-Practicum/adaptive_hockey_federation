from http import HTTPStatus
from typing import Any, Iterable

from core.constants import Role
from main.data_factories.factories import PlayerFactory
from main.models import City, DisciplineName, Player, Team
from tests.base import BaseTestClass
from tests.fixture_user import test_email, test_password, test_role_user
from tests.url_schema import (PLAYER_GET_URLS, PLAYER_POST_URLS, TEAM_GET_URLS,
                              TEAM_POST_URLS, UNLOAD_URLS, USER_GET_URLS,
                              USER_POST_URLS)
from tests.utils import UrlToTest
from users.factories import UserFactory
from users.models import User


class TestPermissions(BaseTestClass):
    """
    Тесты url-путей.

    На возможность доступа к ним определенных категорий пользователей.
    """

    staff_user: User

    @classmethod
    def setUpClass(cls) -> None:
        """Классовый метод для базовой настройки всех тестов класса."""
        super().setUpClass()
        cls.staff_user = UserFactory.create(role=test_role_user, is_staff=True)

    def url_tests(self, url_to_test: UrlToTest):
        """
        Прогоняет тесты урл-адреса на доступ различных пользователей.

        Принимает в качестве параметра экземпляр класса UrlToTest (см.
        docstring к классу UrlToTest).
        """
        responses = url_to_test.execute_tests(self.client, self.user)
        for fact, estimated, message in responses:
            if isinstance(estimated, (str, int)):
                self.assertEqual(fact, estimated, message)
            elif isinstance(estimated, (list, tuple)):
                self.assertIn(fact, estimated, message)

    def batch_url_test(self, urls_to_test: Iterable[UrlToTest]):
        """Проводит sub-тесты для нескольких урл."""
        for url_to_test in urls_to_test:
            with self.subTest(url_to_test=url_to_test):
                self.url_tests(url_to_test)

    def test_main_page(self):
        """
        Главная страница доступна только авторизованному пользователю.

        Для неавторизованного происходит переадресация.
        """
        url_to_test = UrlToTest("/")
        self.url_tests(url_to_test)

    # TODO: Раскомментировать после починки админки. Пользователю вне групп,
    #  но с полем is_staff == True, недоступны почти все урлы в админке.
    # def test_admin_site_available_for_admins_only(self):
    #     """Страницы админки доступны пользователям, у которых поле
    #     is_staff == True, и недоступны при is_staff == False.
    #     администраторам."""
    #     urls_to_test = tuple(
    #         UrlToTest(url, admin_only=True) for url in ADMIN_SITE_ADMIN_OK
    #     )
    #     self.batch_url_test(urls_to_test)

    def test_auth_login(self):
        """
        Для неавторизованного пользователя.

        Должна быть доступна страница входа на сайт.
        """
        url_to_test = UrlToTest("/auth/login/", authorized_only=False)
        self.url_tests(url_to_test)

    def test_auth_logout(self):
        """
        Для авторизованного пользователя.

        POST-запрос авторизованного пользователя на страницы лог-аута
        должен вернуть ответ с кодом 302.
        """
        url_to_test = UrlToTest(
            "/auth/logout/",
            code_estimated=HTTPStatus.FOUND,
            use_post=True,
        )
        self.url_tests(url_to_test)

    def test_auth_password_change_url(self):
        """
        Для авторизованного пользователя.

        Страница смены пароля должна быть доступна только авторизованному
        пользователю.
        """
        url_to_test = UrlToTest("/auth/password_change/")
        self.url_tests(url_to_test)

    def test_auth_password_reset_url(self):
        """
        Для неавторизованного пользователя.

        Страница сброса пароля должна быть доступна неавторизованному
        пользователю.
        """
        url_to_test = UrlToTest("/auth/password_reset/", authorized_only=False)
        self.url_tests(url_to_test)

    # TODO: Раскомментировать, когда будет починен урл. Сейчас он недоступен
    #  для пользователя с is_staff == True, если он не в группе
    #  администраторов.
    # def test_analytics_url(self):
    #     """Страница аналитики доступна пользователям, у которых поле
    #     is_staff == True, и недоступны при is_staff == False."""
    #     url_to_test = UrlToTest("/analytics/", admin_only=True)
    #     self.url_tests(url_to_test)

    # TODO: Проверить тесты и привести в соответсвие с последними изменениями.
    # def test_competition_get_urls(self):
    #    """Тесты get-страниц соревнования на соответствующие разрешения."""
    #    urls_to_test = tuple(UrlToTest(**url) for url in COMPETITION_GET_URLS)
    #    self.batch_url_test(urls_to_test)

    # TODO: Раскомментировать, когда будут починены вьюхи
    #  DeleteTeamFromCompetition и AddTeamToCompetition. Там надо просто
    #  поменять пермишен в одном случае и создать кастомный
    #  add_team_competition в модели соревнований и прикрутить его - во втором.
    # def test_competition_post_urls(self):
    #     """Тесты post-страниц соревнования на соответствующие разрешения."""
    #     urls_to_test = tuple(
    #         UrlToTest(**url, use_post=True, code_estimated=HTTPStatus.FOUND)
    #         for url in COMPETITION_POST_URLS
    #     )
    #     self.batch_url_test(urls_to_test)

    def test_player_get_urls(self):
        """Тесты get-страниц игрока на соответствующие разрешения."""
        urls_to_test = tuple(UrlToTest(**url) for url in PLAYER_GET_URLS)
        self.batch_url_test(urls_to_test)

    def test_player_post_urls(self):
        """Тесты post-страниц игрока на соответствующие разрешения."""
        urls_to_test = tuple(
            UrlToTest(**url, code_estimated=HTTPStatus.FOUND, use_post=True)
            for url in PLAYER_POST_URLS
        )
        self.batch_url_test(urls_to_test)

    # TODO: Раскомментировать, когда пермишены будут приведены в соответствие
    #  с названием сущности (затык на разных наименованиях пермишенов,
    #  где-то это staff, где-то - staffmember, где-то - staffteammember.
    #  Надо привести в общую канву нейминга, так как объект называется
    #  всё-таки StaffTeamMember, соответственно, пермишены надо поименовать
    #  ..._staffteammember), тем более, что StaffMember - это другая
    #  сущность, либо, если я не прав (что вполне возможно) - исправить этот
    #  тест.
    # def test_staff_get_urls(self):
    #     """Тесты get-страниц сотрудника команды на соответствующие
    #     разрешения."""
    #     urls_to_test = tuple(UrlToTest(**url) for url in STAFF_GET_URLS)
    #     self.batch_url_test(urls_to_test)

    # TODO: Раскомментировать, когда пермишены будут приведены в соответствие
    #  с названием сущности (затык на разных наименованиях пермишенов,
    #  где-то это staff, где-то - staffmember, где-то - staffteammember.
    #  Надо привести в общую канву нейминга, так как объект называется
    #  всё-таки StaffTeamMember, соответственно, пермишены надо поименовать
    #  ..._staffteammember), тем более, что StaffMember - это другая
    #  сущность, либо, если я не прав (что вполне возможно) - исправить этот
    #  тест.
    # def test_staff_post_urls(self):
    #     """Тесты post-страниц сотрудника команды на соответствующие
    #     разрешения."""
    #     urls_to_test = tuple(
    #         UrlToTest(**url, code_estimated=HTTPStatus.FOUND, use_post=True)
    #         for url in STAFF_POST_URLS
    #     )
    #     self.batch_url_test(urls_to_test)

    def test_team_get_urls(self):
        """Тесты get-страниц команд на соответствующие разрешения."""
        urls_to_test = tuple(UrlToTest(**url) for url in TEAM_GET_URLS)
        self.batch_url_test(urls_to_test)

    def test_team_post_urls(self):
        """Тесты post-страниц команд на соответствующие разрешения."""
        urls_to_test = tuple(
            UrlToTest(**url, code_estimated=HTTPStatus.FOUND, use_post=True)
            for url in TEAM_POST_URLS
        )
        self.batch_url_test(urls_to_test)

    def test_user_get_urls(self):
        """Тесты get-страниц пользователя на соответствующие разрешения."""
        urls_to_test = tuple(UrlToTest(**url) for url in USER_GET_URLS)
        self.batch_url_test(urls_to_test)

    def test_user_post_urls(self):
        """Тесты post-страниц пользователя на соответствующие разрешения."""
        urls_to_test = tuple(
            UrlToTest(**url, code_estimated=HTTPStatus.FOUND, use_post=True)
            for url in USER_POST_URLS
        )
        self.batch_url_test(urls_to_test)

    def test_unload_urls(self):
        """Тесты get-страниц выгрузки на соответствующие разрешения."""
        urls_to_test = tuple(UrlToTest(**url) for url in UNLOAD_URLS)
        self.batch_url_test(urls_to_test)


class TestSpecialPermissions(BaseTestClass):
    """
    Тесты на наличие специальных разрешений.

    На доступ отдельных групп пользователей к отдельным объектам.
    """

    user_agent: User | Any = None
    team_2: Team | Any = None
    player_2: Player | Any = None

    @classmethod
    def setUpClass(cls) -> None:
        """Классовый метод для базовой настройки всех тестов класса."""
        super().setUpClass()
        cls.user_agent = User.objects.create_user(
            password=test_password,
            first_name="Иван",
            last_name="Агент",
            role=Role.AGENT,
            email="agent_" + test_email,
        )
        cls.team_2 = Team.objects.create(
            name="Team 2",
            city=City.objects.create(name="cls_Test City_2"),
            discipline_name=DisciplineName.objects.create(
                name="cls_Test DisciplineName_2",
            ),
            curator=cls.user_agent,
        )
        cls.player_2 = PlayerFactory.create()
        cls.player.team.clear()
        cls.player_2.team.clear()
        cls.player_2.team.add(cls.team_2)

    # def setUp(self):
    #     self.client = Client()

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
                    msg=(f"Представителю команды должна "
                         f"быть доступна {message}"),
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
                    msg=(f"Представителю команды НЕ должна "
                         f"быть доступна {message}"),
                )
