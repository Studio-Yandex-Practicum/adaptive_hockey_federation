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
        return settings.YANDEX_DISK_OAUTH_TOKEN


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


class GameDataPlayerSerializer(serializers.Serializer):
    """Сериалатор для маршалинга ответа от сервиса дс-ов."""

    game_id = serializers.PrimaryKeyRelatedField(
        queryset=Game.objects.all(),
    )
    tracking = TrackingSerializer(
        many=True,
    )
