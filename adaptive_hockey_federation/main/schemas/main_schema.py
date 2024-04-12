from django.urls import reverse


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
