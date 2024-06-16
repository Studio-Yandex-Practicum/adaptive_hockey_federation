from games.models import Game, GameTeam
from main.models import (Diagnosis, DisciplineLevel, DisciplineName, Document,
                         Nosology, Player, Team)
from rest_framework import serializers


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
