from rest_framework import serializers

from games.models import Game, GameTeam, GamePlayer
from main.models import (
    Diagnosis,
    DisciplineLevel,
    DisciplineName,
    Document,
    Nosology,
    Player,
    Team,
)


class NosologySerializers(serializers.ModelSerializer):
    """Сериализатор для модели Nosology."""

    class Meta:
        model = Nosology
        fields = "__all__"


class DiagnosisSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Diagnosis."""

    nosology = NosologySerializers(read_only=True)

    class Meta:
        model = Diagnosis
        fields = "__all__"


class DisciplineNameSerializer(serializers.ModelSerializer):
    """Сериализатор для модели DisciplineName."""

    class Meta:
        model = DisciplineName
        fields = "__all__"


class DisciplineLevelSerializer(serializers.ModelSerializer):
    """Сериализатор для модели DisciplineLevel."""

    class Meta:
        model = DisciplineLevel
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Team."""

    class Meta:
        model = Team
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Document."""

    class Meta:
        model = Document
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Player."""

    diagnosis = DiagnosisSerializer(read_only=True)
    discipline_name = DisciplineNameSerializer(read_only=True)
    discipline_level = DisciplineLevelSerializer(read_only=True)
    team = TeamSerializer(many=True, read_only=True)
    player_documemts = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Player
        fields = [
            "id",
            "surname",
            "name",
            "patronymic",
            "birthday",
            "addition_date",
            "gender",
            "level_revision",
            "position",
            "number",
            "is_captain",
            "is_assistent",
            "identity_document",
            "diagnosis",
            "discipline_name",
            "discipline_level",
            "team",
            "player_documemts",
        ]


class GameTeamSerializer(serializers.ModelSerializer):
    """Сериализатор для модели GameTeam."""

    team = TeamSerializer(read_only=True)

    class Meta:
        model = GameTeam
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Game."""

    game_teams = GameTeamSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
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
