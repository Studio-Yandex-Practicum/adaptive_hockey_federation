import random

import factory
from faker import Faker
from main.models import (
    City,
    Diagnosis,
    Discipline,
    DisciplineLevel,
    DisciplineName,
    Nosology,
    StaffMember,
    StaffTeamMember,
)

from .constants import (
    DIAGNOSIS_WORDS,
    DISCIPLINE_NAME,
    NOSOLOGY_DIAGNOSIS,
    NOSOLOGY_WORDS,
    STAFF_TEAM_MEMBER,
)
from .utils import check_len

faker = Faker()


class CityFactory(factory.django.DjangoModelFactory):

    class Meta():
        model = City

    name = factory.Faker('city', locale='ru_RU')


class StaffMemberFactory(factory.django.DjangoModelFactory):

    class Meta():
        model = StaffMember

    surname = factory.Faker('last_name', locale='ru_RU')
    name = factory.Faker('first_name', locale='ru_RU')
    patronymic = factory.Faker('middle_name', locale='ru_RU')
    phone = factory.Faker('phone_number', locale='ru_RU')


class NosologyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Nosology

    name = factory.Faker(
        'sentence',
        nb_words=NOSOLOGY_WORDS['max'],
        locale='ru_RU',
    )

    diagnosis = factory.RelatedFactoryList(
        'main.factories.factory.DiagnosisFactory',
        factory_related_name='nosology',
        size=lambda: random.randint(
            NOSOLOGY_DIAGNOSIS['min'],
            NOSOLOGY_DIAGNOSIS['max'],
        )
    )

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        field = self.name
        if create:
            self.name = check_len(
                field,
                NOSOLOGY_WORDS['max'],
                NOSOLOGY_WORDS['min'],
            )


class DiagnosisFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Diagnosis

    nosology = factory.SubFactory(NosologyFactory)
    name = factory.Faker(
        'sentence',
        nb_words=DIAGNOSIS_WORDS['max'],
        locale='ru_RU',
    )

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        field = self.name
        if create:
            self.name = check_len(
                field,
                DIAGNOSIS_WORDS['max'],
                DIAGNOSIS_WORDS['min'],
            )


class StaffTeamMemberFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = StaffTeamMember

    staff_member = factory.SubFactory(StaffMemberFactory)
    qualification = factory.Faker(
        'sentence',
        nb_words=STAFF_TEAM_MEMBER['qualification']['max'],
        locale='ru_RU',
    )
    notes = factory.Faker(
        'sentence',
        nb_words=STAFF_TEAM_MEMBER['notes']['max'],
        locale='ru_RU',
    )

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        qualification = self.qualification
        notes = self.notes
        if create:
            self.qualification = check_len(
                qualification,
                STAFF_TEAM_MEMBER['qualification']['max'],
                STAFF_TEAM_MEMBER['qualification']['min'],
            )
            self.notes = check_len(
                notes,
                STAFF_TEAM_MEMBER['notes']['max'],
                STAFF_TEAM_MEMBER['notes']['min'],
            )


class DisciplineNameFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = DisciplineName

    name = factory.Faker('sentence', nb_words=DISCIPLINE_NAME, locale='ru_RU')
    discipline = factory.RelatedFactoryList(
        'main.factories.factory.DisciplineFactory',
        factory_related_name='discipline_name',
        size=5,
    )


class DisciplineLevelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = DisciplineLevel
        django_get_or_create = ['name']

    name = factory.Iterator(['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])


class DisciplineFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Discipline

    discipline_name = factory.SubFactory(DisciplineNameFactory)
    discipline_level = factory.SubFactory(DisciplineLevelFactory)
