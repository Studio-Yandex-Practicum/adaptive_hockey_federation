import factory  # type: ignore
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика создания тестовых юзеров"""
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    patronymic = factory.Faker('first_name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    password = '123456789'
