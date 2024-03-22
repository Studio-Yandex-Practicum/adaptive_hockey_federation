from django.test import TestCase
from tests.fixture_user import (
    test_email,
    test_lastname,
    test_name,
    test_password,
    test_role_user,
)
from users.factories import UserFactory
from users.models import User


class TestUser(TestCase):
    """Тестирование CRUD пользователя
    с использованием фабрик."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных."""
        cls.test_user = UserFactory.create()
        cls.test_user2 = UserFactory.create()

        cls.first_name = test_name
        cls.last_name = test_lastname
        cls.test_password = test_password
        cls.email = test_email
        cls.role = test_role_user

    # TODO: Добавить проверку пермишенов
    def test_create_user(self):
        """Проверка создания пользователей."""
        self.assertIsNotNone(self.test_user, "Пользователь 1 не создался")
        self.assertIsNotNone(self.test_user2, "Пользователь 2 не создался")
        users_count = User.objects.count()
        self.assertEqual(
            users_count, 2, "Неправильное количество после создания."
        )

    # TODO: Добавить проверку пермишенов
    def test_get_user(self):
        """Тест получения информации о пользователе."""
        try:
            retrieved_user = User.objects.get(id=self.test_user.id)
            self.assertEqual(
                self.test_user.first_name,
                retrieved_user.first_name,
                "Ошибка при получении first_name",
            )
            self.assertEqual(
                self.test_user.last_name,
                retrieved_user.last_name,
                "Ошибка при получении last_name.",
            )
            self.assertEqual(
                self.test_user.email,
                retrieved_user.email,
                "Ошибка при получении email",
            )
            self.assertEqual(
                self.test_user.password,
                retrieved_user.password,
                "Ошибка при получении password.",
            )
            self.assertEqual(
                self.test_user.role,
                retrieved_user.role,
                "Ошибка при получении role.",
            )
        except User.DoesNotExist:
            self.fail("Ошибка при получении пользователя.")

    # TODO: Добавить проверку пермишенов
    def test_update_user(self):
        """Тест обновления информации о пользователе."""

        self.assertNotEqual(
            self.test_user.first_name,
            self.first_name,
            "неверные тестовые данные",
        )
        self.test_user.first_name = self.first_name
        self.test_user.last_name = self.last_name
        self.test_user.email = self.email
        self.test_user.password = self.test_password
        self.test_user.role = self.role
        self.assertEqual(
            self.test_user.first_name,
            self.first_name,
            "Ошибка в изменении first_name",
        )
        self.assertEqual(
            self.test_user.last_name,
            self.last_name,
            "Ошибка в обновлении last_name",
        )
        self.assertEqual(
            self.test_user.email,
            self.email,
            "Ошибка в обновлении информации email",
        )
        self.assertEqual(
            self.test_user.password,
            self.test_password,
            "Ошибка при обновлении password.",
        )
        self.assertEqual(
            self.test_user.role, self.role, "Ошибка при обновлении role."
        )

    # TODO: Добавить проверку пермишенов
    def test_delete_user(self):
        """Тест удаления пользователя."""
        test_id = self.test_user.id
        count = User.objects.count()
        self.test_user.delete()
        count2 = User.objects.count()
        self.assertEqual(
            count2, count - 1, "Количество пользователей не изменилось"
        )
        try:
            with self.assertRaises(User.DoesNotExist):
                User.objects.get(id=test_id)
        except Exception:
            self.fail("Ошибка при удалении пользователя")
