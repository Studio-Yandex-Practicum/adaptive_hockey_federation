import json
import subprocess

from main.models import (
    City,
    Discipline,
    DisciplineLevel,
    DisciplineName,
    Nosology,
    Player,
    StaffMember,
    StaffTeamMember,
    Team,
)

from adaptive_hockey_federation.core.config.dev_settings import RESOURSES_ROOT
from adaptive_hockey_federation.parser.user_card import BaseUserInfo

FILE_MODEL_MAP = {
    'main_nosology': Nosology,
    'main_city': City,
    'main_disciplinename': DisciplineName,
    'main_disciplinelevel': DisciplineLevel,
    'main_discipline': Discipline,
    'main_team': Team
}

POSITIONS = ('нападающий', 'поплавок', 'вратарь', 'защитник')


def parse_file(file_path: str) -> list[BaseUserInfo]:
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data


def get_discipline(item_name: str) -> int:
    try:
        discipline_level_id = DisciplineLevel.objects.get(
            name=item_name
        )
        discipline = Discipline.objects.get(
            discipline_level_id=discipline_level_id
        )
    except DisciplineLevel.DoesNotExist:
        discipline = None
    return discipline


def create_staff_member(item) -> None:
    try:
        staff_member_model = StaffMember(
            surname=item['surname'],
            name=item['name'],
            patronymic=item['patronymic'],
        )
        staff_member_model.save()
        staff_team_member_model = StaffTeamMember(
            staff_position=item['position'],
            staff_member_id=staff_member_model.id)
        staff_team_member_model.save()

    except Exception as e:
        print(f'Ошибка вставки данных {e} -> {item}')


def importing_parser_data_db(FIXSTURES_FILE: str) -> None:
    subprocess.getoutput(f'poetry run parser -r -p {RESOURSES_ROOT}')
    data = parse_file(FIXSTURES_FILE)
    for item in data:
        for key in item:
            if item[key] is None and key != 'player_number':
                item[key] = ''
            if item[key] is None and key == 'player_number':
                item[key] = 0
            if key == 'classification':
                discipline = get_discipline(item['classification'])
            if key == 'position' and item[key] not in POSITIONS:
                create_staff_member(item)
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
                identity_document=item['passport'],
                discipline=discipline
            )
            player_model.save()
        except Exception as e:
            print(f'Ошибка вставки данных {e} -> {item}')


def importing_real_data_db(FIXSTURES_DIR: str, file_name: str) -> None:
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
            if key == 'main_discipline':
                model_ins = models_name(
                    id=item['id'],
                    discipline_level_id=item['discipline_level_id'],
                    discipline_name_id=item['discipline_name_id']
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
