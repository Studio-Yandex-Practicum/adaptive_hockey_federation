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
        self.correct_create_tests(url="/users/create/")

    def test_user_update_via_http(self):
        object_id_estimated = User.objects.count() + 1
        url = f"/users/{object_id_estimated}/edit/"
        self.correct_update_tests(url=url)

    def test_user_delete_via_http(self):
        object_id_estimated = User.objects.count() + 1
        url = f"/users/{object_id_estimated}/delete/"
        self.correct_delete_tests(url=url)

    def test_user_fields_validation_via_http(self):
        object_id_estimated = User.objects.count() + 1
        url = f"/users/{object_id_estimated}/edit/"
        self.incorrect_field_tests_via_url(url=url)

    def test_user_fields_admit_values_via_http(self):
        object_id_estimated = User.objects.count() + 1
        url = f"/users/{object_id_estimated}/edit/"
        self.correct_field_tests(url=url)


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
