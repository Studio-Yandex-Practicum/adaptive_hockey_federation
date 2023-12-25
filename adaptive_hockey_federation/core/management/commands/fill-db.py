from django.conf import settings
from django.core.management.base import BaseCommand

from adaptive_hockey_federation.parser.importing_db import (
    importing_parser_data_db,
)


class Command(BaseCommand):
    help = "Запуск парсера офисных документов."

    def handle(self, *args, **options):
        """Загрузка распарсенных данных."""
        importing_parser_data_db(settings.FIXSTURES_FILE)
