from typing import Any

from core.constants import ROLE_AGENT
from main.models import (
    City,
    Diagnosis,
    Player,
    StaffMember,
    StaffTeamMember,
    Team,
)
from tests.base import ModelTestBaseClass
from tests.models_schema import (
    CITY_MODEL_TEST_SCHEMA,
    DIAGNOSIS_MODEL_TEST_SCHEMA,
    GROUP_MODEL_TEST_SCHEMA,
    PLAYER_MODEL_TEST_SCHEMA,
    STAFF_MEMBER_MODEL_TEST_SCHEMA,
    STAFF_TEAM_MEMBER_MODEL_TEST_SCHEMA,
    TEAM_MODEL_TEST_SCHEMA,
    USER_MODEL_TEST_SCHEMA,
)
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

    # def test_user_fields_validation(self):
    #     self.incorrect_field_tests()

    # def test_user_fields_admit_values(self):
    #     self.correct_field_tests()

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

    # def test_user_fields_validation_via_http(self):
    #     object_id_estimated = User.objects.count() + 1
    #     url = f"/users/{object_id_estimated}/edit/"
    #     self.incorrect_field_tests_via_url(url=url)

    # def test_user_fields_admit_values_via_http(self):
    #     object_id_estimated = User.objects.count() + 1
    #     url = f"/users/{object_id_estimated}/edit/"
    #     self.correct_field_tests(url=url)

    def test_user_correct_create_via_admin(self):
        self.correct_create_tests(url="/admin/users/user/add/")

    def test_user_correct_update_via_admin(self):
        url = f"/admin/users/user/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    # def test_user_fields_validation_via_admin(self):
    #     url = f"/admin/users/user/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_user_delete_via_admin(self):
        self.client.force_login(self.superuser)
        url = f"/admin/users/user/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    # def test_user_fields_admit_values_via_admin(self):
    #     url = f"/admin/users/user/{self.future_obj_id}/change/"
    #     self.correct_field_tests(url=url)


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


class CityCrudTest(ModelTestBaseClass):
    model = City
    model_schema = CITY_MODEL_TEST_SCHEMA

    def test_city_correct_creation(self):
        self.correct_create_tests()

    def test_city_correct_update(self):
        self.correct_update_tests()

    # def test_city_fields_validation(self):
    #     self.incorrect_field_tests()

    def test_city_fields_admit_values(self):
        self.correct_field_tests()

    def test_city_deletion(self):
        self.correct_delete_tests()

    def test_city_correct_create_via_admin(self):
        self.correct_create_tests(url="/admin/main/city/add/")

    def test_city_correct_update_via_admin(self):
        url = f"/admin/main/city/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    # def test_city_fields_validation_via_admin(self):
    #     url = f"/admin/main/city/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_city_delete_via_admin(self):
        url = f"/admin/main/city/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_city_fields_admit_values_via_admin(self):
        url = f"/admin/main/city/{self.future_obj_id}/change/"
        self.correct_field_tests(url=url)


class DiagnosisCrudTest(ModelTestBaseClass):
    model = Diagnosis
    model_schema = DIAGNOSIS_MODEL_TEST_SCHEMA

    def test_diagnosis_correct_creation(self):
        self.correct_create_tests()

    def test_diagnosis_correct_update(self):
        self.correct_update_tests()

    # def test_diagnosis_fields_validation(self):
    #     self.incorrect_field_tests()

    def test_diagnosis_fields_admit_values(self):
        self.correct_field_tests()

    def test_diagnosis_deletion(self):
        self.correct_delete_tests()

    def test_diagnosis_correct_create_via_admin(self):
        self.correct_create_tests(url="/admin/main/diagnosis/add/")

    def test_diagnosis_correct_update_via_admin(self):
        url = f"/admin/main/diagnosis/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    # def test_diagnosis_fields_validation_via_admin(self):
    #     url = f"/admin/main/diagnosis/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_diagnosis_delete_via_admin(self):
        url = f"/admin/main/diagnosis/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_diagnosis_fields_admit_values_via_admin(self):
        url = f"/admin/main/diagnosis/{self.future_obj_id}/change/"
        self.correct_field_tests(url=url)


class StaffMemberCrudTest(ModelTestBaseClass):
    model = StaffMember
    model_schema = STAFF_MEMBER_MODEL_TEST_SCHEMA

    def test_staff_member_correct_creation(self):
        self.correct_create_tests()

    def test_staff_member_correct_update(self):
        self.correct_update_tests()

    # def test_staff_member_fields_validation(self):
    #     self.incorrect_field_tests()

    # def test_staff_member_fields_admit_values(self):
    #     self.correct_field_tests()

    def test_staff_member_deletion(self):
        self.correct_delete_tests()

    def test_staff_member_correct_create_via_admin(self):
        self.correct_create_tests(url="/admin/main/staffmember/add/")

    def test_staff_member_correct_update_via_admin(self):
        url = f"/admin/main/staffmember/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить")

    # def test_staff_member_fields_validation_via_admin(self):
    #     url = f"/admin/main/staffmember/{self.future_obj_id}/change/"
    #     self.incorrect_field_tests_via_url(url=url, _save="Сохранить")

    def test_staff_member_delete_via_admin(self):
        url = f"/admin/main/staffmember/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    # def test_staff_member_fields_admit_values_via_admin(self):
    #     url = f"/admin/main/staffmember/{self.future_obj_id}/change/"
    #     self.correct_field_tests(url=url)


class StaffTeamMemberCrudTest(ModelTestBaseClass):
    model = StaffTeamMember
    model_schema = STAFF_TEAM_MEMBER_MODEL_TEST_SCHEMA

    def test_staff_team_member_correct_creation(self):
        self.correct_create_tests()

    def test_staff_team_member_correct_update(self):
        self.correct_update_tests()

    def test_staff_team_member_fields_validation(self):
        self.incorrect_field_tests()

    def test_staff_team_member_fields_admit_values(self):
        self.correct_field_tests()

    def test_staff_team_member_deletion(self):
        self.correct_delete_tests()

    def test_staff_team_member_correct_create_via_admin(self):
        schema = self.get_correct_create_schema()
        schema["team"] = "1"
        self.correct_create_tests(
            schema, url="/admin/main/staffteammember/add/"
        )

    def test_staff_team_member_correct_update_via_admin(self):
        url = f"/admin/main/staffteammember/{self.future_obj_id}/change/"
        self.correct_update_tests(url=url, _save="Сохранить", team="1")

    def test_staff_team_member_fields_validation_via_admin(self):
        url = f"/admin/main/staffteammember/{self.future_obj_id}/change/"
        self.incorrect_field_tests_via_url(url=url, _save="Сохранить", team=1)

    def test_staff_team_member_delete_via_admin(self):
        url = f"/admin/main/staffteammember/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_staff_team_member_fields_admit_values_via_admin(self):
        url = f"/admin/main/staffteammember/{self.future_obj_id}/change/"
        self.correct_field_tests(url=url, team=1)


class TeamCrudTest(ModelTestBaseClass):
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
        super().setUpClass()
        cls.user_agent = UserFactory.create(role=ROLE_AGENT)

    def get_correct_create_schema(self):
        schema = super(TeamCrudTest, self).get_correct_create_schema()
        schema["curator"] = self.user_agent
        return schema

    def get_correct_update_schema(self):
        schema = super().get_correct_update_schema()
        schema["curator"] = self.user_agent
        return schema

    def test_team_correct_creation(self):
        self.correct_create_tests()

    def test_team_correct_update(self):
        self.correct_update_tests()

    def test_team_fields_validation(self):
        self.incorrect_field_tests()

    def test_team_fields_admit_values(self):
        self.correct_field_tests()

    def test_team_deletion(self):
        self.correct_delete_tests()

    def test_team_create_via_http(self):
        self.correct_create_tests(url="/teams/create/")

    def test_team_update_via_http(self):
        url = f"/teams/{self.future_obj_id}/edit/"
        self.correct_update_tests(url=url)

    def test_team_delete_via_http(self):
        url = f"/teams/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url)

    def test_team_fields_validation_via_http(self):
        url = f"/teams/{self.future_obj_id}/edit/"
        self.incorrect_field_tests_via_url(url=url)

    def test_team_fields_admit_values_via_http(self):
        url = f"/teams/{self.future_obj_id}/edit/"
        self.correct_field_tests(url=url)

    def test_team_correct_create_via_admin(self):
        self.correct_create_tests(
            url="/admin/main/team/add/",
            **self.admin_inlines_no_player_no_staff,
        )

    def test_team_correct_update_via_admin(self):
        url = f"/admin/main/team/{self.future_obj_id}/change/"
        self.correct_update_tests(
            url=url,
            _save="Сохранить",
            **self.admin_inlines_no_player_no_staff,
        )

    def test_team_fields_validation_via_admin(self):
        url = f"/admin/main/team/{self.future_obj_id}/change/"
        self.incorrect_field_tests_via_url(
            url=url, _save="Сохранить", **self.admin_inlines_no_player_no_staff
        )

    def test_team_delete_via_admin(self):
        self.client.force_login(self.superuser)
        url = f"/admin/main/team/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_team_fields_admit_values_via_admin(self):
        url = f"/admin/main/team/{self.future_obj_id}/change/"
        self.correct_field_tests(
            url=url, **self.admin_inlines_no_player_no_staff
        )


class PlayerCrudTest(ModelTestBaseClass):
    model = Player
    model_schema = PLAYER_MODEL_TEST_SCHEMA
    user_agent: User | Any = None

    admin_inlines_no_team_no_docs = {
        "player_documemts-TOTAL_FORMS": 0,
        "player_documemts-INITIAL_FORMS": 0,
        "Player_team-TOTAL_FORMS": 0,
        "Player_team-INITIAL_FORMS": 0,
    }

    # @classmethod
    # def setUpClass(cls) -> None:
    #     super().setUpClass()
    #     cls.user_agent = UserFactory.create(role=ROLE_AGENT)
    #
    # def get_correct_create_schema(self):
    #     schema = super().get_correct_create_schema()
    #     schema["team"] = "1"
    #     return schema
    #
    # def get_correct_update_schema(self):
    #     schema = super().get_correct_update_schema()
    #     schema["team"] = "1"
    #     return schema

    def test_player_correct_creation(self):
        self.correct_create_tests()

    def test_player_correct_update(self):
        self.correct_update_tests()

    def test_player_fields_validation(self):
        self.incorrect_field_tests()

    def test_player_fields_admit_values(self):
        self.correct_field_tests()

    def test_player_deletion(self):
        self.correct_delete_tests()

    def test_player_create_via_http(self):
        self.correct_create_tests(url="/players/create/", team=1)

    def test_player_update_via_http(self):
        url = f"/players/{self.future_obj_id}/edit/"
        self.correct_update_tests(url=url, team=1)

    def test_player_delete_via_http(self):
        url = f"/players/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url)

    def test_player_fields_validation_via_http(self):
        url = f"/players/{self.future_obj_id}/edit/"
        self.incorrect_field_tests_via_url(url=url, team=1)

    def test_player_fields_admit_values_via_http(self):
        url = f"/players/{self.future_obj_id}/edit/"
        self.correct_field_tests(url=url, team=1)

    def test_player_correct_create_via_admin(self):
        self.correct_create_tests(
            url="/admin/main/player/add/",
            **self.admin_inlines_no_team_no_docs,
            team=1,
        )

    def test_player_correct_update_via_admin(self):
        url = f"/admin/main/player/{self.future_obj_id}/change/"
        self.correct_update_tests(
            url=url,
            _save="Сохранить",
            **self.admin_inlines_no_team_no_docs,
            team=1,
        )

    def test_player_fields_validation_via_admin(self):
        url = f"/admin/main/player/{self.future_obj_id}/change/"
        self.incorrect_field_tests_via_url(
            url=url,
            team=1,
            _save="Сохранить",
            **self.admin_inlines_no_team_no_docs,
        )

    def test_player_delete_via_admin(self):
        self.client.force_login(self.superuser)
        url = f"/admin/main/player/{self.future_obj_id}/delete/"
        self.correct_delete_tests(url=url, post="yes")

    def test_player_fields_admit_values_via_admin(self):
        url = f"/admin/main/player/{self.future_obj_id}/change/"
        self.correct_field_tests(
            url=url,
            team=1,
            **self.admin_inlines_no_team_no_docs,
        )
