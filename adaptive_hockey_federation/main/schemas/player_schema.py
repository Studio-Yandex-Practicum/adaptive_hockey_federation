from django.urls import reverse

SEARCH_FIELDS: dict = {
    "surname": "surname",
    "name": "name",
    "birthday": ("year", "month", "day"),
    "gender": "gender",
    "number": "number",
    "discipline_name": "discipline_name__name",
    "discipline_level": "discipline_level__name",
    "team": "team__name",
}


def get_player_table_data(context):
    table_data = [
        {
            "surname": player.surname,
            "name": player.name,
            "birthday": player.birthday,
            "gender": player.get_gender_display(),
            "number": player.number,
            "discipline_name": (
                player.discipline_name if player.discipline_name else None
            ),
            "discipline_level": (
                player.discipline_level if player.discipline_level else None
            ),
            "team": (
                ", ".join([team.name for team in player.team.all()])
                if player.team.exists()
                else "Отсутствует"
            ),
            "url": reverse("main:player_id", args=[player.id]),
            "id": player.pk,
        }
        for player in context["players"]
    ]
    return table_data


def get_player_fields_personal(player):
    data = [
        ("Фамилия", player.surname),
        ("Имя", player.name),
        ("Отчество", player.patronymic),
        ("Пол", player.gender),
        ("Дата рождения", player.birthday),
        ("Удостоверение личности", player.identity_document),
        ("Дисциплина", player.discipline_name),
        ("Числовой статус", player.discipline_level),
        ("Нозология", player.diagnosis.nosology),
        ("Диагноз", player.diagnosis.name),
    ]
    return data


def get_player_fields(player):
    player_teams = [
        {
            "name": team.name,
            "url": reverse("main:teams_id", args=[team.id]),
        }
        for team in player.team.all()
    ]
    player_fields = [
        ("Команда", player_teams),
        ("Игровая классификация", player.level_revision),
        ("Капитан", player.is_captain),
        ("Ассистент", player.is_assistent),
        ("Игровая позиция", player.position),
        ("Номер игрока", player.number),
    ]
    return player_fields
