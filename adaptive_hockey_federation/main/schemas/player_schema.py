from django.urls import reverse
from main.models import Player


def player_list_table(self, context):
    table_head = {}
    for field in self.fields:
        if field != "id":
            table_head[field] = Player._meta.get_field(field).verbose_name
    context["table_head"] = table_head
    table_data = [
        {
            "surname": player.surname,
            "name": player.name,
            "birthday": player.birthday,
            "gender": player.get_gender_display(),
            "number": player.number,
            "discipline": player.discipline if player.discipline else None,
            "diagnosis": (
                player.diagnosis.name if player.diagnosis else None
            ),  # Noqa
            "url": reverse("main:player_id", args=[player.id]),
            "id": player.pk,
        }
        for player in context["players"]
    ]

    context["table_data"] = table_data
    return context


def player_id_table(self, context) -> dict:
    player = context["player"]
    player_fields_personal = [
        ("Фамилия", player.surname),
        ("Имя", player.name),
        ("Отчество", player.patronymic),
        ("Пол", player.gender),
        ("Дата рождения", player.birthday),
        ("Удостоверение личности", player.identity_document),
        ("Дисциплина", player.discipline),
        ("Диагноз", player.diagnosis),
    ]

    player_teams = [
        {
            "name": team.name,
            "url": reverse("main:teams_id", args=[team.id]),
        }
        for team in player.team.all()
    ]

    player_fields = [
        ("Команда", player_teams),
        ("Уровень ревизии", player.level_revision),
        ("Капитан", player.is_captain),
        ("Ассистент", player.is_assistent),
        ("Игровая позиция", player.position),
        ("Номер игрока", player.number),
    ]

    player_documents = self.get_object().player_documemts.all()

    context["player_fields_personal"] = player_fields_personal
    context["player_fields"] = player_fields
    context["player_documents"] = player_documents
    return context
