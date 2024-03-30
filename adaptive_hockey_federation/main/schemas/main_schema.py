from django.urls import reverse
from main.models import Player


def search_table(self, context, search):
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
            "discipline": (player.discipline if player.discipline else None),
            "diagnosis": (player.diagnosis.name if player.diagnosis else None),
            "url": reverse("main:player_id", args=[player.id]),
            "id": player.pk,
        }
        for player in context["main"]
    ]
    context["table_data"] = table_data
    return context
