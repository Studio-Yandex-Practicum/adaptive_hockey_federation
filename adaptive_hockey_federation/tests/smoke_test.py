from http import HTTPStatus

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
    "GET запрос по адресу: {url} должен вернуть ответ со статусом " "200."
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

    def test_competitions_simple_access(self):
        """Тест доступности страниц с соревнованиями."""
        for url in COMPETITIONS_URLS:
            with self.subTest(url=url):
                response = self.super_client.get(url)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    msg=URL_MSG_GET.format(url=url),
                )
