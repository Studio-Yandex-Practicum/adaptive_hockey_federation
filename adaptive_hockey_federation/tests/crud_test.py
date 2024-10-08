from typing import Any

import pytest
from core.constants import Role
from main.models import (
    City,
    Diagnosis,
    DisciplineLevel,
    DisciplineName,
    Nosology,
    Player,
    StaffMember,
    StaffTeamMember,
    Team,
)
from tests.base import ModelTestBaseClass
from tests.model_schemas.city import CITY_MODEL_TEST_SCHEMA
from tests.model_schemas.diagnosis import DIAGNOSIS_MODEL_TEST_SCHEMA
from tests.model_schemas.discipline_level import (
    DISCIPLINE_LEVEL_MODEL_TEST_SCHEMA,
)
from tests.model_schemas.discipline_name import (
    DISCIPLINE_NAME_MODEL_TEST_SCHEMA,
)
from tests.model_schemas.group import GROUP_MODEL_TEST_SCHEMA
from tests.model_schemas.nosology import NOSOLOGY_MODEL_TEST_SCHEMA
from tests.model_schemas.player import PLAYER_MODEL_TEST_SCHEMA
from tests.model_schemas.staff_member import STAFF_MEMBER_MODEL_TEST_SCHEMA
from tests.model_schemas.staff_team_member import (
    STAFF_TEAM_MEMBER_MODEL_TEST_SCHEMA,
)
from tests.model_schemas.team import TEAM_MODEL_TEST_SCHEMA
from tests.model_schemas.user import USER_MODEL_TEST_SCHEMA
from users.factories import UserFactory
from users.models import ProxyGroup, User


class UserCrudTest(ModelTestBaseClass):
    """CRUD-тесты пользователя."""

    model = User
    model_schema = USER_MODEL_TEST_SCHEMA
    model_factory = UserFactory

    def test_user_correct_creation(self):
        """Тест на корректное создание напрямую через БД."""
        self.correct_create_tests()

    def test_user_correct_update(self):
        """Тест на корректное изменение напрямую через БД."""
        self.correct_update_tests()

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_user_fields_validation(self):
    # """Тест на валидацию некорректных значений напрямую через БД."""
    #     self.incorrect_field_tests()

    # def test_user_fields_admit_values(self):
    # """Тест на допуск корректных значений напрямую через БД."""
    #     self.correct_field_tests()

    def test_user_deletion(self):
        """Тест на удаление объекта напрямую через БД."""
        self.correct_delete_tests()

    def test_user_create_via_http(self):
        """Тест на корректное создание через сайт."""
        self.correct_create_tests(url="/users/create/")

    def test_user_update_via_http(self):
        """Тест на корректное изменение через сайт."""
        url = f"/users/{self.future_obj_id}/edit/"
        self.correct_update_tests(url=url)

    def test_user_delete_via_http(self):
        """Тест на корректное удаление через сайт."""
        url = f"/users/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url)

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_user_fields_validation_via_http(self):
    # """Тест на валидацию некорректных значений при изменении через сайт."""
    #     url = f"/users/{self.future_obj_id}/edit/"
    #     self.incorrect_field_tests_via_url(url=url)

    # def test_user_fields_admit_values_via_http(self):
    # """Тест на допуск корректных значений при изменении через сайт."""
    #     url = f"/users/{self.future_obj_id}/edit/"
    #     self.correct_field_tests(url=url)

    def test_user_correct_create_via_admin(self):
        """Тест на корректное создание через административную часть."""
        self.correct_create_tests(url="/admin/users/user/add/")

    def test_user_correct_update_via_admin(self):
        """Тест на корректное изменение через административную часть."""
        url = f"/admin/users/user/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_user_fields_validation_via_admin(self):
    # """Тест на валидацию некорректных значений при изменении через
    # административную часть."""
    #     url = f"/admin/users/user/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_user_delete_via_admin(self):
        """Тест на корректное удаление через административную часть."""
        self.client.force_login(self.superuser)
        url = f"/admin/users/user/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_user_fields_admit_values_via_admin(self):
    # """Тест на допуск корректных значений через административную часть."""
    #     url = f"/admin/users/user/{self.future_obj_id}/change/"
    #     self.correct_field_tests(url=url)


class GroupCrudTest(ModelTestBaseClass):
    """CRUD-тесты групп."""

    model = ProxyGroup
    model_schema = GROUP_MODEL_TEST_SCHEMA

    def test_group_correct_creation(self):
        """Тест на корректное создание напрямую через БД."""
        self.correct_create_tests()

    def test_group_correct_update(self):
        """Тест на корректное изменение напрямую через БД."""
        self.correct_update_tests()

    def test_group_fields_validation(self):
        """Тест на валидацию некорректных значений напрямую через БД."""
        self.incorrect_field_tests()

    def test_group_fields_admit_values(self):
        """Тест на допуск корректных значений напрямую через БД."""
        self.correct_field_tests()

    def test_group_deletion(self):
        """Тест на удаление объекта напрямую через БД."""
        self.correct_delete_tests()

    def test_group_correct_create_via_admin(self):
        """Тест на корректное создание через административную часть."""
        self.correct_create_tests(url="/admin/auth/group/add/")

    def test_group_correct_update_via_admin(self):
        """Тест на корректное изменение через административную часть."""
        url = f"/admin/auth/group/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    def test_group_fields_validation_via_admin(self):
        """
        Тест на валидацию некорректных значений.

        Через административную часть.
        """
        url = f"/admin/auth/group/{self.future_obj_id}/change/"
        self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_group_delete_via_admin(self):
        """Тест на корректное удаление через административную часть."""
        url = f"/admin/auth/group/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_group_fields_admit_values_via_admin(self):
        """Тест на допуск корректных значений через административную часть."""
        url = f"/admin/auth/group/{self.future_obj_id}/change/"
        self.correct_field_tests(url=url)


class CityCrudTest(ModelTestBaseClass):
    """CRUD-тесты модели города."""

    model = City
    model_schema = CITY_MODEL_TEST_SCHEMA

    def test_city_correct_creation(self):
        """Тест на корректное создание напрямую через БД."""
        self.correct_create_tests()

    def test_city_correct_update(self):
        """Тест на корректное изменение напрямую через БД."""
        self.correct_update_tests()

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_city_fields_validation(self):
    # """Тест на валидацию некорректных значений напрямую через БД."""
    #     self.incorrect_field_tests()

    def test_city_fields_admit_values(self):
        """Тест на допуск корректных значений напрямую через БД."""
        self.correct_field_tests()

    def test_city_deletion(self):
        """Тест на удаление объекта напрямую через БД."""
        self.correct_delete_tests()

    def test_city_correct_create_via_admin(self):
        """Тест на корректное создание через административную часть."""
        self.correct_create_tests(url="/admin/main/city/add/")

    def test_city_correct_update_via_admin(self):
        """Тест на корректное изменение через административную часть."""
        url = f"/admin/main/city/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_city_fields_validation_via_admin(self):
    # """Тест на валидацию некорректных значений через административную
    # часть."""
    #     url = f"/admin/main/city/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_city_delete_via_admin(self):
        """Тест на корректное удаление через административную часть."""
        url = f"/admin/main/city/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_city_fields_admit_values_via_admin(self):
        """Тест на допуск корректных значений через административную часть."""
        url = f"/admin/main/city/{self.future_obj_id}/change/"
        self.correct_field_tests(url=url)


class DiagnosisCrudTest(ModelTestBaseClass):
    """CRUD-тесты модели диагноза."""

    model = Diagnosis
    model_schema = DIAGNOSIS_MODEL_TEST_SCHEMA

    def test_diagnosis_correct_creation(self):
        """Тест на корректное создание напрямую через БД."""
        self.correct_create_tests()

    def test_diagnosis_correct_update(self):
        """Тест на корректное изменение напрямую через БД."""
        self.correct_update_tests()

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_diagnosis_fields_validation(self):
    # """Тест на валидацию некорректных значений напрямую через БД."""
    #     self.incorrect_field_tests()

    def test_diagnosis_fields_admit_values(self):
        """Тест на допуск корректных значений напрямую через БД."""
        self.correct_field_tests()

    def test_diagnosis_deletion(self):
        """Тест на удаление объекта напрямую через БД."""
        self.correct_delete_tests()

    def test_diagnosis_correct_create_via_admin(self):
        """Тест на корректное создание через административную часть."""
        self.correct_create_tests(url="/admin/main/diagnosis/add/")

    def test_diagnosis_correct_update_via_admin(self):
        """Тест на корректное изменение через административную часть."""
        url = f"/admin/main/diagnosis/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_diagnosis_fields_validation_via_admin(self):
    #     """Тест на валидацию некорректных значений полей через
    #     административную часть."""
    #     url = f"/admin/main/diagnosis/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_diagnosis_delete_via_admin(self):
        """Тест на корректное удаление через административную часть."""
        url = f"/admin/main/diagnosis/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_diagnosis_fields_admit_values_via_admin(self):
        """
        Тест на допуск корректных значений полей.

        Через административную часть.
        """
        url = f"/admin/main/diagnosis/{self.future_obj_id}/change/"
        self.correct_field_tests(url=url)


class NosologyCrudTest(ModelTestBaseClass):
    """CRUD-тесты модели диагноза."""

    model = Nosology
    model_schema = NOSOLOGY_MODEL_TEST_SCHEMA

    def test_nosology_correct_creation(self):
        """Тест на корректное создание напрямую через БД."""
        self.correct_create_tests()

    def test_nosology_correct_update(self):
        """Тест на корректное изменение напрямую через БД."""
        self.correct_update_tests()

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_nosology_fields_validation(self):
    #     """Тест на валидацию некорректных значений напрямую через БД."""
    #     self.incorrect_field_tests()

    def test_nosology_fields_admit_values(self):
        """Тест на допуск корректных значений напрямую через БД."""
        self.correct_field_tests()

    def test_nosology_deletion(self):
        """Тест на удаление объекта напрямую через БД."""
        self.correct_delete_tests()

    def test_nosology_correct_create_via_admin(self):
        """Тест на корректное создание через административную часть."""
        self.correct_create_tests(url="/admin/main/nosology/add/")

    def test_nosology_correct_update_via_admin(self):
        """Тест на корректное изменение через административную часть."""
        url = f"/admin/main/nosology/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_nosology_fields_validation_via_admin(self):
    #     """Тест на валидацию некорректных значений полей через
    #     административную часть."""
    #     url = f"/admin/main/nosology/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_nosology_delete_via_admin(self):
        """Тест на корректное удаление через административную часть."""
        url = f"/admin/main/nosology/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_nosology_fields_admit_values_via_admin(self):
        """
        Тест на допуск корректных значений полей.

        Через административную часть.
        """
        url = f"/admin/main/nosology/{self.future_obj_id}/change/"
        self.correct_field_tests(url=url)


class DisciplineNameCrudTest(ModelTestBaseClass):
    """CRUD-тесты модели диагноза."""

    model = DisciplineName
    model_schema = DISCIPLINE_NAME_MODEL_TEST_SCHEMA

    def test_discipline_name_correct_creation(self):
        """Тест на корректное создание напрямую через БД."""
        self.correct_create_tests()

    def test_discipline_name_correct_update(self):
        """Тест на корректное изменение напрямую через БД."""
        self.correct_update_tests()

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_discipline_name_fields_validation(self):
    #     """Тест на валидацию некорректных значений напрямую через БД."""
    #     self.incorrect_field_tests()

    def test_discipline_name_fields_admit_values(self):
        """Тест на допуск корректных значений напрямую через БД."""
        self.correct_field_tests()

    def test_discipline_name_deletion(self):
        """Тест на удаление объекта напрямую через БД."""
        self.correct_delete_tests()

    def test_discipline_name_correct_create_via_admin(self):
        """Тест на корректное создание через административную часть."""
        self.correct_create_tests(url="/admin/main/disciplinename/add/")

    def test_discipline_name_correct_update_via_admin(self):
        """Тест на корректное изменение через административную часть."""
        url = f"/admin/main/disciplinename/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_discipline_name_fields_validation_via_admin(self):
    #     """Тест на валидацию некорректных значений полей через
    #     административную часть."""
    #     url = f"/admin/main/disciplinename/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_discipline_name_delete_via_admin(self):
        """Тест на корректное удаление через административную часть."""
        url = f"/admin/main/disciplinename/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_discipline_name_fields_admit_values_via_admin(self):
        """
        Тест на допуск корректных значений полей.

        Через административную часть.
        """
        url = f"/admin/main/disciplinename/{self.future_obj_id}/change/"
        self.correct_field_tests(url=url)


class DisciplineLevelCrudTest(ModelTestBaseClass):
    """CRUD-тесты модели уровня дисциплин."""

    model = DisciplineLevel
    model_schema = DISCIPLINE_LEVEL_MODEL_TEST_SCHEMA

    def test_discipline_level_correct_creation(self):
        """Тест на корректное создание напрямую через БД."""
        self.correct_create_tests()

    def test_discipline_level_correct_update(self):
        """Тест на корректное изменение напрямую через БД."""
        self.correct_update_tests()

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_discipline_level_fields_validation(self):
    #     """Тест на валидацию некорректных значений напрямую через БД."""
    #     self.incorrect_field_tests()

    def test_discipline_level_fields_admit_values(self):
        """Тест на допуск корректных значений напрямую через БД."""
        self.correct_field_tests()

    def test_discipline_level_deletion(self):
        """Тест на удаление объекта напрямую через БД."""
        self.correct_delete_tests()

    def test_discipline_level_correct_create_via_admin(self):
        """Тест на корректное создание через административную часть."""
        self.correct_create_tests(url="/admin/main/disciplinelevel/add/")

    def test_discipline_level_correct_update_via_admin(self):
        """Тест на корректное изменение через административную часть."""
        url = f"/admin/main/disciplinelevel/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_discipline_level_fields_validation_via_admin(self):
    #     """Тест на валидацию некорректных значений полей через
    #     административную часть."""
    #     url = f"/admin/main/disciplinelevel/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_discipline_level_delete_via_admin(self):
        """Тест на корректное удаление через административную часть."""
        url = f"/admin/main/disciplinelevel/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_discipline_level_fields_admit_values_via_admin(self):
        """
        Тест на допуск корректных значений полей.

        Через административную часть.
        """
        url = f"/admin/main/disciplinelevel/{self.future_obj_id}/change/"
        self.correct_field_tests(url=url)


class StaffMemberCrudTest(ModelTestBaseClass):
    """CRUD-тесты сотрудника."""

    model = StaffMember
    model_schema = STAFF_MEMBER_MODEL_TEST_SCHEMA

    def test_staff_member_correct_creation(self):
        """Тест на корректное создание напрямую через БД."""
        self.correct_create_tests()

    def test_staff_member_correct_update(self):
        """Тест на корректное изменение напрямую через БД."""
        self.correct_update_tests()

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_staff_member_fields_validation(self):
    # """Тест на валидацию некорректных значений напрямую через БД."""
    #     self.incorrect_field_tests()

    # def test_staff_member_fields_admit_values(self):
    # """Тест на допуск корректных значений напрямую через БД."""
    #     self.correct_field_tests()

    def test_staff_member_deletion(self):
        """Тест на удаление объекта напрямую через БД."""
        self.correct_delete_tests()

    def test_staff_member_correct_create_via_admin(self):
        """Тест на корректное создание через административную часть."""
        self.correct_create_tests(url="/admin/main/staffmember/add/")

    def test_staff_member_correct_update_via_admin(self):
        """Тест на корректное изменение через административную часть."""
        url = f"/admin/main/staffmember/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_staff_member_fields_validation_via_admin(self):
    #     """Тест на валидацию некорректных значений полей через
    #     административную часть."""
    #     url = f"/admin/main/staffmember/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_staff_member_delete_via_admin(self):
        """Тест на корректное удаление через административную часть."""
        url = f"/admin/main/staffmember/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_staff_member_fields_admit_values_via_admin(self):
    #     """Тест на допуск корректных значений полей через административную
    #     часть."""
    #     url = f"/admin/main/staffmember/{self.future_obj_id}/change/"
    #     self.correct_field_tests(url=url)


@pytest.mark.skip(reason="Модель StuffTeamMember был исключен из админки")
class StaffTeamMemberCrudTest(ModelTestBaseClass):
    """CRUD-тесты сотрудника команды."""

    model = StaffTeamMember
    model_schema = STAFF_TEAM_MEMBER_MODEL_TEST_SCHEMA

    def test_staff_team_member_correct_creation(self):
        """Тест на корректное создание напрямую через БД."""
        self.correct_create_tests()

    def test_staff_team_member_correct_update(self):
        """Тест на корректное изменение напрямую через БД."""
        self.correct_update_tests()

    def test_staff_team_member_fields_validation(self):
        """Тест на валидацию некорректных значений напрямую через БД."""
        self.incorrect_field_tests()

    def test_staff_team_member_fields_admit_values(self):
        """Тест на допуск корректных значений напрямую через БД."""
        self.correct_field_tests()

    def test_staff_team_member_deletion(self):
        """Тест на удаление объекта напрямую через БД."""
        self.correct_delete_tests()

    def test_staff_team_member_correct_create_via_admin(self):
        """Тест на корректное создание через административную часть."""
        schema = self.get_correct_create_schema()
        schema["team"] = "1"
        self.correct_create_tests(
            schema,
            url="/admin/main/staffteammember/add/",
        )

    def test_staff_team_member_correct_update_via_admin(self):
        """Тест на корректное изменение через административную часть."""
        url = f"/admin/main/staffteammember/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить", team="1")

    def test_staff_team_member_fields_validation_via_admin(self):
        """
        Тест на валидацию некорректных значений полей.

        Через административную часть.
        """
        url = f"/admin/main/staffteammember/{self.future_obj_id}/change/"
        self.incorrect_field_tests_via_url(url=url, _save="Сохранить", team=1)

    def test_staff_team_member_delete_via_admin(self):
        """Тест на корректное удаление через административную часть."""
        url = f"/admin/main/staffteammember/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_staff_team_member_fields_admit_values_via_admin(self):
        """
        Тест на допуск корректных значений полей.

        Через административную часть.
        """
        url = f"/admin/main/staffteammember/{self.future_obj_id}/change/"
        self.correct_field_tests(url=url, team=1)

    #  TODO: Раскомментировать и доработать все тесты на стаффтиммембера
    #   через сайт, поскольку вьюха работает некорректно в принципе: она
    #   запитана на модель StaffMember, в то время как должна быть
    #   задействована модель StaffTeamMember. Соответственно, если у нас
    #   один человек занимает две должности в команде, то:
    #   1. Не отображаются обе записи
    #   2. При удалении одной удаляются две, поскольку происходит касакадное
    #   удаление.

    # def test_staff_team_member_correct_create_via_http(self):
    #     """Тест на корректное создание через сайт."""
    #     schema = self.get_correct_create_schema()
    #     schema["team"] = "1"
    #     self.correct_create_tests(
    #         schema, url="/staffs/create/"
    #     )
    #
    # def test_staff_team_member_correct_update_via_http(self):
    #     """Тест на корректное изменение через сайт."""
    #     url = f"/staffs/{self.future_obj_id}/edit/"
    #     self.correct_update_tests(url=url, _save="Сохранить", team="1")
    #
    # def test_staff_team_member_fields_validation_via_http(self):
    #     """Тест на валидацию некорректных значений полей через сайт."""
    #     url = f"/staffs/{self.future_obj_id}/edit/"
    #     self.incorrect_field_tests_via_url(
    #       url=url, _save="Сохранить", team=1
    #      )
    #
    # def test_staff_team_member_delete_via_http(self):
    #     """Тест на корректное удаление через сайт."""
    #     url = f"/staffs/{self.future_obj_id}/delete/"
    #     self.correct_delete_tests(url=url)
    #
    # def test_staff_team_member_fields_admit_values_via_http(self):
    #     """Тест на допуск корректных значений полей через сайт."""
    #     url = f"/staffs/{self.future_obj_id}/edit/"
    #     self.correct_field_tests(url=url, team=1)


class TeamCrudTest(ModelTestBaseClass):
    """CRUD-тесты команды."""

    model = Team
    model_schema = TEAM_MODEL_TEST_SCHEMA
    user_agent: User | Any = None
    admin_inlines_no_player_no_staff = {
        "StaffTeamMember_team-TOTAL_FORMS": 0,
        "StaffTeamMember_team-INITIAL_FORMS": 0,
        "Player_team-TOTAL_FORMS": 0,
        "Player_team-INITIAL_FORMS": 0,
    }

    @classmethod
    def setUpClass(cls) -> None:
        """Классовый метод для базовой настройки всех тестов класса."""
        super().setUpClass()
        cls.user_agent = UserFactory.create(role=Role.AGENT)

    def get_correct_create_schema(self):
        """Метод на формирование корректной схемы создания объектов."""
        schema = super(TeamCrudTest, self).get_correct_create_schema()
        schema["curator"] = self.user_agent
        return schema

    def get_correct_update_schema(self):
        """Метод на формирование корректной схемы обновления объектов."""
        schema = super().get_correct_update_schema()
        schema["curator"] = self.user_agent
        return schema

    def test_team_correct_creation(self):
        """Тест на корректное создание напрямую через БД."""
        self.correct_create_tests()

    def test_team_correct_update(self):
        """Тест на корректное изменение напрямую через БД."""
        self.correct_update_tests()

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_team_fields_validation(self):
    # """Тест на валидацию некорректных значений напрямую через БД."""
    #     self.incorrect_field_tests()

    def test_team_fields_admit_values(self):
        """Тест на допуск корректных значений напрямую через БД."""
        self.correct_field_tests()

    def test_team_deletion(self):
        """Тест на удаление объекта напрямую через БД."""
        self.correct_delete_tests()

    def test_team_create_via_http(self):
        """Тест на корректное создание через сайт."""
        self.correct_create_tests(url="/teams/create/")

    def test_team_update_via_http(self):
        """Тест на корректное изменение через сайт."""
        url = f"/teams/{self.future_obj_id}/edit/"
        self.correct_update_tests(url=url)

    def test_team_delete_via_http(self):
        """Тест на корректное удаление через сайт."""
        url = f"/teams/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url)

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_team_fields_validation_via_http(self):
    #     """Тест на валидацию некорректных значений полей через сайт."""
    #     url = f"/teams/{self.future_obj_id}/edit/"
    #     self.incorrect_field_tests_via_url(url=url)

    def test_team_fields_admit_values_via_http(self):
        """Тест на допуск корректных значений полей через сайт."""
        url = f"/teams/{self.future_obj_id}/edit/"
        self.correct_field_tests(url=url)

    def test_team_correct_create_via_admin(self):
        """Тест на корректное создание через административную часть."""
        self.correct_create_tests(
            url="/admin/main/team/add/",
            **self.admin_inlines_no_player_no_staff,
        )

    def test_team_correct_update_via_admin(self):
        """Тест на корректное изменение через административную часть."""
        url = f"/admin/main/team/{self.future_obj_id}/change/"
        self.correct_update_tests(
            url=url,
            _save="Сохранить",
            **self.admin_inlines_no_player_no_staff,
        )

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_team_fields_validation_via_admin(self):
    #     """Тест на валидацию некорректных значений полей через
    #     административную часть."""
    #     url = f"/admin/main/team/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(
    #         url=url, _save="Сохранить",
    #         **self.admin_inlines_no_player_no_staff
    #     )

    def test_team_delete_via_admin(self):
        """Тест на корректное удаление через административную часть."""
        self.client.force_login(self.superuser)
        url = f"/admin/main/team/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_team_fields_admit_values_via_admin(self):
        """
        Тест на допуск корректных значений полей.

        Через административную часть.
        """
        url = f"/admin/main/team/{self.future_obj_id}/change/"
        self.correct_field_tests(
            url=url,
            **self.admin_inlines_no_player_no_staff,
        )


class PlayerCrudTest(ModelTestBaseClass):
    """CRUD-тесты игрока."""

    model = Player
    model_schema = PLAYER_MODEL_TEST_SCHEMA
    user_agent: User | Any = None

    admin_inlines_no_team_no_docs = {
        "player_documemts-TOTAL_FORMS": 0,
        "player_documemts-INITIAL_FORMS": 0,
        "Player_team-TOTAL_FORMS": 0,
        "Player_team-INITIAL_FORMS": 0,
    }

    def test_player_correct_creation(self):
        """Тест на корректное создание напрямую через БД."""
        self.correct_create_tests()

    def test_player_correct_update(self):
        """Тест на корректное изменение напрямую через БД."""
        self.correct_update_tests()

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_player_fields_validation(self):
    # """Тест на валидацию некорректных значений напрямую через БД."""
    #     self.incorrect_field_tests()

    # def test_player_fields_admit_values(self):
    # """Тест на допуск корректных значений напрямую через БД."""
    #     self.correct_field_tests()

    def test_player_deletion(self):
        """Тест на удаление объекта напрямую через БД."""
        self.correct_delete_tests()

    def test_player_create_via_http(self):
        """Тест на корректное создание через сайт."""
        self.correct_create_tests(
            url="/players/create/",
            team=1,
            nosology=1,
            diagnosis=1,
        )

    def test_player_update_via_http(self):
        """Тест на корректное изменение через сайт."""
        url = f"/players/{self.future_obj_id}/edit/"
        self.correct_update_tests(url=url, team=1, nosology=1, diagnosis=1)

    def test_player_delete_via_http(self):
        """Тест на корректное удаление через сайт."""
        url = f"/players/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url)

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_player_fields_validation_via_http(self):
    #     """Тест на валидацию некорректных значений полей через сайт."""
    #     url = f"/players/{self.future_obj_id}/edit/"
    #     self.incorrect_field_tests_via_url(url=url, team=1)

    # def test_player_fields_admit_values_via_http(self):
    #     """Тест на допуск корректных значений полей через сайт."""
    #     url = f"/players/{self.future_obj_id}/edit/"
    #     self.correct_field_tests(url=url, team=1)

    def test_player_correct_create_via_admin(self):
        """Тест на корректное создание через административную часть."""
        self.correct_create_tests(
            url="/admin/main/player/add/",
            **self.admin_inlines_no_team_no_docs,
            team=1,
            nosology=1,
            diagnosis=1,
        )

    def test_player_correct_update_via_admin(self):
        """Тест на корректное изменение через административную часть."""
        url = f"/admin/main/player/{self.future_obj_id}/change/"
        self.correct_update_tests(
            url=url,
            _save="Сохранить",
            **self.admin_inlines_no_team_no_docs,
            team=1,
            nosology=1,
            diagnosis=1,
        )

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_player_fields_validation_via_admin(self):
    #     """Тест на валидацию некорректных значений полей через
    #     административную часть."""
    #     url = f"/admin/main/player/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(
    #         url=url,
    #         team=1,
    #         _save="Сохранить",
    #         **self.admin_inlines_no_team_no_docs,
    #     )

    def test_player_delete_via_admin(self):
        """Тест на корректное удаление через административную часть."""
        self.client.force_login(self.superuser)
        url = f"/admin/main/player/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    # TODO: Раскомментировать после согласования объема валидаций и
    #  доработки валидации полей модели.

    # def test_player_fields_admit_values_via_admin(self):
    #     """Тест на допуск корректных значений полей через административную
    #     часть."""
    #     url = f"/admin/main/player/{self.future_obj_id}/change/"
    #     self.correct_field_tests(
    #         url=url,
    #         team=1,
    #         **self.admin_inlines_no_team_no_docs,
    #     )


# TODO: Сделать тест модели Document.
# TODO: Аналогично для Competitions и Unloads.
# TODO: Не очень понял, зачем нам файл сommand_test.
# TODO: там по сути 4 CRUD теста для команд,
# TODO: которые у нас уже есть в этом файле.
# TODO: Нужно решить, что мы делаем с тестами админки:
# TODO: Либо удаляем, либо дописываем. То же самое с тестами на валидацию.
# TODO: Соответственно, когда мы решим, в каком направлении мы двигаемся
# TODO: Соответственно, когда мы решим, в каком направлении мы двигаемся
