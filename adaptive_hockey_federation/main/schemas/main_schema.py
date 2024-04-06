from django.urls import reverse


def get_main_table_data(context):
    table_data = [
        {
            "surname": player.surname,
            "name": player.name,
            "birthday": player.birthday,
            "gender": player.get_gender_display(),
            "number": player.number,
            "discipline": (player.discipline if player.discipline else None),
            "diagnosis": (player.diagnosis.name if player.diagnosis else None),
            "url": reverse("main:player_id", args=[player.id]),
            "id": player.pk,
        }
        for player in context["main"]
    ]
    return table_data
