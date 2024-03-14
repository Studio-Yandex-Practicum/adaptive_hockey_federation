from main.models import Player
from users.models import User


def agent_has_player_permission(user: User, player: Player):
    """Проверка, имеет ли представитель право доступа к игроку.
    Проверяет только пользователей с role == agent. Остальным просто выдает
    разрешение."""
    if not user.is_agent:
        return True
    return player.team.filter(curator=user).exists()
