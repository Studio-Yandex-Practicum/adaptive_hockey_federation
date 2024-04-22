from django.urls import reverse

SEARCH_FIELDS = {
    "surname": ("surname__icontains", "", "search", None),
    "name": ("name__icontains", "", "search", None),
    "birthday": (
        ("birthday__year__icontains", "birthday__year__exact", "year", None),
        (
            "birthday__month__icontains",
            "birthday__month__exact",
            "month",
            None,
        ),
        ("birthday__day__icontains", "birthday__day__exact", "day", None),
    ),
    "gender": ("gender__icontains", "gender__exact", "gender", None),
    "number": ("number__icontains", "", "search", None),
    "discipline_name": (
        "discipline_name__name__icontains",
        "",
        "search",
        None,
    ),
    "discipline_level": (
        "discipline_level__name__icontains",
        "",
        "search",
        None,
    ),
    "team": ("team__name__icontains", "", "search", None),
}

ANALITICS_SEARCH_FIELDS = {
    "timespan": "addition_date__gte",
    "birthday": "birthday__year__exact",
    "discipline": "discipline_name__id",
    "city": "team__city",
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
                [team.name for team in player.team.all()]
                if player.team.exists()
                else ["Отсуствует"]
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
        ("Диагноз", player.diagnosis),
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
