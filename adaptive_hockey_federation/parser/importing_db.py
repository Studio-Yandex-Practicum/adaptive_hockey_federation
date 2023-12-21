import json
import subprocess

from core.config.base_settings import RESOURSES_ROOT  # type: ignore
from main.models import Player

from adaptive_hockey_federation.parser.user_card import \
    BaseUserInfo  # type: ignore


def parse_file(file_path: str) -> list[BaseUserInfo]:
    file = open(file_path)
    data = json.load(file)
    return data


def importing_parser_data_db(FIXSTURES_FILE: str) -> None:
    subprocess.getoutput(f'poetry run parser -r -p {RESOURSES_ROOT}')
    data = parse_file(FIXSTURES_FILE)
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
