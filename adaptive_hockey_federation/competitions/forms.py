from typing import Any

from competitions.models import CHAR_FIELD_LENGTH, Competition
from competitions.validators import date_not_before_today
from django import forms
from django.core.exceptions import ValidationError
from main.forms import CityChoiceField
from main.models import Team


class CompetitionForm(forms.ModelForm):
    """Форма для соревнований."""

    def __init__(self, *args, **kwargs):
        super(CompetitionForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            self.set_readonly("date_start", self.instance.is_started)
            self.set_readonly("date_end", self.instance.is_ended)

        for field in [self.fields["date_start"], self.fields["date_end"]]:
            if field.disabled:
                field.validators = []
            else:
                field.validators = [date_not_before_today]

    title = forms.CharField(label="Название")
    city = CityChoiceField(label="Город, где проводятся соревнования")

    location = forms.CharField(
        label="Место проведения (адрес, учреждение и т.д.)",
        max_length=CHAR_FIELD_LENGTH,
    )

    date_start = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        ),
        label="Дата начала",
        error_messages={"required": "Пожалуйста, укажите дату начала."},
    )
    date_end = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        ),
        label="Дата завершения",
        error_messages={"required": "Пожалуйста, укажите дату завершения."},
    )

    def set_readonly(self, field: str, readonly_value: bool):
        """Делает поле формы неактивным при соблюдении условия.
        - field - название поля.
        - readonly_value - любое bool условие. Если условие не
        соблюдается, поле активируется.
        """
        self.fields[field].disabled = readonly_value

    class Meta:
        model = Competition
        fields = ["title", "city", "location", "date_start", "date_end"]

    def save(self, commit=True):
        instance = super(CompetitionForm, self).save(commit=True)
        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        date_start = cleaned_data.get("date_start")
        date_end = cleaned_data.get("date_end")
        if date_start and date_end and date_start > date_end:
            raise forms.ValidationError(
                "Дата окончания соревнования должна "
                "быть позже или совпадать с датой "
                "начала."
            )
        return cleaned_data


class TeamField(forms.ModelChoiceField):
    """Заказное поле для выбора названия команды.
    Работает с виджетом TextInput.
    Для корректного отображения на вэб-странице должен быть элемент:
        <datalist id="available_teams">
            <option_value="Название команды"></option>
            ...и так для каждой команды в списке.
        </datalist>
    """

    def __init__(self, competition: Competition):
        super(TeamField, self).__init__(
            queryset=Team.objects.all(),
            widget=forms.TextInput(
                attrs={
                    "class": "form-control",
                    "list": "available_teams",
                    "placeholder": (
                        "Начните вводить название команды "
                        "и выберите из списка"
                    ),
                }
            ),
            label="Поиск команды для допуска",
        )
        self.competition = competition

    def clean(self, value: Any) -> Any:
        """Переопределенный метод родительского класса."""

        if not isinstance(value, str) or value in self.empty_values:
            raise ValidationError(self.error_messages["required"])

        value = value.strip()

        if team := Team.get_by_name(value):
            if self.competition.teams.filter(id=team.id).exists():
                raise ValidationError("Команда уже добавлена в соревнования.")
            return super().clean(team)

        raise ValidationError("Такой команды не существует")


class CompetitionTeamForm(forms.ModelForm):
    """Форма для добавления команд в соревнование.
    Работает с промежуточной моделью Competition_Team."""

    def __init__(self, *args, **kwargs):
        self.competition = kwargs.pop("competition")
        super(CompetitionTeamForm, self).__init__(*args, **kwargs)
        self.fields["team"] = TeamField(competition=self.competition)

    class Meta:
        model = Competition.teams.through
        fields = ["team"]

    def save(self, commit=True):
        instance = super(CompetitionTeamForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
