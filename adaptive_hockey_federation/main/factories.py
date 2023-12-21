import factory
from faker import Faker

from .models import City, StaffMember

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
