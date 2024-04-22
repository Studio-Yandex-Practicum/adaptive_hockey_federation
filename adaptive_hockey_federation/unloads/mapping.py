from main.schemas.player_schema import SEARCH_FIELDS
from main.schemas.team_schema import TEAM_SEARCH_FIELDS

model_mapping = {
    "players": ("main", "Player", "Данные игроков", SEARCH_FIELDS),
    "teams": ("main", "Team", "Данные команд", TEAM_SEARCH_FIELDS),
    "competitions": (
        "competitions",
        "Competition",
        "Данные соревнований",
    ),
    "analytics": ("main", "Player", "Данные аналитики", SEARCH_FIELDS),
    "users": (
        "users",
        "User",
        "Данные пользователей",
    ),
}
