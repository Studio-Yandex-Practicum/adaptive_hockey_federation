import subprocess

from core.constants import (
    DB_MESSAGE,
    ROLE_ADMIN,
    ROLE_AGENT,
    ROLE_MODERATOR,
    TEST_USERS_AMOUNT,
)
from django.conf import settings
from django.core.management.base import BaseCommand
from users.factories import UserFactory

ROLES = [ROLE_AGENT, ROLE_MODERATOR, ROLE_ADMIN]


class Command(BaseCommand):
    help = "Запуск парсера офисных документов, и создание тестовых юзеров."

    def run_parser(self):
        """Запуск парсера офисных документов."""
        run_parser = subprocess.getoutput(
            f'poetry run parser -r -p {settings.RESOURSES_ROOT}'
        )
        with open(
            f'{settings.RESOURSES_ROOT}/result.txt',
            'w',
            encoding='utf-8',
        ) as file:
            print(run_parser)
            file.write(run_parser)

    def create_test_users(self):
        """Cоздание тестовых юзеров."""
        for role in ROLES:
            UserFactory.create_batch(TEST_USERS_AMOUNT, role=role)

    def handle(self, *args, **options):
        """Запись данных в БД."""
        self.run_parser()
        self.create_test_users()
        self.stdout.write(self.style.SUCCESS(DB_MESSAGE))
