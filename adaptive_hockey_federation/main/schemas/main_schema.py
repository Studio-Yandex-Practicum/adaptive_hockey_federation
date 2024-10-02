from django.urls import reverse

no_search_pages = [
    "analytics",
    "player_id",
    "player_create",
    "player_id_edit",
    "user_create",
    "user_update",
    "team_create",
    "team_update",
    "teams_id",
    "staff_create",
    "staff_id",
    "staff_id_edit",
    "teams",
    "competition_add",
    "competition_update",
    "competition_id",
    "game_info",
]

show_return_button = [
    "player_id",
    "player_create",
    "player_id_edit",
    "user_create",
    "user_update",
    "team_create",
    "team_update",
    "teams_id",
    "staff_create",
    "staff_id",
    "staff_id_edit",
    "competition_add",
    "competition_update",
    "competition_id",
    "game_create",
    "staff_id_team_edit",
    "staff_id_team_create",
    "edit_team_players_numbers",
    "game_edit",
    "game_info",
]


def get_main_table_data(context):
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
            "diagnosis": (player.diagnosis.name if player.diagnosis else None),
            "url": reverse("main:player_id", args=[player.id]),
            "id": player.pk,
        }
        for player in context["main"]
    ]
    return table_data
