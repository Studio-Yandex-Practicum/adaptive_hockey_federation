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
from users.models import User

URL_MSG_GET = (
    "{method} запрос по адресу: {url} должен вернуть ответ со статусом "
    "{status_code}."
)

COMPETITIONS_URLS = (
    "/competitions/",
    "/competitions/create/",
    # "/competitions/competitions/1/teams/1/add/", 404 (нужен post запрос)
    # "/competitions/1/teams/1/delete/", template does not exist
    "/competitions/1/",
    "/competitions/1/edit/",
    # "/competitions/1/delete/", template does not exist
)
PLAYER_URLS = (
    "/players/",
    "/players/1/",
    # "/players/1/delete/", template does not exist
    "/players/1/edit/",
    "/players/create/",
    # "/players/deleted/", template does not exist
)

STAFF_URLS = (
    "/staffs/",
    "/staffs/1/",
    # '/staffs/1/delete/', template does not exist
    "/staffs/1/edit/",
    "/staffs/create/",
)

TEAM_URLS = (
    "/teams/",
    "/teams/1/",
    # '/teams/1/delete/', template does not exist
    "/teams/1/edit/",
    "/teams/create/",
)
# '/unloads/',
# '/users/',
# '/users/<int:pk>/delete/',
# '/users/<int:pk>/edit/',
# '/users/create/',
# '/users/set_password/<uidb64>/<token>/'


class TestUrlsSmoke(TestCase):

    superuser: User
    discipline_name: DisciplineName
    team: Team
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
        cls.discipline_name = DisciplineNameFactory.create()
        cls.team = TeamFactory.create()
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
        urls: Iterable,
        method: str = "get",
        status_code: int = HTTPStatus.OK,
    ):
        """Унифицированный метод для урл-тестов.
        - urls: список или кортеж урл-адресов, подлежащих тестированию
        - method: метод запроса (обычно "get" или "post", по умолчанию -
        "get")
        - status_code: ожидаемый ответ."""
        for url in urls:
            with self.subTest(url=url):
                response = self.super_client.__getattribute__(method.lower())(
                    url
                )
                self.assertEqual(
                    response.status_code,
                    status_code,
                    msg=URL_MSG_GET.format(
                        method=method.upper(), url=url, status_code=status_code
                    ),
                )

    def test_competitions_simple_access(self):
        """Тест доступности страниц с соревнованиями."""
        self.url_get_test(COMPETITIONS_URLS)

    def test_player_simple_access(self):
        """Тест доступности страниц с игроками."""
        self.url_get_test(PLAYER_URLS)

    def test_staff_simple_access(self):
        """Тест доступности страниц с сотрудниками команд."""
        self.url_get_test(STAFF_URLS)

    def test_team_simple_access(self):
        """Тест доступности страниц с сотрудниками команд."""
        self.url_get_test(TEAM_URLS)
