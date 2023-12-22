from os import listdir
from os.path import isfile, join

from django.core.management.base import BaseCommand

from adaptive_hockey_federation.core.config.dev_settings import (
    FIXSTURES_DIR,
    FIXSTURES_FILE,
)
from adaptive_hockey_federation.parser.importing_db import (
    importing_parser_data_db,
    importing_test_data_db,
)


class Command(BaseCommand):
    help = "Запуск парсера офисных документов."

    def handle(self, *args, **options):
        """Загрузка распарсенных данных."""
        importing_parser_data_db(FIXSTURES_FILE)

        """Загрузка тестовых данных из файлов формата JSON."""
        file_names = [f for f in listdir(FIXSTURES_DIR)
                      if isfile(join(FIXSTURES_DIR, f))]
        for file_name in file_names:
            if 'main_' in file_name:
                try:
                    importing_test_data_db(FIXSTURES_DIR, file_name)
                except Exception as e:
                    print(f'Ошибка вставки тестовых данных {e} -> {file_name}')
