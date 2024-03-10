from django.urls import reverse
from main.models import Player


def get_player_href(player: Player) -> dict[str, str]:
    """Возвращает словарь с информацией для ссылки на игрока."""
    url = reverse("main:player_id", args=[player.id])
    name = " ".join((player.surname, player.name))
    return {"name": name, "url": url}
