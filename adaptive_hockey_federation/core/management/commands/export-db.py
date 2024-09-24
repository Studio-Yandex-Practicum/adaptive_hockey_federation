from django.core.management import call_command
from django.core.management.base import BaseCommand

from adaptive_hockey_federation.core.config.dev_settings import DB_DUMP_FILE


class Command(BaseCommand):
    """Класс экспорта данных из БД."""

    help = "Экспорт данных из базы данных в JSON-файл"

    def handle(self, *args, **options):
        """Экспортирует данные из БД."""
        try:
            call_command(
                "dumpdata",
                exclude=["contenttypes", "auth.permission"],
                natural_foreign=True,
                natural_primary=True,
                indent=2,
                output=DB_DUMP_FILE,
            )

            return self.stdout.write(
                self.style.SUCCESS(
                    f"База данных экспортирована в {DB_DUMP_FILE}",
                ),
            )
        except Exception as e:
            return self.stdout.write(
                self.style.ERROR(f"Ошибка при экспорте данных: {str(e)}"),
            )
