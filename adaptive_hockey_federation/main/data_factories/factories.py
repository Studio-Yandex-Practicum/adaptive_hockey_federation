import random
from datetime import date, timedelta
from io import BytesIO

import factory
from competitions.models import Competition
from core.constants import DISCIPLINES
from django.core.files.base import File
from django.db.models import Count
from main.models import (
    GENDER_CHOICES,
    PLAYER_POSITION_CHOICES,
    City,
    Diagnosis,
    DisciplineLevel,
    DisciplineName,
    Document,
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
    Создание данных о сотрудниках привязаных к командам. Квалификация
    может быть "Тренер" и "Другие сотрудники".
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
        qualification = self.qualification
        notes = self.notes
        if create:
            self.qualification = check_len(qualification, 5, 3)
            self.notes = check_len(notes, 10, 7)

    @factory.post_generation
    def team(self, create, extracted, **kwargs):
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
        field = self.name
        if create:
            self.name = check_len(field, 5, 3)


class DiagnosisFactory(factory.django.DjangoModelFactory):
    """
    Создание диагнозов, и связанных с ними нозологий.  Колонка "name"
    является уникальной.
    """

    class Meta:
        model = Diagnosis
        django_get_or_create = ["name"]
        skip_postgeneration_save = True

    nosology = factory.SubFactory(NosologyFactory)
    name = factory.Faker("sentence", nb_words=5, locale="ru_RU")

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        field = self.name
        if create:
            self.name = check_len(field, 5, 3)


class DisciplineLevelFactory(factory.django.DjangoModelFactory):
    """
    Создание уровней для адаптивных дисциплин. Колонка "name"
    является уникальной.
    """

    class Meta:
        model = DisciplineLevel
        django_get_or_create = ["name"]

    name = factory.Iterator(["A1", "A2", "B1", "B2", "C1", "C2"])


class TeamFactory(factory.django.DjangoModelFactory):
    """
    Создание команд. Привязка к ним уже созданных городов,
    сотрудников(тренеров), кураторов, дисциплин. Колонка
    с названием команды является уникальной.
    """

    class Meta:
        model = Team
        django_get_or_create = ["name"]

    name = factory.Faker("sentence", nb_words=2, locale="ru_RU")
    city = factory.SubFactory(CityFactory)

    @factory.lazy_attribute
    def discipline_name(self):
        return get_random_objects(DisciplineName)

    @factory.lazy_attribute
    def curator(self):
        return get_random_objects(User)


class CompetitionFactory(factory.django.DjangoModelFactory):
    """
    Создание соревнований. Привязка к ним уже созданных городов, команд
    создание локации, времени начала и окончания, активно или закончено
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
    is_active = factory.LazyFunction(lambda: random.choice([True, False]))

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if create:
            teams = Team.objects.all()
            list_teams = random.choices(teams, k=8)
            for team in list_teams:
                self.teams.add(team)


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player
        django_get_or_create = ["birthday"]
        skip_postgeneration_save = True

    surname = factory.Faker("last_name", locale="ru_RU")
    name = factory.Faker("first_name", locale="ru_RU")
    patronymic = factory.Faker("middle_name", locale="ru_RU")
    birthday = factory.Faker("date_of_birth", minimum_age=12, maximum_age=18)
    addition_date = factory.Faker(
        "date_time_this_decade", before_now=True, after_now=False
    )
    gender = factory.LazyFunction(lambda: random.choice(GENDER_CHOICES)[1])
    discipline_name = factory.LazyFunction(
        lambda: random.choice(DISCIPLINES)[1]
    )
    level_revision = factory.Faker("sentence", nb_words=1, locale="ru_RU")
    position = factory.LazyFunction(
        lambda: random.choice(PLAYER_POSITION_CHOICES)[1]
    )
    number = factory.Faker("random_number", digits=2)
    identity_document = factory.LazyFunction(
        lambda: random.choice(["паспорт", "свидетельство"])
    )

    @factory.lazy_attribute
    def diagnosis(self):
        return get_random_objects(Diagnosis)

    @factory.post_generation
    def team(self, create, extracted, **kwargs):
        if create:
            teams_with_player_count = Team.objects.annotate(
                player_count=Count("team_players")
            )
            if teams_with_player_count.filter(player_count__lt=10):
                self.team.set([get_random_objects(Team)])


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document
        skip_postgeneration_save = True

    name = factory.LazyAttribute(
        lambda obj: f"{obj.player.surname}-{random.randint(1000, 9999)}"
    )

    @factory.lazy_attribute
    def player(self):
        return get_random_objects(PlayerFactory)

    @factory.post_generation
    def file(self, create, extracted, **kwargs):
        if not create:
            return
        file_obj = BytesIO()
        image = Image.new(FORMAT_IMAGE, size=SIZE_IMAGE, color=COLOR_IMAGE)
        image.save(file_obj, EXT_IMAGE)
        file_obj.seek(0)
        self.file.save(f"{self.name}.png", File(file_obj))
