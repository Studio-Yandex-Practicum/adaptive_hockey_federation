import json
import sqlite3
import subprocess

from django.core.management.base import BaseCommand

from adaptive_hockey_federation.core.config.dev_settings import (
    BASE_DIR,
    FIXSTURES_DIR,
    RESOURSES_ROOT,
)


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

        conn = sqlite3.connect(BASE_DIR / 'db.sqlite3')
        cursor = conn.cursor()
        data = json.load(open(FIXSTURES_DIR / 'data.json'))
        for item in data:
            for key in item:
                if item[key] is None:
                    item[key] = ''
            try:
                cursor.execute('''
                    INSERT INTO main_player (
                            surname,
                            name,
                            patronymic,
                            birthday,
                            gender,
                            level_revision,
                            position,
                            number,
                            is_captain,
                            is_assistent,
                            identity_document
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['surname'],
                    item['name'],
                    item['patronymic'],
                    item['date_of_birth'],
                    '',
                    # gender,
                    item['revision'],
                    item['position'],
                    item['player_number'],
                    item['is_captain'],
                    item['is_assistant'],
                    item['passport']
                )
                )
            except Exception as e:
                print(e)
                print(item)
        conn.commit()
