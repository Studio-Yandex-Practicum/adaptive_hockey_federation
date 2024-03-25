from typing import Any

import pytest
from competitions.models import Competition
from core import constants
from core.constants import ROLE_AGENT
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
    user_agent: User | Any = None
    team: Team | Any = None
    team_2: Team | Any = None
    competition: Competition | Any = None
    diagnosis: Diagnosis | Any = None
    player: Player | Any = None
    player_2: Player | Any = None

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

        cls.user_agent = User.objects.create_user(
            password=test_password,
            first_name="Иван",
            last_name="Агент",
            role=ROLE_AGENT,
            email="agent_" + test_email,
        )

        cls.team = Team.objects.create(
            name="cls_Test Team",
            city=City.objects.create(name="cls_Test City"),
            discipline_name=DisciplineName.objects.create(
                name="cls_Test DisciplineName"
            ),
            curator=cls.user,
        )

        cls.team_2 = Team.objects.create(
            name="Team 2",
            city=City.objects.create(name="cls_Test City_2"),
            discipline_name=DisciplineName.objects.create(
                name="cls_Test DisciplineName_2"
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
