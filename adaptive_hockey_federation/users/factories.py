import factory  # type: ignore
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from faker import Faker
from users.provaders import CustomPhoneProvider

fake = Faker(locale="ru_RU")
fake.add_provider(CustomPhoneProvider)
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика создания тестовых юзеров."""

    class Meta:
        model = User
        skip_postgeneration_save = True

    first_name = factory.Faker("first_name", locale="ru_RU")
    last_name = factory.Faker("last_name", locale="ru_RU")
    patronymic = factory.Faker("first_name", locale="ru_RU")
    email = factory.Faker("email", locale="ru_RU")
    phone = factory.LazyAttribute(lambda _: fake.phone_number())

    @factory.lazy_attribute
    def password(self):
        """Метод для создания пароля."""
        return make_password("pass1234")

    @factory.post_generation
    def admin_create(self, create, extracted, **kwargs):
        """Метод для присваивания роли админа или модератора."""
        if create:
            if self.role in ["admin", "moderator"]:
                self.is_staff = True
                if self.role == "admin":
                    self.is_superuser = True
