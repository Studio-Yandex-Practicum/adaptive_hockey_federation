from core.constants import ROLE_ADMIN
from tests.base import BaseTestClass
from tests.url_schema import ADMIN_SITE_ADMIN_OK
from tests.utils import UrlToTest


class TestPermissions(BaseTestClass):
    """Тесты урл-путей на возможность доступа к ним определенных категорий
    пользователей."""

    # @classmethod
    # def setUpClass(cls) -> None:
    #     super().setUpClass()
    #     ProxyGroup.objects.create(name=TEST_GROUP_NAME).save()
    #     constants.GROUPS_BY_ROLE[test_role_user] = TEST_GROUP_NAME

    def url_tests(self, url_to_test: UrlToTest):
        """Прогоняет тесты урл-адреса на доступ различных пользователей.
        Принимает в качестве параметра экземпляр класса UrlToTest (см.
        docstring к классу UrlToTest)."""
        responses = url_to_test.execute_tests(self.client, self.user)
        for fact, estimated, message in responses:
            with self.subTest(msg=message, fact=fact, estimated=estimated):
                if isinstance(estimated, (str, int)):
                    self.assertEqual(fact, estimated, message)
                elif isinstance(estimated, (list, tuple)):
                    self.assertIn(fact, estimated, message)

    def test_main_page(self):
        """Главная страница доступна только авторизованному пользователю.
        Для неавторизованного происходит переадресация."""
        url_to_test = UrlToTest("/")
        self.url_tests(url_to_test)

    def test_admin_site_available_for_admins_only(self):
        """Страницы админки доступны только администраторам."""
        self.user.role = ROLE_ADMIN
        self.user.save()
        for admin_url in ADMIN_SITE_ADMIN_OK:
            url_to_test = UrlToTest(
                admin_url,
                admin_only=True,
            )
            self.url_tests(url_to_test)

    # UrlToTest("/auth/login/", authorized_only=False),
    # UrlToTest(
    #     "/auth/logout/", code_estimated=HTTPStatus.FOUND, use_post=True
    # ),
    # UrlToTest("/auth/password_change/"),
    # UrlToTest("/auth/password_reset/", authorized_only=False),
    # UrlToTest("/analytics/", permission_required="list_view_player"),
    # UrlToTest(
    #     "/competitions/", permission_required="list_view_competition"
    # ),
    # # TODO Раскомментировать при доработке пермишенов для страниц с
    # #  соревнованиями.
    # UrlToTest(
    #     "/competitions/1/", permission_required="list_team_competition"
    # ),
    # # TODO Раскомментировать при доработке пермишенов для страниц с
    # #  игроками.
    # UrlToTest("/players/create/", permission_required="add_player"),
    # UrlToTest("/players/", permission_required="list_view_player"),
    # # TODO Раскомментировать при доработке пермишенов для страниц с
    # #  игроками.
    # UrlToTest("/players/1/", permission_required="view_player"),
    # UrlToTest("/players/1/edit/", permission_required="change_player"),
    # UrlToTest("/teams/", permission_required="list_view_team"),
    # UrlToTest("/teams/1/", permission_required="view_team"),
    # UrlToTest("/teams/1/edit/", permission_required="change_team"),
    # UrlToTest("/teams/create/", permission_required="add_team"),
    # UrlToTest("/unloads/"),
    # # TODO Раскомментировать при доработке пермишенов для страниц с
    # #  пользователями.
    # UrlToTest("/users/create/", permission_required="add_user"),
    # UrlToTest("/users/", permission_required="list_view_user"),
    # UrlToTest("/users/1/edit/", permission_required="change_user")
