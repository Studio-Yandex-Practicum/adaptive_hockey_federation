import json
import subprocess

from core.config.base_settings import (  # type: ignore
    FIXSTURES_DIR,
    RESOURSES_ROOT,
)
from django.core.management.base import BaseCommand
from main.models import Player


class Command(BaseCommand):
    help = "Запуск парсера офисных документов."

    def handle(self, *args, **options):
        subprocess.getoutput(
            f'poetry run parser -r -p {RESOURSES_ROOT}'
        )

        data = json.load(open(FIXSTURES_DIR / 'data.json'))
        for item in data:
            for key in item:
                if item[key] is None and key != 'player_number':
                    item[key] = ''
                if item[key] is None and key == 'player_number':
                    item[key] = 0
            try:
                player_model = Player(
                    surname=item['surname'],
                    name=item['name'],
                    patronymic=item['patronymic'],
                    birthday=item['date_of_birth'].replace(' 00:00:00', ''),
                    gender='',
                    level_revision=item['revision'],
                    position=item['position'],
                    number=item['player_number'],
                    is_captain=item['is_captain'],
                    is_assistent=item['is_assistant'],
                    identity_document=item['passport']
                )
                player_model.save()
            except Exception as e:
                print(f'Ошибка вставки данных {e} -> {item}')
