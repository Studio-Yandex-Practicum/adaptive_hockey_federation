from django.core.management.base import BaseCommand

from adaptive_hockey_federation.core.config.dev_settings import FIXSTURES_FILE
from adaptive_hockey_federation.parser.importing_db import (
    importing_parser_data_db,
)


class Command(BaseCommand):
    help = "Запуск парсера офисных документов."

    def handle(self, *args, **options):
        """Загрузка распарсенных данных."""
        importing_parser_data_db(FIXSTURES_FILE)
