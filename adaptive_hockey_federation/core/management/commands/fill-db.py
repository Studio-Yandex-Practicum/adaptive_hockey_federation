import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Запуск парсера офисных документов."

    def handle(self, *args, **options):
        run_parser = subprocess.getoutput(
            f'poetry run parser -r -p {settings.RESOURSES_ROOT}'
        )
        with open(
            f'{settings.RESOURSES_ROOT}/result.txt',
            'w',
            encoding='utf-8',
        ) as file:
            print(run_parser)
            file.write(run_parser)
