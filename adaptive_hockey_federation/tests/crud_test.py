from tests.base import ModelTestBaseClass
from tests.models_schema import GROUP_MODEL_TEST_SCHEMA, USER_MODEL_TEST_SCHEMA
from users.factories import UserFactory
from users.models import ProxyGroup, User


class UserCrudTest(ModelTestBaseClass):
    model = User
    model_schema = USER_MODEL_TEST_SCHEMA
    model_factory = UserFactory

    def test_user_correct_creation(self):
        self.correct_create_tests()

    def test_user_correct_update(self):
        self.correct_update_tests()

    def test_user_fields_validation(self):
        self.incorrect_field_tests()

    def test_user_fields_admit_values(self):
        self.correct_field_tests()

    def test_user_deletion(self):
        self.correct_delete_tests()

    def test_user_create_via_http(self):
        self.client.force_login(self.superuser)
        count = User.objects.count()
        self.client.post(
            "/users/create/",
            {
                "first_name": "Виктор",
                "last_name": "Ушакевич",
                "patronymic": "Александрович",
                "email": "victorixx@yandex.ru",
                "phone": "+7 921 332-71-72",
                "role": "Администратор",
            },
        )
        self.assertEqual(User.objects.count(), count + 1, msg="Неправильно.")


class GroupCrudTest(ModelTestBaseClass):
    model = ProxyGroup
    model_schema = GROUP_MODEL_TEST_SCHEMA

    def test_group_correct_creation(self):
        self.correct_create_tests()

    def test_group_correct_update(self):
        self.correct_update_tests()

    def test_group_fields_validation(self):
        self.incorrect_field_tests()

    def test_group_fields_admit_values(self):
        self.correct_field_tests()

    def test_group_deletion(self):
        self.correct_delete_tests()
