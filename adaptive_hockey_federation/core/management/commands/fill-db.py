from django.conf import settings
from django.core.management.base import BaseCommand

from adaptive_hockey_federation.parser.importing_db import (
    importing_parser_data_db,
)

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

    def load_data(self):
        """Загрузка распарсенных данных."""
        importing_parser_data_db(settings.FIXSTURES_FILE)

    def handle(self, *args, **options):
        """Запись данных в БД."""
        parser = options.get('parser')
        if parser:
            self.load_data()
        self.stdout.write(self.style.SUCCESS(DB_MESSAGE))
