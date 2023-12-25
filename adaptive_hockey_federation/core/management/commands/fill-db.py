from core.constants import ROLE_ADMIN, ROLE_AGENT, ROLE_MODERATOR
from django.conf import settings
from django.core.management.base import BaseCommand
from users.factories import UserFactory

from adaptive_hockey_federation.parser.importing_db import (
    importing_parser_data_db,
)

ROLES = [ROLE_AGENT, ROLE_MODERATOR, ROLE_ADMIN]
TEST_USERS_AMOUNT = 3
DB_MESSAGE = 'Данные успешно добавлены!'


class Command(BaseCommand):
    help = "Запуск парсера офисных документов, и создание тестовых юзеров."

    def load_data(self):
        """Загрузка распарсенных данных."""
        importing_parser_data_db(settings.FIXSTURES_FILE)

    def create_test_users(self):
        """Cоздание тестовых юзеров."""
        for role in ROLES:
            UserFactory.create_batch(TEST_USERS_AMOUNT, role=role)

    def handle(self, *args, **options):
        """Запись данных в БД."""
        self.load_data()
        self.create_test_users()
        self.stdout.write(self.style.SUCCESS(DB_MESSAGE))
