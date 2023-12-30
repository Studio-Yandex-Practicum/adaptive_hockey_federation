import json
import subprocess

from django.db import connection
from main import models
from main.models import (
    Discipline,
    DisciplineLevel,
    Player,
    StaffMember,
    StaffTeamMember,
    Team,
)

from adaptive_hockey_federation.core.config.dev_settings import (
    FILE_MODEL_MAP,
    RESOURSES_ROOT,
)
from adaptive_hockey_federation.parser.user_card import BaseUserInfo

MODELS_ONE_FIELD_NAME = ['main_city', 'main_disciplinename',
                         'main_disciplinelevel', 'main_nosology']

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
        )
        player_model.save()
        teams = Team.objects.get(name=item['team'])
        player_model.team.add(teams)

    except Exception as e:
        print(f'Ошибка вставки данных {e} -> {item}')

# flake8: noqa: C901
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
                    get_discipline(item['classification'])
                )
        for i in STAFF_POSITIONS:
            if i in item['position']:
                create_staff_member(item)


def clear_data_db(file_name: str) -> None:
    key = file_name.replace('.json', '')
    models_name = getattr(models, FILE_MODEL_MAP[key])
    models_name.objects.all().delete()
    cursor = connection.cursor()
    cursor.execute(f"SELECT setval(pg_get_serial_sequence('{key}', 'id'),"
                   f"coalesce(max(id), 1), max(id) IS NOT null)"
                   f"FROM {key};")


def importing_real_data_db(
        FIXSTURES_DIR: str, file_name: str) -> None:
    file = open(FIXSTURES_DIR / file_name)
    data = json.load(file)
    key = file_name.replace('.json', '')
    models_name = getattr(models, FILE_MODEL_MAP[key])
    for item in data:
        try:
            if key in MODELS_ONE_FIELD_NAME:
                model_ins = models_name(
                    id=item['id'],
                    name=item['name']
                )
                model_ins.save()
            if key == 'main_staffmember':
                model_ins = models_name(
                    id=item['id'],
                    surname=item['surname'],
                    name=item['name'],
                    patronymic=item['patronymic'],
                )
                model_ins.save()
            if key == 'main_discipline':
                model_ins = models_name(
                    id=item['id'],
                    discipline_level_id=item['discipline_level_id'],
                    discipline_name_id=item['discipline_name_id']
                )
                model_ins.save()
            if key == 'main_staffteammember':
                model_ins = models_name(
                    id=item['id'],
                    staff_position=item['staff_position'],
                    qualification=item['qualification'],
                    notes=item['notes'],
                    staff_member_id=item['staff_member_id'],
                )
                model_ins.save()
            if key == 'main_team':
                model_ins = models_name(
                    id=item['id'],
                    name=item['name'],
                    city_id=item['city_id'],
                    discipline_name_id=item['discipline_name_id'],
                    staff_team_member_id=item['staff_team_member_id'],
                    curator_id=1
                )
                model_ins.save()
            if key == 'main_player':
                model_ins = models_name(
                    id=item['id'],
                    surname=item['surname'],
                    name=item['name'],
                    patronymic=item['patronymic'],
                    birthday=item['birthday'],
                    gender=item['gender'],
                    level_revision=item['level_revision'],
                    position=item['position'],
                    number=item['number'],
                    is_captain=item['is_captain'],
                    is_assistent=item['is_assistent'],
                    identity_document=item['identity_document'],
                    diagnosis_id=item['diagnosis_id'],
                    discipline_id=item['discipline_id'],
                    document_id=item['document_id']
                )
                model_ins.save()
            if key == 'main_player_team':
                player = Player.objects.get(pk=item['player_id'])
                team = Team.objects.get(pk=item['team_id'])
                player.team.add(team)
        except Exception as e:
            print(f'Ошибка вставки данных {e} -> {item}')
