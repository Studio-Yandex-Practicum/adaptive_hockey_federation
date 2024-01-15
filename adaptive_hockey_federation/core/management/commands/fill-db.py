from django.conf import settings
from django.core.management.base import BaseCommand

from adaptive_hockey_federation.core.config.dev_settings import FILE_MODEL_MAP
from adaptive_hockey_federation.parser.importing_db import (
    clear_data_db,
    importing_parser_data_db,
    importing_real_data_db,
)

DB_MESSAGE = 'Данные успешно добавлены!'


class Command(BaseCommand):
    help = ("Запуск парсера офисных документов, и запись их в БД.")

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--parser',
            action='store_true',
            help='Запуск парсера документов',
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
        if fixtures:
            self.load_real_data()
        if parser:
            self.load_data()
        self.stdout.write(self.style.SUCCESS(DB_MESSAGE))
