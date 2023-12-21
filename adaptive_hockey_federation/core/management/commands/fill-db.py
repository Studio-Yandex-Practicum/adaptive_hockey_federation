from parser.importing_db import importing_parser_data_db

from core.config.base_settings import FIXSTURES_FILE  # type: ignore
from django.core.management.base import BaseCommand  # type: ignore


class Command(BaseCommand):
    help = "Запуск парсера офисных документов."

    def handle(self, *args, **options):
        importing_parser_data_db(FIXSTURES_FILE)
