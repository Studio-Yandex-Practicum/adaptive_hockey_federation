from http import HTTPStatus
from typing import Any

import pytest
from competitions.models import Competition
from core import constants
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

    @pytest.mark.django_db(transaction=True)
    def test_auth_urls(self, client):
        urls = {"/auth/login/": 200, "/auth/logout/": 302}
        for url, status in urls.items():
            try:
                response = client.post(url)
            except Exception as e:
                assert (
                    False
                ), f"Страница {url} работает неправильно. Ошибка: {e}"
            assert response.status_code != 404, (
                f"Страница {url} не найдена, проверьте этот адрес в "
                f"*urls.py*"
            )
            assert response.status_code == status, (
                f"Ошибка {response.status_code} при открытии {url}. "
                f"Проверьте ее view-функцию"
            )


class TestUrls(TestCase):
    user: User | Any = None
    team: Team | Any = None
    competition: Competition | Any = None
    diagnosis: Diagnosis | Any = None
    player: Player | Any = None

    @classmethod
    def setUpClass(cls) -> None:
        """Создает необходимые сущности (объекты моделей БД).
        Запускается только один раз (в отличие от метода setUp),
        не сбрасывается после каждого теста, что помогает
        избежать многократного создания сущностей и, как следствие, смены id
        каждой сущности после каждого теста."""
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

        cls.team = Team.objects.create(
            name="cls_Test Team",
            city=City.objects.create(name="cls_Test City"),
            discipline_name=DisciplineName.objects.create(
                name="cls_Test DisciplineName"
            ),
            curator=cls.user,
        )
        cls.competition = CompetitionFactory.create()
        cls.diagnosis = DiagnosisFactory.create()
        cls.player = PlayerFactory.create()

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            password=test_password,
            first_name=test_name,
            last_name=test_lastname,
            role=test_role_user,
            email=test_email,
        )
        self.permissions = {
            "view_team": Permission.objects.get(codename="view_team")
        }

    def delete_user(self, user_id):
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
        """Тесты основных урл.
        Для тестирования нового урл - добавить соответствующий объект класса
        UrlToTest в список urls (см. документацию к классу UrlToTest)."""
        urls = [
            UrlToTest("/"),
            UrlToTest(
                "/admin/",
                admin_only=True,
                unauthorized_code_estimated=HTTPStatus.FOUND,
            ),
            UrlToTest("/auth/login/", authorized_only=False),
            UrlToTest(
                "/auth/logout/", code_estimated=HTTPStatus.FOUND, use_post=True
            ),
            UrlToTest("/auth/password_change/"),
            UrlToTest("/auth/password_reset/", authorized_only=False),
            UrlToTest("/analytics/", permission_required="list_view_player"),
            UrlToTest(
                "/competitions/",
                permission_required="list_view_competition"
            ),
            # TODO Раскомментировать при доработке пермишенов для страниц с
            #  соревнованиями.
            UrlToTest(
                "/competitions/1/", permission_required="list_team_competition"
            ),
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
            UrlToTest("/unloads/"),
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
