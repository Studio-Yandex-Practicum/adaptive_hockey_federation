import json
import os

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

from adaptive_hockey_federation.core.config.dev_settings import DB_DUMP_FILE


class Command(BaseCommand):
    """Класс импорта данных в БД."""

    help = "Импорт данных из JSON-файла в базу данных"

    def handle(self, *args, **options):
        """Импортирует данные в БД."""
        if not os.path.exists(DB_DUMP_FILE):
            return self.stdout.write(
                self.style.ERROR(f"Файл {DB_DUMP_FILE} не найден"),
            )

        with open(DB_DUMP_FILE, "r") as f:
            data = json.load(f)
        models_to_clear = set(item["model"] for item in data)

        # Очистка таблиц, в которые импортируются данные,
        # для исключения ошибки unique constraint
        with connection.cursor() as cursor:
            for model_name in models_to_clear:
                try:
                    app_label, model = model_name.split(".")
                    model_class = apps.get_model(app_label, model)
                    table_name = model_class._meta.db_table
                    cursor.execute(f"TRUNCATE TABLE {table_name} CASCADE")
                except Exception as e:
                    return self.stdout.write(
                        self.style.WARNING(
                            f"Не удалось очистить таблицу для модели {model_name}: {str(e)}",  # noqa: E501
                        ),
                    )

        try:
            call_command("loaddata", DB_DUMP_FILE)
            return self.stdout.write(
                self.style.SUCCESS(
                    f"Данные из {DB_DUMP_FILE} импортированы в базу данных",
                ),
            )
        except Exception as e:
            return self.stdout.write(
                self.style.ERROR(f"Ошибка при импорте данных: {str(e)}"),
            )
