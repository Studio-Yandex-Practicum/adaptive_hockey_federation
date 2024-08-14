from django.conf import settings
from rest_framework import serializers

from games.models import Game, GamePlayer
from main.models import Player


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

    def sort_player_by_team(
        self,
        obj: Game,
        field_name: str,
    ) -> list[list[int]]:
        """
        Метод для сортировки игроков по командам.

        Сортировка в соответствии с порядком команд в поле team_ids.
        """
        game_players = GamePlayer.objects.filter(game_team__game=obj)
        team_players: list[tuple[int, int]] = list(
            game_players.values_list("game_team_id", field_name),
        )
        teams: dict[int, list[int]] = {
            team_id: [] for team_id in self.get_team_ids(obj)
        }
        for team_id, field in team_players:
            teams[team_id].append(field)
        return list(teams.values())

    def get_team_ids(self, obj):
        """Метод получения ID команд."""
        return list(obj.game_teams.values_list("gameteam_id", flat=True))

    def get_player_ids(self, obj):
        """Метод получения ID игроков."""
        return self.sort_player_by_team(obj, "id")

    def get_player_numbers(self, obj):
        """Метод получения номеров игроков."""
        return self.sort_player_by_team(obj, "number")

    def get_token(self, obj):
        """Метод токена."""
        return settings.YANDEX_DISK_OAUTH_TOKEN


# TODO возможно верный сериализатор DS. Уточнить структуру ответа DS
class TrackingSerializer(serializers.Serializer):
    """Сериализатор, обрабатывающий tracking с фреймами."""

    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(),
    )
    team_id = serializers.IntegerField()
    frames = serializers.ListField(
        child=serializers.IntegerField(),
    )
    boxes = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
        ),
    )
    time = serializers.ListField(
        child=serializers.CharField(max_length=50),
    )
    predicted_number = serializers.SerializerMethodField()

    def get_predicted_number(self, obj):
        """Данные predicted_number могут быть как str так и int."""
        return obj.predicted_number


# TODO возможно верный сериализатор DS. Уточнить структуру ответа DS
class GameDataPlayerSerializer(serializers.Serializer):
    """Сериалатор для маршалинга ответа от сервиса дс-ов."""

    game_id = serializers.PrimaryKeyRelatedField(
        queryset=Game.objects.all(),
    )
    tracking = TrackingSerializer(
        many=True,
    )


# TODO уточнить структуру ответа DS
class GameDataPlayerSerializerMock(serializers.Serializer):
    """Сериализатор заглушка ответа DS."""

    number = serializers.IntegerField()
    team = serializers.IntegerField()
    counter = serializers.IntegerField()
    frames = serializers.ListField(
        child=serializers.IntegerField(),
    )
