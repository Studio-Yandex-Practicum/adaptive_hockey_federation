from core.constants import ROLE_ADMIN, ROLE_AGENT, ROLE_MODERATOR
from django.conf import settings
from django.core.management.base import BaseCommand
from main.factories import CityFactory, StaffMemberFactory
from users.factories import UserFactory

from adaptive_hockey_federation.parser.importing_db import (
    importing_parser_data_db,
)

ROLES = [ROLE_AGENT, ROLE_MODERATOR, ROLE_ADMIN]
TEST_USERS_AMOUNT = 3
DB_MESSAGE = 'Данные успешно добавлены!'


class Command(BaseCommand):
    help = ("Запуск парсера офисных документов, и запись их в БД."
            "А также создание рандомных фикстур для моделей проекта.")

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--parser',
            action='store_true',
            help='Запуск парсера документов',
        )
        parser.add_argument(
            '-c',
            '--city',
            action='store_true',
            help='Фикстуры для таблицы City'
        )
        parser.add_argument(
            '-s',
            '--staff',
            action='store_true',
            help='Фикстуры для таблицы StaffMember'
        )
        parser.add_argument(
            '-u',
            '--users',
            action='store_true',
            help='Фикстуры для таблицы Users'
        )
        parser.add_argument(
            '-a',
            '--amount',
            type=int,
            default=10,
            help='Количество фикстур для создания')

    def load_data(self):
        """Загрузка распарсенных данных."""
        importing_parser_data_db(settings.FIXSTURES_FILE)

    def handle(self, *args, **options):
        """Запись данных в БД."""

        parser = options.get('parser')
        city = options.get('city', False)
        staff_member = options.get('staff', False)
        test_users = options.get('users', False)
        amount = options.get('amount')
        if city:
            CityFactory.create_batch(amount)
            return f'{amount} фикстур для таблицы City создано!'
        if staff_member:
            StaffMemberFactory.create_batch(amount)
            return f'{amount} фикстур для таблицы StaffMemmber создано!'
        if parser:
            self.load_data()
        if test_users:
            for role in ROLES:
                UserFactory.create_batch(amount, role=role)
        self.stdout.write(self.style.SUCCESS(DB_MESSAGE))
