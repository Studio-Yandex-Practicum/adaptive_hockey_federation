import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand
from main.factories import CityFactory, StaffMemberFactory


class Command(BaseCommand):
    help = ("Запуск парсера офисных документов, и запись их в БД."
            "А также создание рандомных фикстур для моделей проекта.")

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--parser',
            action='store_true',
            help='Запуск парсера документов',
        )
        parser.add_argument(
            '-c',
            '--city',
            action='store_true',
            help='Фикстуры для таблицы City'
        )
        parser.add_argument(
            '-s',
            '--staff',
            action='store_true',
            help='Фикстуры для таблицы StaffMember'
        )
        parser.add_argument(
            '-a',
            '--amount',
            type=int,
            default=10,
            help='Количество фикстур для создания')

    def handle(self, *args, **options):
        parser = options.get('parser')
        city = options.get('city', False)
        staff_member = options.get('staff', False)
        amount = options.get('amount')
        if city:
            CityFactory.create_batch(amount)
            return f'{amount} фикстур для таблицы City создано!'
        if staff_member:
            StaffMemberFactory.create_batch(amount)
            return f'{amount} фикстур для таблицы StaffMemmber создано!'
        if parser:
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
