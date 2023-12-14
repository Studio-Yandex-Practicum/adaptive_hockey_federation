import os
import subprocess

from django.core.management.base import BaseCommand

from adaptive_hockey_federation.settings import BASE_DIR

RESOURSES_ROOT = os.path.join(BASE_DIR, 'resourses')
PARSER_MAIN = os.path.join(BASE_DIR, 'parser/parser.py')


class Command(BaseCommand):
    help = "Описание команды"

    def handle(self, *args, **options):
        run_parser = subprocess.getoutput(
            f'poetry run python {PARSER_MAIN} -r -p {RESOURSES_ROOT}'
        )
        with open(
            f'{RESOURSES_ROOT}/result.txt',
            'w',
            encoding='utf-8',
        ) as file:
            print(run_parser)
            file.write(run_parser)
