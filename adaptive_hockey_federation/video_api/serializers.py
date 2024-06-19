from games.models import Game, GamePlayer
from rest_framework import serializers


class GameFeatureSerializer(serializers.ModelSerializer):
    """Сериализатор подготовки данных для отправки к DS."""

    game_id = serializers.IntegerField(
        source="id",
    )
    game_link = serializers.CharField(
        source="video_link",
        read_only=True,
    )
    team_ids = serializers.SerializerMethodField()
    player_ids = serializers.SerializerMethodField()
    player_numbers = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "game_id",
            "game_link",
            "player_ids",
            "player_numbers",
            "team_ids",
            "token",
        ]

    def get_team_ids(self, obj):
        """Метод получения ID команд."""
        return list(obj.game_teams.values_list("id", flat=True))

    def get_player_ids(self, obj):
        """Метод получения ID игроков."""
        game_players = GamePlayer.objects.filter(game_team__game=obj)
        return list(game_players.values_list("id", flat=True))

    def get_player_numbers(self, obj):
        """Метод получения номеров игроков."""
        game_players = GamePlayer.objects.filter(game_team__game=obj)
        return list(game_players.values_list("number", flat=True))

    def get_token(self, obj):
        """Метод токена."""
        # TODO: заглушка для отправки токена
        return "y0_AgAAAAA8cbR4AAtjkQAAAAD9CA6QAAA7HIEFePpA7qKzGdujIAwVc_JH9w"
