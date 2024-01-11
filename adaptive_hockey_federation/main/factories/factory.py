import random

import factory
# from faker import Faker
from main.models import (
    City,
    Diagnosis,
    Discipline,
    DisciplineLevel,
    DisciplineName,
    Nosology,
    StaffMember,
    StaffTeamMember,
    Team,
)
from users.factories import UserFactory

from .utils import check_len

# faker = Faker()


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

    name = factory.Faker('sentence', nb_words=5, locale='ru_RU')

    diagnosis = factory.RelatedFactoryList(
        'main.factories.factory.DiagnosisFactory',
        factory_related_name='nosology',
        size=lambda: random.randint(3, 5,)
    )

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        field = self.name
        if create:
            self.name = check_len(field, 5, 3)


class DiagnosisFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Diagnosis

    nosology = factory.SubFactory(NosologyFactory)
    name = factory.Faker('sentence', nb_words=5, locale='ru_RU')

    @factory.post_generation
    def check_field(self, create, extracted, **kwargs):
        field = self.name
        if create:
            self.name = check_len(field, 5, 3)


class StaffTeamMemberFactory(factory.django.DjangoModelFactory):

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


class DisciplineNameFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = DisciplineName

    name = factory.Faker('sentence', nb_words=2, locale='ru_RU')
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


class TeamFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Team

    name = factory.Faker('sentence', nb_words=1, locale='ru_RU')
    city = factory.SubFactory(CityFactory)
    staff_team_member = factory.SubFactory(StaffTeamMemberFactory)
    discipline_name = factory.SubFactory(DisciplineNameFactory)
    curator = factory.SubFactory(UserFactory)
