import subprocess

from django.core.management.base import BaseCommand

from adaptive_hockey_federation.settings import RESOURSES_ROOT


class Command(BaseCommand):
    help = "Запуск парсера офисных документов."

    def handle(self, *args, **options):
        run_parser = subprocess.getoutput(
            f'poetry run parser -r -p {RESOURSES_ROOT}'
        )
        with open(
            f'{RESOURSES_ROOT}/result.txt',
            'w',
            encoding='utf-8',
        ) as file:
            print(run_parser)
            file.write(run_parser)
