from core.constants import FILE_RESOLUTION, MAX_UPLOAD_SIZE_MB
from django.urls import reverse
from main.models import Player, Team


def get_player_href(player: Player) -> dict[str, str]:
    """Возвращает словарь с информацией для ссылки на игрока."""
    url = reverse("main:player_id", args=[player.id])
    name = " ".join((player.surname, player.name))
    return {"name": name, "url": url}


def get_team_href(team: Team) -> dict[str, str]:
    """Возвращает словарь с информацией для ссылки на команду."""
    url = reverse("main:teams_id", args=[team.id])
    name = team.name
    return {"name": name, "url": url}


def errormessage() -> str:
    return (
        "Максимальный размер файла " + MAX_UPLOAD_SIZE_MB
        + ", допустимые разрешения " + ", ".join(FILE_RESOLUTION))
