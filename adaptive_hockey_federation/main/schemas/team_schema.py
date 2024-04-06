from core.constants import STAFF_POSITION_CHOICES
from django.urls import reverse
from main.controllers.utils import get_player_href

TEAM_SEARCH_FIELDS = {
    "discipline_name": "discipline_name_id__name",
    "name": "name",
    "city": "city__name",
}

TEAM_TABLE_HEAD = {
    "name": "Название",
    "discipline_name": "Дисциплина",
    "city": "Город",
    "team_structure": "Состав команды",
}


def get_staff_table(team):
    staff_table = [
        {
            "position": staff_position[1].title(),
            "head": {
                "number": "№",
                "surname": "Фамилия",
                "name": "Имя",
                "position": "Квалификация",
                "note": "Примечание",
            },
            "data": [
                {
                    "number": i + 1,
                    "surname": staff.staff_member.surname,
                    "name": staff.staff_member.name,
                    "position": staff.qualification,
                    "note": staff.notes,
                    "id": staff.id,
                }
                for i, staff in enumerate(
                    team.team_members.filter(staff_position=staff_position[1])
                )
            ],
        }
        for staff_position in STAFF_POSITION_CHOICES
    ]
    return staff_table


def get_players_table(players):
    players_table = {
        "name": "Игроки",
        "head": {
            "full_name": "Фамилия, Имя",
            "birthday": "Д.Р.",
            "gender": "Пол",
            "position": "Квалификация",
            "diagnosis": "Диагноз",
            "number": "Номер игрока",
            "level_revision": "Уровень ревизии",
        },
        "data": [
            {
                "full_name_link": get_player_href(player),
                "birthday": player.birthday,
                "gender": player.get_gender_display(),
                "position": player.get_position_display(),
                "diagnosis": (
                    player.diagnosis.name if player.diagnosis else None
                ),
                "number": player.number,
                "level_revision": player.level_revision,
                "id": player.pk,
            }
            for player in players
        ],
    }
    return players_table


def get_team_table_data(teams, user):
    table_data = []
    for team in teams:
        team_data = {
            "id": team.id,
            "name": team.name,
            "discipline_name": team.discipline_name,
            "city": team.city,
            "_ref_": {
                "name": "Посмотреть",
                "type": "button",
                "url": reverse("main:teams_id", args=[team.id]),
            },
            "allow_edit": user.is_admin
            or (user.is_agent and team.curator == user),
        }
        table_data.append(team_data)

    return table_data
