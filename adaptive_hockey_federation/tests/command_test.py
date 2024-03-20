from typing import Any

from core import constants
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from main.data_factories.factories import TeamFactory
from main.models import City, DisciplineName, Team
from tests.fixture_user import (
    test_email,
    test_lastname,
    test_name,
    test_password,
    test_role_user,
)
from users.models import ProxyGroup, User

TEST_GROUP_NAME = "no_permission_group"


class TestCommand(TestCase):
    user: User | Any = None
    team: Team | Any = None

    @classmethod
    def setUpClass(cls) -> None:
        """Создает необходимые сущности (объекты моделей БД)."""
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

    def setUp(self):
        self.client = Client()
        self.permissions = {
            "view_team": Permission.objects.get(codename="view_team")
        }

    # TODO: Добавить проверку пермишенов после их полной реализации
    def test_create_team(self):
        """Тест - создание команды."""
        new_team = TeamFactory.create()
        self.assertIsNotNone(new_team, "Ошибка при создании команды")

    # TODO: Добавить проверку пермишенов после их полной реализации
    def test_read_team(self):
        """Тест - чтения команды."""
        new_team = TeamFactory.create()
        try:
            retrieved_team = Team.objects.get(id=new_team.id)
            self.assertEqual(new_team.name, retrieved_team.name)
        except Team.DoesNotExist:
            self.fail("Ошибка при чтении команды: тестовая команда не найдена")

    # TODO: Добавить проверку пермишенов после их полной реализации
    def test_update_team(self):
        """Тест - обновления команды."""
        new_team = TeamFactory.create()
        new_name = "Updated Team"
        new_team.name = new_name
        try:
            new_team.save()
            updated_team = Team.objects.get(id=new_team.id)
            self.assertEqual(updated_team.name, new_name)
        except Exception:
            self.fail("Ошибка при обновлении команды")

    # TODO: Добавить проверку пермишенов после их полной реализации
    def test_delete_team(self):
        """Тест - удаления команды."""
        new_team = TeamFactory.create()
        new_team_id = new_team.id
        try:
            new_team.delete()
            with self.assertRaises(Team.DoesNotExist):
                Team.objects.get(id=new_team_id)
        except Exception:
            self.fail("Ошибка при удалении команды")
