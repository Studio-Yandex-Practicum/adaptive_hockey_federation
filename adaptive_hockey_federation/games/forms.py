from django import forms

from core.constants import (
    MAX_TEAMS_IN_GAME,
    NO_MORE_THAN_TWO_TEAMS_IN_GAME,
    MUST_BE_TWO_TEAMS_IN_A_GAME,
    CANNOT_PLAY_AGAINST_SELF,
)
from games.models import Game
from main.forms import CustomMultipleChoiceField
from main.models import Team


class GameForm(forms.ModelForm):
    """Форма, используемая при создании нового объекта Игры."""

    game_teams = CustomMultipleChoiceField(
        label="Команды",
        required=True,
        help_text="Команды, участвующие в игре",
    )
    available_teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all().order_by("name"),
        required=False,
        help_text="Команды, доступные для участия в игре",
        label="Команды",
    )

    class Meta:
        model = Game
        fields = [
            "name",
            "date",
            "competition",
            "available_teams",
            "game_teams",
            "video_link",
        ]
        widgets = {
            "date": forms.DateTimeInput(
                format="%d-%m-%Y %H:%M",
                attrs={
                    "type": "datetime-local",
                    "placeholder": "Введите дату проведения игры",
                    "class": "form-control",
                },
            ),
        }

    def clean_game_teams(self) -> list[Team]:
        """Метод, проверяющий корректность выбора команд."""
        if len(self.cleaned_data["game_teams"]) > MAX_TEAMS_IN_GAME:
            raise forms.ValidationError(NO_MORE_THAN_TWO_TEAMS_IN_GAME)
        elif len(self.cleaned_data["game_teams"]) < MAX_TEAMS_IN_GAME:
            raise forms.ValidationError(MUST_BE_TWO_TEAMS_IN_A_GAME)
        if (
            self.cleaned_data["game_teams"][0]
            == self.cleaned_data["game_teams"][1]
        ):
            raise forms.ValidationError(CANNOT_PLAY_AGAINST_SELF)
        return self.cleaned_data["game_teams"]
