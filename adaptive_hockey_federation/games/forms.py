from typing import Any

from django import forms
from django.db import transaction
from django.db.models import Q, QuerySet
from django.forms import modelformset_factory
from games.constants import Errors, Literals, NumericalValues
from games.models import Game, GamePlayer, GameTeam
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
        return Team.objects.filter(id__in=value)


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

    @transaction.atomic
    def save(self, commit=True):
        """
        Метод создает и сохраняет объект игры в базе данных.

        Поле game_teams удаляется из обработки, поскольку сохранение нужно
        произвести не по модели Team, а по модели GameTeam. Для этой цели
        id указанных Team передаются в списке через атрибут в сигналы, где
        и происходит дальнейшая обработка.
        """
        if isinstance(self.cleaned_data["game_teams"], list):
            teams = self.cleaned_data.pop("game_teams")
        else:
            teams = self.cleaned_data["game_teams"].values_list(
                "id",
                flat=True,
            )
            # Тут берём ID для того, чтобы передать их в сигнал,
            # иначе всё сломается двумя строчками ниже, т.к. в случае
            # редактирования формы передаётся QuerySet, а не простой список
        del self.fields["game_teams"]
        self.instance.teams = list(map(int, teams))
        instance = super(GameForm, self).save(commit)
        return instance


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
        if queryset := GameTeam.objects.filter(game=self.instance):
            self.fields["game_teams"] = CustomGameMultipleChoiceField(
                queryset=Team.objects.filter(
                    Q(
                        discipline_name__name__in=queryset.values_list(
                            "discipline_name",
                            flat=True,
                        ),
                    )
                    & Q(name__in=queryset.values_list("name", flat=True)),
                ),
                required=True,
                help_text=Literals.GAME_PARTICIPATING_TEAMS,
                label=Literals.GAME_TEAMS,
            )
        available_teams_qs = Team.objects.exclude(
            name__in=queryset.values_list("name", flat=True),
        ).order_by("name")
        self.fields["available_teams"] = CustomGameMultipleChoiceField(
            queryset=available_teams_qs,
            required=False,
            help_text=Literals.GAME_AVAILABLE_TEAMS,
        )


class GamePlayerNumberForm(forms.ModelForm):
    """Форма для редактирования номера игрока."""

    class Meta:
        model = GamePlayer
        fields = ["number"]


EditTeamPlayersNumbersFormSet = modelformset_factory(
    GamePlayer,
    form=GamePlayerNumberForm,
    extra=0,
    can_delete=True,
)


class EditTeamPlayersNumbersForm(forms.Form):
    """Форма для редактирования номеров игроков команды."""

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму для редактирования номеров игроков команды.

        Описание:
        - Извлекает объект game_team из именованных аргументов.
        - Извлекает данные для заполнения формы, если они переданы.
        - Инициализирует форму и формсет EditTeamPlayersNumbersFormSet
        для игроков из указанной команды.
        """
        self.game_team = kwargs.pop("game_team")
        data = kwargs.pop("data", None)
        super().__init__(*args, **kwargs)
        self.formset = EditTeamPlayersNumbersFormSet(
            queryset=GamePlayer.objects.filter(
                game_team=self.game_team,
            ).order_by("last_name", "name"),
            data=data if self.is_bound else None,
        )

    def is_valid(self):
        """Проверка валидности формы и формсета."""
        return super().is_valid() and self.formset.is_valid()

    def save(self):
        """Сохранение изменений формсета."""
        self.formset.save()
