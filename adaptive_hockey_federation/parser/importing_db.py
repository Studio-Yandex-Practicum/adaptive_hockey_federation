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

PLAYER_POSITIONS = ['нападающий', 'поплавок', 'вратарь', 'защитник',
                    'Позиция записана неверно',]
STAFF_POSITIONS = ['тренер', 'координатор', 'пушер',]


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


# def get_team(item_name: str) -> int:
#     print(f'@@@{item_name}')
#     try:
#         teams = Team.objects.filter(
#             name=item_name
#         )
#     except Team.DoesNotExist:
#         teams = None
#     print(f'####{teams}')
#     for team in teams:
#         print(f'####{team}')
#         return team


def create_staff_member(item) -> None:
    try:
        try:
            staff_member = StaffMember(
                surname=item['surname'],
                name=item['name'],
                patronymic=item['patronymic']
            )
            staff_member.save()

            staff_team_member = StaffTeamMember(
                staff_position=item['position'],
                staff_member_id=staff_member.id,
                notes=item['date_of_birth'].replace(' 00:00:00', '')
            )

            staff_team_member.save()
            team = Team.objects.get(name=item['team'])
            staff_team_member_id = StaffTeamMember.objects.get(
                staff_position__contains='тренер',
                pk=staff_team_member.id
            )
            if (team.staff_team_member_id != staff_team_member_id):
                team.staff_team_member_id = staff_team_member_id
                team.save()
            return team
        except StaffTeamMember.DoesNotExist:
            team = None
    except Exception as e:
        print(f'Ошибка вставки данных {e} -> {item}')


def create_players(item, discipline: int) -> None:
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
            discipline=discipline,
            # team=team
        )
        player_model.save()
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
        for i in PLAYER_POSITIONS:
            if i in item['position']:
                create_players(
                    item,
                    get_discipline(item['classification']),
                    # get_team(item['team'])
                )
        for i in STAFF_POSITIONS:
            if i in item['position']:
                create_staff_member(item)


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
