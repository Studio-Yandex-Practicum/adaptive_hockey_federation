import factory
from faker import Faker

from .dev_utils import check_len_name
from .models import City, Diagnosis, Nosology, StaffMember

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

    name = factory.Faker('sentence', nb_words=5, locale='ru_RU')

    @factory.post_generation
    def check_name(self, create, extracted, **kwargs):
        if create:
            check_len_name(self)


class DiagnosisFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Diagnosis

    nosology = factory.SubFactory(NosologyFactory)
    name = factory.Faker('sentence', nb_words=5, locale='ru_RU')

    @factory.post_generation
    def check_name(self, create, extracted, **kwargs):
        if create:
            check_len_name(self)
