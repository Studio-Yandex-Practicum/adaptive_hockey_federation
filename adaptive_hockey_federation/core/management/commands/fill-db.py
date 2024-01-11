from core.constants import ROLE_ADMIN, ROLE_AGENT, ROLE_MODERATOR
from django.conf import settings
from django.core.management.base import BaseCommand
from main.factories import CityFactory, StaffMemberFactory
from users.factories import UserFactory

from adaptive_hockey_federation.core.config.dev_settings import FILE_MODEL_MAP
from adaptive_hockey_federation.parser.importing_db import (
    clear_data_db,
    importing_parser_data_db,
    importing_real_data_db,
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
            help='Количество фикстур для создания'
        )
        parser.add_argument(
            '-f',
            '--fixtures',
            action='store_true',
            help='Фикстуры с реальными данными для таблиц.',
        )

    def load_data(self):
        """Загрузка распарсенных данных."""
        importing_parser_data_db(settings.FIXSTURES_FILE)

    def load_real_data(self):
        """Загрузка реальных данных из JSON."""
        for key in FILE_MODEL_MAP.items():
            file_name = key[0] + '.json'
            if 'main_' in key[0]:
                try:
                    clear_data_db(file_name)
                except Exception as e:
                    print(f'Ошибка удаления данных {e} -> '
                          f'{file_name}')
        items = list(FILE_MODEL_MAP.items())
        items.reverse()
        for key in items:
            file_name = key[0] + '.json'
            if 'main_' in key[0]:
                try:
                    importing_real_data_db(
                        settings.FIXSTURES_DIR,
                        file_name
                    )
                except Exception as e:
                    print(f'Ошибка вставки данных {e} -> '
                          f'{file_name}')

        return 'Фикстуры с реальными данными вставлены в таблицы!'

    def handle(self, *args, **options):
        """Запись данных в БД."""
        parser = options.get('parser')
        fixtures = options.get('fixtures')
        city = options.get('city', False)
        staff_member = options.get('staff', False)
        test_users = options.get('users', False)
        amount = options.get('amount')
        if fixtures:
            self.load_real_data()
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
