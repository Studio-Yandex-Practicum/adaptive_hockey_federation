import factory
from faker import Faker
from main.models import City, Diagnosis, Nosology, StaffMember, StaffTeamMember

from .constants import DIAGNOSIS_WORDS, NOSOLOGY_WORDS, STAFF_TEAM_MEMBER
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
