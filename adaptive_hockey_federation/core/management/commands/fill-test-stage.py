import subprocess

from django.core.management.base import BaseCommand

base_commands = "python manage.py fill-test-db "
commands = (
    "--users",
    "--diagnosis --amount 8",
    "--discipline --amount 3",
    "--team --amount 20",
    "--staffteam",
    "--player --amount 300",
    "--document",
    "--competition --amount 10",
)


class Command(BaseCommand):

    help = "Наполнение базы данных тестовыми данными."

    def handle(self, *args, **options):
        for argument in commands:

            result = subprocess.run(
                base_commands + argument,
                shell=True,
                capture_output=True,
                text=True,
            )
            print(self.style.SUCCESS(result.stdout))
        return self.style.SUCCESS("Создание фикстур завершено!")
