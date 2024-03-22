import re
from http import HTTPStatus
from typing import Iterable

from competitions.models import Competition
from core.constants import ROLE_SUPERUSER
from django.test import Client, TestCase
from main.data_factories.factories import (
    CompetitionFactory,
    DiagnosisFactory,
    DisciplineNameFactory,
    DocumentFactory,
    PlayerFactory,
    StaffTeamMemberFactory,
    TeamFactory,
)
from main.models import (
    Diagnosis,
    DisciplineName,
    Document,
    Player,
    StaffTeamMember,
    Team,
)
from tests.url_test import TEST_GROUP_NAME
from users.factories import UserFactory
from users.models import ProxyGroup, User

URL_MSG = (
    "{method} запрос по адресу: {msg_url} должен вернуть ответ со статусом "
    "{status_code}. Тестировался запрос по адресу: {url}"
)


class BaseTestClass(TestCase):
    """Базовый класс для тестирования.
    При инициализации создает в тестовой БД по одному экземпляру каждой из
    задействованных в приложении моделей. Пользователей создается два:
    суперпользователь и обычный пользователь."""

    superuser: User
    user: User
    discipline_name: DisciplineName
    teams: Team
    diagnosis: Diagnosis
    player: Player
    staff: StaffTeamMember
    competition: Competition
    document: Document

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
        ProxyGroup.objects.create(name=TEST_GROUP_NAME).save()
        cls.document = DocumentFactory.create(player=cls.player)


class UrlTestMixin:
    """Миксин предоставляет унифицированный метод для тестирования
    урл-адресов, с генерацией информативного сообщения."""

    @staticmethod
    def _render_url(url: str, subs: tuple | str):
        pattern = re.compile(r"<[^/]+>")
        if not re.search(pattern, url):
            return url
        if isinstance(subs, str):
            subs = (subs,)
        for sub in subs:
            url = re.sub(pattern, sub, url, 1)
        if re.search(pattern, url):
            url = re.sub(pattern, subs[-1], url)
        return url

    def get_default_client(self) -> Client:
        """Переопределите этот метод для тестирования по умолчанию клиентом,
        отличным от простого неавторизованного."""
        return getattr(self, "client")

    def url_get_test(
        self,
        urls: Iterable | str,
        method: str = "get",
        status_code: int = HTTPStatus.OK,
        subs: tuple[str, ...] | str = "1",
        client: Client | None = None,
        message: str | None = None,
    ):
        """Унифицированный метод для урл-тестов.
        - urls: урл-адрес либо список или кортеж урл-адресов, подлежащих
          тестированию;
        - method: метод запроса (обычно "get" или "post", по умолчанию -
          "get");
        - status_code: ожидаемый ответ, по умолчанию - 200.
        - subs: строка или кортеж строк подстановки вместо
          динамических идентификаторов объектов типа <int:pk> в урл-путях.
          Например, для обработки пути:
          "/competitions/<int:competition_id>/teams/<int:pk>/add/"
          если передать кортеж ("1", "2"), то он преобразует путь в
          "/competitions/1/teams/2/add/").
          Если подстановок больше, чем элементов в кортеже "subs", то для
          оставшихся подстановок возьмется последний элемент. Если в примере
          выше передать строку "1" или кортеж ("1",), то урл преобразуется в
          "/competitions/1/teams/1/add/". Если в урл нет динамических
          идентификаторов, данный параметр не имеет значения.
        - client: клиент для тестирования.
          Если не определить этот параметр, то клиент будет получен из
          метода get_default_client(). Если метод get_default_client() не
          переопределен в классе, то тестирование будет проводиться с
          простым неавторизованным клиентом.
        - message: кастомное сообщение в случае непрохождения теста,
          если генерируемое методом сообщение по каким-то причинам не
          устраивает.
        """
        client = client or self.get_default_client()
        if isinstance(urls, str):
            urls = (urls,)
        for url in urls:
            url_for_message = url
            url = self._render_url(url, subs)
            msg = message or URL_MSG.format(
                method=method.upper(),
                msg_url=url_for_message,
                status_code=status_code,
                url=url,
            )
            with self.__getattribute__("subTest")(url=url):
                response = client.__getattribute__(method.lower())(url)
                self.__getattribute__("assertEqual")(
                    response.status_code,
                    status_code,
                    msg=msg,
                )
