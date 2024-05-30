from typing import Any

from django import forms
from django.db.models import QuerySet

from games.constants import Errors, NumericalValues, Literals
from games.models import Game
from main.forms import CustomMultipleChoiceField
from main.models import Team


class CustomGameMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Кастомное поле выбора для команд."""

    @staticmethod
    def _check_values(value: Any) -> QuerySet:
        """
        Переопределение стандартного метода проверки значений.

        Используется для обхода ограничения Django на использование
        QuerySet.filter после QuerySet.difference.
        """
        try:
            value = frozenset(value)
        except TypeError:
            raise forms.ValidationError(Errors.INCORRECT_GAME_TEAMS)
        value = list(value)
        qs = Team.objects.filter(pk__in=value)
        return qs


class GameForm(forms.ModelForm):
    """Форма, используемая при создании нового объекта игры."""

    game_teams = CustomMultipleChoiceField(
        label=Literals.GAME_TEAMS,
        required=True,
        help_text=Literals.GAME_PARTICIPATING_TEAMS,
    )
    available_teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all().order_by("name"),
        required=False,
        help_text=Literals.GAME_AVAILABLE_TEAMS,
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
                format="%Y-%m-%d %H:%M",
                attrs={
                    "type": "datetime-local",
                    "placeholder": Literals.GAME_FORM_DATETIME_PLACEHOLDER,
                    "class": "form-control",
                },
            ),
        }

    def clean_game_teams(self) -> list[Team]:
        """Метод, проверяющий корректность выбора команд."""
        if (
            len(self.cleaned_data["game_teams"])
            > NumericalValues.MAX_TEAMS_IN_GAME
        ):
            raise forms.ValidationError(Errors.NO_MORE_THAN_TWO_TEAMS_IN_GAME)
        elif (
            len(self.cleaned_data["game_teams"])
            < NumericalValues.MAX_TEAMS_IN_GAME
        ):
            raise forms.ValidationError(Errors.MUST_BE_TWO_TEAMS_IN_A_GAME)
        if (
            self.cleaned_data["game_teams"][0]
            == self.cleaned_data["game_teams"][1]
        ):
            raise forms.ValidationError(Errors.CANNOT_PLAY_GAME_AGAINST_SELF)
        return self.cleaned_data["game_teams"]


class GameUpdateForm(GameForm):
    """Форма, используемая при обновлении существующего объекта игры."""

    def __init__(self, *args, **kwargs):
        """
        Метод инициализации экземпляра класса.

        При инициализации переопределяем queryset для полей формы game_teams
        и available_teams со значениями, полученными из текущей игры для
        корректного отображения команд, доступны к выбору, и команд, уже
        участвующих в игре.
        """
        super(GameForm, self).__init__(*args, **kwargs)
        if queryset := self.instance.game_teams.all():
            self.fields["game_teams"] = CustomGameMultipleChoiceField(
                queryset=queryset,
                required=True,
                help_text=Literals.GAME_PARTICIPATING_TEAMS,
                label=Literals.GAME_TEAMS,
            )
        available_teams_qs = (
            Team.objects.all().difference(queryset).order_by("name")
        )
        self.fields["available_teams"] = CustomGameMultipleChoiceField(
            queryset=available_teams_qs,
            required=False,
            help_text=Literals.GAME_AVAILABLE_TEAMS,
        )
