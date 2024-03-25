from http import HTTPStatus
from typing import Iterable

from tests.base import BaseTestClass
from tests.fixture_user import test_role_user
from tests.url_schema import (
    COMPETITION_GET_URLS,
    COMPETITION_POST_URLS,
    PLAYER_GET_URLS,
    PLAYER_POST_URLS,
    STAFF_GET_URLS,
    STAFF_POST_URLS,
    TEAM_GET_URLS,
    TEAM_POST_URLS,
    UNLOAD_URLS,
    USER_GET_URLS,
    USER_POST_URLS,
)
from tests.utils import UrlToTest
from users.factories import UserFactory
from users.models import User


class TestPermissions(BaseTestClass):
    """Тесты урл-путей на возможность доступа к ним определенных категорий
    пользователей."""

    staff_user: User

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.staff_user = UserFactory.create(role=test_role_user, is_staff=True)

    def url_tests(self, url_to_test: UrlToTest):
        """Прогоняет тесты урл-адреса на доступ различных пользователей.
        Принимает в качестве параметра экземпляр класса UrlToTest (см.
        docstring к классу UrlToTest)."""
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
        """Главная страница доступна только авторизованному пользователю.
        Для неавторизованного происходит переадресация."""
        url_to_test = UrlToTest("/")
        self.url_tests(url_to_test)

    # def test_admin_site_available_for_admins_only(self):
    #     """Страницы админки доступны пользователям, у которых поле
    #     is_staff == True, и недоступны при is_staff == False.
    #     администраторам."""
    #     for admin_url in ADMIN_SITE_ADMIN_OK:
    #         with self.subTest(admin_url=admin_url):
    #             url_to_test = UrlToTest(
    #                 admin_url,
    #                 admin_only=True,
    #             )
    #             self.url_tests(url_to_test)

    def test_auth_login(self):
        """Неавторизованному пользователю должна быть доступна страница
        входа на сайт."""
        url_to_test = UrlToTest("/auth/login/", authorized_only=False)
        self.url_tests(url_to_test)

    def test_auth_logout(self):
        """POST-запрос авторизованного пользователя на страницы лог-аута
        должен вернуть ответ с кодом 302."""
        url_to_test = UrlToTest(
            "/auth/logout/", code_estimated=HTTPStatus.FOUND, use_post=True
        )
        self.url_tests(url_to_test)

    def test_auth_password_change_url(self):
        """Страница смены пароля должна быть доступна только авторизованному
        пользователю."""
        url_to_test = UrlToTest("/auth/password_change/")
        self.url_tests(url_to_test)

    def test_auth_password_reset_url(self):
        """Страница сброса пароля должна быть доступна неавторизованному
        пользователю."""
        url_to_test = UrlToTest("/auth/password_reset/", authorized_only=False)
        self.url_tests(url_to_test)

    def test_analytics_url(self):
        """Страница аналитики доступна пользователям, у которых поле
        is_staff == True, и недоступны при is_staff == False."""
        url_to_test = UrlToTest("/analytics/", admin_only=True)
        self.url_tests(url_to_test)

    def test_competition_get_urls(self):
        """Тесты get-страниц соревнования на соответствующие разрешения."""
        urls_to_test = tuple(UrlToTest(**url) for url in COMPETITION_GET_URLS)
        self.batch_url_test(urls_to_test)

    def test_competition_post_urls(self):
        """Тесты post-страниц соревнования на соответствующие разрешения."""
        urls_to_test = tuple(
            UrlToTest(**url, use_post=True, code_estimated=HTTPStatus.FOUND)
            for url in COMPETITION_POST_URLS
        )
        self.batch_url_test(urls_to_test)

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

    def test_staff_get_urls(self):
        """Тесты get-страниц сотрудника команды на соответствующие
        разрешения."""
        urls_to_test = tuple(UrlToTest(**url) for url in STAFF_GET_URLS)
        self.batch_url_test(urls_to_test)

    def test_staff_post_urls(self):
        """Тесты post-страниц сотрудника команды на соответствующие
        разрешения."""
        urls_to_test = tuple(
            UrlToTest(**url, code_estimated=HTTPStatus.FOUND, use_post=True)
            for url in STAFF_POST_URLS
        )
        self.batch_url_test(urls_to_test)

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
