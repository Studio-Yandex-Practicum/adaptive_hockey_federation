from django.core.management.base import BaseCommand

from adaptive_hockey_federation.core.config.dev_settings import (
    FILE_MODEL_MAP,
    FIXSTURES_DIR,
    FIXSTURES_FILE,
)
from adaptive_hockey_federation.parser.importing_db import (
    clear_data_db,
    importing_parser_data_db,
    importing_real_data_db,
)

DB_MESSAGE = "Данные успешно добавлены!"


class Command(BaseCommand):
    """Класс для парсинга данных и их записи в БД."""

    help = "Запуск парсера офисных документов, и запись их в БД."

    def add_arguments(self, parser):
        """Добавляет новые аргументы для командной строки."""
        parser.add_argument(
            "-p",
            "--parser",
            action="store_true",
            help="Запуск парсера документов",
        )
        parser.add_argument(
            "-f",
            "--fixtures",
            action="store_true",
            help="Фикстуры с реальными данными для таблиц.",
        )

    def load_data(self) -> None:
        """Загрузка распарсенных данных."""
        importing_parser_data_db(FIXSTURES_FILE)
        return None

    def load_real_data(self) -> None:
        """Загрузка реальных данных из JSON."""
        for key in FILE_MODEL_MAP.items():
            file_name = key[0] + ".json"
            if "main_" in key[0]:
                try:
                    clear_data_db(file_name)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Ошибка удаления данных {e} -> " f"{file_name}",
                        ),
                    )
        items = list(FILE_MODEL_MAP.items())
        items.reverse()
        for key in items:
            file_name = key[0] + ".json"
            if "main_" in key[0]:
                try:
                    importing_real_data_db(FIXSTURES_DIR, file_name)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Фикстуры с файла {file_name} вставлены "
                            "в таблицы!",
                        ),
                    )
                except Exception as e:
                    return self.stdout.write(
                        self.style.ERROR_OUTPUT(
                            f"Ошибка вставки данных {e} -> " f"{file_name}",
                        ),
                    )
        return None

    def handle(self, *args, **options):
        """Запись данных в БД."""
        parser = options.get("parser")
        fixtures = options.get("fixtures")
        if fixtures:
            self.load_real_data()
        if parser:
            self.load_data()
