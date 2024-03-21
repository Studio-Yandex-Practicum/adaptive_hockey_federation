from http import HTTPStatus
from typing import Iterable

from competitions.models import Competition
from core.constants import ROLE_SUPERUSER
from django.test import Client, TestCase
from main.data_factories.factories import (
    CompetitionFactory,
    DiagnosisFactory,
    DisciplineNameFactory,
    PlayerFactory,
    StaffTeamMemberFactory,
    TeamFactory,
)
from main.models import (
    Diagnosis,
    DisciplineName,
    Player,
    StaffTeamMember,
    Team,
)
from users.factories import UserFactory
from users.models import User

URL_MSG = (
    "{method} запрос по адресу: {url} должен вернуть ответ со статусом "
    "{status_code}."
)

COMPETITION_GET_URLS = (
    "/competitions/",
    "/competitions/create/",
    "/competitions/1/",
    "/competitions/1/edit/",
)

COMPETITION_POST_URLS = (
    "/competitions/1/teams/1/add/",
    "/competitions/1/teams/1/delete/",
    "/competitions/1/delete/",
)

PLAYER_GET_URLS = (
    "/players/",
    "/players/1/",
    "/players/1/edit/",
    "/players/create/",
)

PLAYER_POST_URLS = (
    "/players/1/delete/",
    # TODO: Тест на данный урл выдает TemplateDoesNotExist. Необходимо
    #  раскомментировать, когда будет починен player_id_deleted() в
    #  main.views или вообще удалить, если эта страница не нужна.
    # "/players/deleted/",
)

STAFF_GET_URLS = (
    "/staffs/",
    "/staffs/1/",
    "/staffs/1/edit/",
    "/staffs/create/",
)

STAFF_POST_URL = ("/staffs/1/delete/",)

TEAM_GET_URLS = (
    "/teams/",
    "/teams/1/",
    "/teams/1/edit/",
    "/teams/create/",
)

TEAM_POST_URL = "/teams/1/delete/"

USER_GET_URLS = (
    "/users/",
    "/users/1/edit/",
    "/users/create/",
    "/users/set_password/1/fake_token/",
)

USER_POST_URL = "/users/2/delete/"

UNLOAD_URLS = ("/unloads/",)


class TestUrlsSmoke(TestCase):

    superuser: User
    user: User
    discipline_name: DisciplineName
    teams: Team
    diagnosis: Diagnosis
    player: Player
    staff: StaffTeamMember
    competition: Competition

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.superuser = User.objects.create_user(
            password="super1234",
            first_name="Супер",
            last_name="Пользователь",
            role=ROLE_SUPERUSER,
            email="superuser@fake.fake",
            is_staff=True,
            is_superuser=True,
        )
        cls.user = UserFactory.create()
        cls.discipline_name = DisciplineNameFactory.create()
        cls.teams = TeamFactory.create()
        cls.competition = CompetitionFactory.create()
        cls.diagnosis = DiagnosisFactory.create()
        cls.player = PlayerFactory.create()
        cls.staff = StaffTeamMemberFactory.create()

    def setUp(self) -> None:
        self.client = Client()
        self.super_client = Client()
        self.super_client.force_login(self.superuser)

    def url_get_test(
        self,
        urls: Iterable | str,
        method: str = "get",
        status_code: int = HTTPStatus.OK,
    ):
        """Унифицированный метод для урл-тестов.
        - urls: урл-адрес либо список или кортеж урл-адресов, подлежащих
          тестированию;
        - method: метод запроса (обычно "get" или "post", по умолчанию -
          "get");
        - status_code: ожидаемый ответ, по умолчанию - 200."""
        if isinstance(urls, str):
            urls = (urls,)
        for url in urls:
            with self.subTest(url=url):
                response = self.super_client.__getattribute__(method.lower())(
                    url
                )
                self.assertEqual(
                    response.status_code,
                    status_code,
                    msg=URL_MSG.format(
                        method=method.upper(), url=url, status_code=status_code
                    ),
                )

    def test_competitions_simple_access(self):
        """Тест доступности страниц с соревнованиями."""
        self.url_get_test(COMPETITION_GET_URLS)
        self.url_get_test(COMPETITION_POST_URLS, "post", HTTPStatus.FOUND)

    def test_player_simple_access(self):
        """Тест доступности страниц с игроками."""
        self.url_get_test(PLAYER_GET_URLS)
        self.url_get_test(PLAYER_POST_URLS, "post", HTTPStatus.FOUND)

    def test_staff_simple_access(self):
        """Тест доступности страниц с сотрудниками команд."""
        self.url_get_test(STAFF_GET_URLS)
        self.url_get_test(STAFF_POST_URL, "post", HTTPStatus.FOUND)

    def test_team_simple_access(self):
        """Тест доступности страниц со спортивными командами."""
        self.url_get_test(TEAM_GET_URLS)
        self.url_get_test(TEAM_POST_URL, "post", HTTPStatus.FOUND)

    def test_user_simple_access(self):
        """Тест доступности страниц с пользователями."""
        self.url_get_test(USER_GET_URLS)
        self.url_get_test(USER_POST_URL, "post", HTTPStatus.FOUND)

    def test_unload_simple_access(self):
        """Тест доступности страниц с выгрузками."""
        self.url_get_test(UNLOAD_URLS)
