import json
import subprocess

from main.models import (
    City,
    DisciplineLevel,
    DisciplineName,
    Nosology,
    Player,
    Team,
)

from adaptive_hockey_federation.core.config.base_settings import RESOURSES_ROOT
from adaptive_hockey_federation.parser.user_card import BaseUserInfo

FILE_MODEL_MAP = {
    'main_nosology': Nosology,
    'main_city': City,
    'main_disciplinename': DisciplineName,
    'main_disciplinelevel': DisciplineLevel,
    'main_team': Team
}


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


def importing_test_data_db(FIXSTURES_DIR: str, file_name: str) -> None:
    file = open(FIXSTURES_DIR / file_name)
    data = json.load(file)
    key = file_name.replace('.json', '')
    models_name = FILE_MODEL_MAP[key]
    for item in data:
        try:
            if key == 'main_team':
                model_ins = models_name(
                    id=item['id'],
                    name=item['name'],
                    city_id=item['city_id'],
                    discipline_name_id=item['discipline_name_id'],
                    staff_team_member_id=1,
                    curator_id=1
                )
                model_ins.save()
            else:
                model_ins = models_name(
                    id=item['id'],
                    name=item['name']
                )
                model_ins.save()
        except Exception as e:
            print(f'Ошибка вставки данных {e} -> {item}')
    print(f'Импорт тестовых данных в {key} успешно выполнился.')
