import random
import pytz
from datetime import date, timedelta, datetime
from io import BytesIO

import factory
from competitions.models import Competition
from django.core.files.base import File
from django.db.models import Count
from games.models import Game
from main.models import (
    GENDER_CHOICES,
    PLAYER_POSITION_CHOICES,
    City,
    Diagnosis,
    DisciplineName,
    Document,
    GameDataPlayer,
    Nosology,
    Player,
    StaffMember,
    StaffTeamMember,
    Team,
)
from PIL import Image
from users.models import User

from .utils import check_len, get_random_objects

SIZE_IMAGE = (100, 100)
COLOR_IMAGE = (256, 0, 0)
FORMAT_IMAGE = "RGBA"
EXT_IMAGE = "png"


class CityFactory(factory.django.DjangoModelFactory):
    """Создания данных городов. Название города является уникальным."""

    class Meta:
        model = City
        django_get_or_create = ["name"]

    name = factory.Faker("city", locale="ru_RU")


class StaffMemberFactory(factory.django.DjangoModelFactory):
    """Создание сотрудников команд."""

    class Meta:
        model = StaffMember

    surname = factory.Faker("last_name", locale="ru_RU")
    name = factory.Faker("first_name", locale="ru_RU")
    patronymic = factory.Faker("middle_name", locale="ru_RU")
    phone = factory.Faker("phone_number", locale="ru_RU")


class StaffTeamMemberFactory(factory.django.DjangoModelFactory):
    """
    Создание данных о сотрудниках привязаных к командам.

    Квалификация может быть "Тренер" и "Другие сотрудники".
    """

    class Meta:
        model = StaffTeamMember
        skip_postgeneration_save = True

    staff_member = factory.SubFactory(StaffMemberFactory)
    qualification = factory.Faker(
        "sentence",
        nb_words=5,
        locale="ru_RU",
    )
    notes = factory.Faker("sentence", nb_words=10, locale="ru_RU")

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        """Метод для проверки полей: qualification и notes."""
        qualification = self.qualification
        notes = self.notes
        if create:
            self.qualification = check_len(qualification, 5, 3)
            self.notes = check_len(notes, 10, 7)

    @factory.post_generation
    def team(self, create, extracted, **kwargs):
        """Метод для создания связи со случайными командами."""
        if create:
            self.team.set([get_random_objects(Team)])


class NosologyFactory(factory.django.DjangoModelFactory):
    """Создание нозологий."""

    class Meta:
        model = Nosology
        skip_postgeneration_save = True

    name = factory.Faker("sentence", nb_words=5, locale="ru_RU")
    diagnosis = factory.RelatedFactoryList(
        "main.data_factories.factories.DiagnosisFactory",
        factory_related_name="nosology",
        size=lambda: random.randint(
            3,
            5,
        ),
    )

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        """Метод для провеки поля name."""
        field = self.name
        if create:
            self.name = check_len(field, 5, 3)


class DiagnosisFactory(factory.django.DjangoModelFactory):
    """
    Создание диагнозов, и связанных с ними нозологий.

    Колонка "name" является уникальной.
    """

    class Meta:
        model = Diagnosis
        django_get_or_create = ["name"]
        skip_postgeneration_save = True

    nosology = factory.SubFactory(NosologyFactory)
    name = factory.Faker("sentence", nb_words=5, locale="ru_RU")

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        """Метод для провеки поля name."""
        field = self.name
        if create:
            self.name = check_len(field, 5, 3)


class TeamFactory(factory.django.DjangoModelFactory):
    """
    Создание команд.

    Привязка к ним уже созданных городов, сотрудников(тренеров), кураторов,
    дисциплин. Колонка с названием команды является уникальной.
    """

    class Meta:
        model = Team
        django_get_or_create = ["name"]

    name = factory.Faker("sentence", nb_words=2, locale="ru_RU")
    city = factory.SubFactory(CityFactory)

    @factory.lazy_attribute
    def discipline_name(self):
        """Получить случайный набор дисциплин."""
        return get_random_objects(DisciplineName)

    @factory.lazy_attribute
    def curator(self):
        """Получить случайный набор кураторов."""
        return get_random_objects(User)


class CompetitionFactory(factory.django.DjangoModelFactory):
    """
    Создание соревнований.

    Привязка к ним уже созданных городов, команд создание локации,
    времени начала и окончания, активно или закончено.
    """

    class Meta:
        model = Competition
        skip_postgeneration_save = True
        django_get_or_create = ["title"]

    title = factory.Faker("sentence", nb_words=2, locale="ru_RU")
    city = factory.SubFactory(CityFactory)
    date_start = date.today() + timedelta(days=random.randrange(5, 30, 5))
    date_end = date_start + timedelta(days=random.randrange(2, 10, 2))
    location = factory.Faker("sentence", nb_words=4, locale="ru_RU")

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        """Добавляет команды к объекту соревнования."""
        if create:
            teams = Team.objects.all()
            list_teams = random.choices(teams, k=8)
            for team in list_teams:
                self.teams.add(team)

    @factory.post_generation
    def disciplines(self, create, extracted, **kwargs):
        """Добавляет дисциплины к объекту соревнования."""
        if create:
            disciplines = DisciplineName.objects.all()
            list_disciplines = random.choices(disciplines, k=4)
            for discipline in list_disciplines:
                self.disciplines.add(discipline)


class PlayerFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания игрока."""

    class Meta:
        model = Player
        django_get_or_create = ["birthday"]
        skip_postgeneration_save = True

    surname = factory.Faker("last_name", locale="ru_RU")
    name = factory.Faker("first_name", locale="ru_RU")
    patronymic = factory.Faker("middle_name", locale="ru_RU")
    birthday = factory.Faker("date_of_birth", minimum_age=12, maximum_age=18)
    addition_date = factory.Faker(
        "date_time_this_decade",
        before_now=True,
        after_now=False,
    )
    gender = factory.LazyFunction(lambda: random.choice(GENDER_CHOICES)[1])
    level_revision = factory.Faker("sentence", nb_words=1, locale="ru_RU")
    position = factory.LazyFunction(
        lambda: random.choice(PLAYER_POSITION_CHOICES)[1],
    )
    number = factory.Faker("random_number", digits=2)
    identity_document = factory.LazyFunction(
        lambda: random.choice(["паспорт", "свидетельство"]),
    )

    @factory.lazy_attribute
    def diagnosis(self):
        """Получить случайный набор диагнозов."""
        return get_random_objects(Diagnosis)

    @factory.lazy_attribute
    def discipline_name(self):
        """Получить случайный набор дисциплин."""
        return get_random_objects(DisciplineName)

    @factory.post_generation
    def team(self, create, extracted, **kwargs):
        """Добавляет команды к объекту игрока."""
        if create:
            teams_with_player_count = Team.objects.annotate(
                player_count=Count("team_players"),
            )
            if teams_with_player_count.filter(player_count__lt=10):
                self.team.set([get_random_objects(Team)])


class DocumentFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания документов."""

    class Meta:
        model = Document
        skip_postgeneration_save = True

    name = factory.LazyAttribute(
        lambda obj: f"{obj.player.surname}-{random.randint(1000, 9999)}",
    )

    @factory.lazy_attribute
    def player(self):
        """Получить случайный набор игроков."""
        return get_random_objects(PlayerFactory)

    @factory.post_generation
    def file(self, create, extracted, **kwargs):
        """Сохранить файл в документе."""
        if not create:
            return
        file_obj = BytesIO()
        image = Image.new(FORMAT_IMAGE, size=SIZE_IMAGE, color=COLOR_IMAGE)
        image.save(file_obj, EXT_IMAGE)
        file_obj.seek(0)
        self.file.save(f"{self.name}.png", File(file_obj))


class GameFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания игр."""

    class Meta:
        model = Game
        skip_postgeneration_save = True

    name = factory.Faker("sentence", locale="ru_RU")
    date = factory.LazyFunction(
        lambda: datetime.now(pytz.timezone("Europe/Moscow")),
    )
    video_link = factory.Faker("url")
    competition = factory.SubFactory(CompetitionFactory)


class GameDataPlayerFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания данных JSON игрока."""

    class Meta:
        model = GameDataPlayer

    player = factory.SubFactory(PlayerFactory)
    data = factory.LazyFunction(
        lambda: {
            "game_link": factory.Faker("url"),
            "player_number": random.randint(1, 99),
            "frames": [random.randint(5000, 10000) for _ in range(3)],
        },
    )
