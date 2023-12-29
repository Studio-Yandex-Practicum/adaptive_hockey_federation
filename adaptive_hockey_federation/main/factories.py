from random import randint

import factory
from faker import Faker

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

    name = factory.Faker('sentence', nb_words=randint(3, 5), locale='ru_RU')


class DiagnosisFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Diagnosis

    nosology = factory.SubFactory(NosologyFactory)
    name = factory.Faker('sentence', nb_words=randint(3, 5), locale='ru_RU')
