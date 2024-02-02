import random

import factory
from django.db.models import Count
from main.models import (
    GENDER_CHOICES,
    PLAYER_POSITION_CHOICES,
    City,
    Diagnosis,
    Discipline,
    DisciplineLevel,
    DisciplineName,
    Nosology,
    Player,
    StaffMember,
    StaffTeamMember,
    Team,
)
from users.models import User

from .utils import check_len, get_random_objects


class CityFactory(factory.django.DjangoModelFactory):
    """Создания данных городов. Название города является уникальным."""

    class Meta():
        model = City
        django_get_or_create = ['name']

    name = factory.Faker('city', locale='ru_RU')


class StaffMemberFactory(factory.django.DjangoModelFactory):
    """Создание сотрудников команд."""

    class Meta():
        model = StaffMember

    surname = factory.Faker('last_name', locale='ru_RU')
    name = factory.Faker('first_name', locale='ru_RU')
    patronymic = factory.Faker('middle_name', locale='ru_RU')
    phone = factory.Faker('phone_number', locale='ru_RU')


class StaffTeamMemberFactory(factory.django.DjangoModelFactory):
    """
    Создание данных о сотрудниках привязаных к командам. Квалификация
    может быть "Тренер" и "Другие сотрудники".
    """

    class Meta:
        model = StaffTeamMember

    staff_member = factory.SubFactory(StaffMemberFactory)
    qualification = factory.Faker('sentence', nb_words=5, locale='ru_RU',)
    notes = factory.Faker('sentence', nb_words=10, locale='ru_RU')

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        qualification = self.qualification
        notes = self.notes
        if create:
            self.qualification = check_len(qualification, 5, 3)
            self.notes = check_len(notes, 10, 7)


class NosologyFactory(factory.django.DjangoModelFactory):
    """Создание нозологий."""

    class Meta:
        model = Nosology

    name = factory.Faker('sentence', nb_words=5, locale='ru_RU')
    diagnosis = factory.RelatedFactoryList(
        'main.data_factories.factories.DiagnosisFactory',
        factory_related_name='nosology',
        size=lambda: random.randint(3, 5,)
    )

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        field = self.name
        if create:
            self.name = check_len(field, 5, 3)


class DiagnosisFactory(factory.django.DjangoModelFactory):
    """
    Cозданиt диагнозов, и связанных с ними нозологий.  Колонка "name"
    является уникальной.
    """

    class Meta:
        model = Diagnosis
        django_get_or_create = ['name']

    nosology = factory.SubFactory(NosologyFactory)
    name = factory.Faker('sentence', nb_words=5, locale='ru_RU')

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        field = self.name
        if create:
            self.name = check_len(field, 5, 3)


class DisciplineNameFactory(factory.django.DjangoModelFactory):
    """Cоздание адаптивных дисциплин. Колонка "name" является уникальной."""

    class Meta:
        model = DisciplineName
        django_get_or_create = ['name']

    name = factory.Faker('sentence', nb_words=2, locale='ru_RU')
    discipline = factory.RelatedFactoryList(
        'main.data_factories.factories.DisciplineFactory',
        factory_related_name='discipline_name',
        size=5,
    )


class DisciplineLevelFactory(factory.django.DjangoModelFactory):
    """
    Создание уровней для адаптивных дисциплин. Колонка "name"
    является уникальной.
    """

    class Meta:
        model = DisciplineLevel
        django_get_or_create = ['name']

    name = factory.Iterator(['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])


class DisciplineFactory(factory.django.DjangoModelFactory):
    """Привязка адаптивных дисциплин к определёным уровням."""

    class Meta:
        model = Discipline

    discipline_name = factory.SubFactory(DisciplineNameFactory)
    discipline_level = factory.SubFactory(DisciplineLevelFactory)


class TeamFactory(factory.django.DjangoModelFactory):
    """
    Создание команд. Привязка к ним уже созданных городов,
    сотрудников(тренеров), кураторов, дисциплин. Колонка
    с названием команды является уникальной.
    """

    class Meta:
        model = Team
        django_get_or_create = ['name']

    name = factory.Faker('sentence', nb_words=2, locale='ru_RU')
    city = factory.SubFactory(CityFactory)

    # @factory.lazy_attribute
    # def staff_team_member(self):
    #     return get_random_objects(StaffTeamMember)

    @factory.lazy_attribute
    def discipline_name(self):
        return get_random_objects(DisciplineName)

    @factory.lazy_attribute
    def curator(self):
        return get_random_objects(User)


class PlayerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Player
        django_get_or_create = ['birthday']

    surname = factory.Faker('last_name', locale='ru_RU')
    name = factory.Faker('first_name', locale='ru_RU')
    patronymic = factory.Faker('middle_name', locale='ru_RU')
    birthday = factory.Faker('date_of_birth', minimum_age=12, maximum_age=18)
    gender = factory.LazyFunction(lambda: random.choice(GENDER_CHOICES)[1])
    level_revision = factory.Faker('sentence', nb_words=1, locale='ru_RU')
    position = factory.LazyFunction(
        lambda: random.choice(PLAYER_POSITION_CHOICES)[1]
    )
    number = factory.Faker('random_number', digits=2)
    identity_document = factory.LazyFunction(
        lambda: random.choice(['паспорт', 'свидетельство'])
    )

    @factory.lazy_attribute
    def diagnosis(self):
        return get_random_objects(Diagnosis)

    @factory.post_generation
    def team(self, create, extracted, **kwargs):
        if create:
            teams_with_player_count = Team.objects.annotate(
                player_count=Count('team_players')
            )
            if teams_with_player_count.filter(player_count__lt=10):
                self.team.set([get_random_objects(Team)])
