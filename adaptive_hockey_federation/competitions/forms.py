from typing import Any

from competitions.models import CHAR_FIELD_LENGTH, Competition
from competitions.validators import date_not_before_today
from core.constants import FORM_HELP_TEXTS
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField
from main.forms import CityChoiceField, CustomMultipleChoiceField
from main.models import DisciplineName, Team


class CustomDisciplineMultipleChoiceField(ModelMultipleChoiceField):
    """Множественное поле выбора для дисциплин."""

    def _check_values(self, value):
        try:
            value = frozenset(value)
        except TypeError:
            raise ValidationError("Неверный список дисциплин!")
        value = list(value)
        qs = DisciplineName.objects.filter(pk__in=value)
        return qs


class CompetitionForm(forms.ModelForm):
    """Форма для соревнований."""

    def __init__(self, *args, **kwargs):
        """
        Метод инициализации экземпляра класса.

        1. Вызывает метод, делающий поля неактивными при соблюдении
        условия
        2. Включает валидацию полей, если они активны.
        """
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

    available_disciplines = ModelMultipleChoiceField(
        queryset=DisciplineName.objects.all().order_by("name"),
        required=False,
        help_text=FORM_HELP_TEXTS["disciplines"],
        label="Дисциплины",
    )

    disciplines = CustomMultipleChoiceField(
        required=True,
        help_text=FORM_HELP_TEXTS["disciplines"],
        label="Дисциплины",
    )

    location = forms.CharField(
        label="Место проведения (адрес, учреждение и т.д.)",
        max_length=CHAR_FIELD_LENGTH,
    )

    date_start = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"},
        ),
        label="Дата начала",
        error_messages={"required": "Пожалуйста, укажите дату начала."},
    )
    date_end = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"},
        ),
        label="Дата завершения",
        error_messages={"required": "Пожалуйста, укажите дату завершения."},
    )

    def set_readonly(self, field: str, readonly_value: bool):
        """
        Делает поле формы неактивным при соблюдении условия.

        - field - название поля.
        - readonly_value - любое bool условие. Если условие не
        соблюдается, поле активируется.
        """
        self.fields[field].disabled = readonly_value

    class Meta:
        model = Competition
        fields = [
            "title",
            "city",
            "location",
            "available_disciplines",
            "disciplines",
            "date_start",
            "date_end",
        ]

    def save_m2m(self):
        """Метод сохраняет M2M связи между соревнованиями и дисциплинами."""
        self.instance.disciplines.through.objects.filter(
            disciplinename__in=self.cleaned_data["disciplines"],
        ).delete()
        self.instance.disciplines.set(self.cleaned_data["disciplines"])

    def save(self, commit=True):
        """Метод создает и сохраняет объект соревнования в базе данных."""
        instance = super(CompetitionForm, self).save(commit=True)
        if commit:
            instance.save()
        self.save_m2m()
        return instance

    def clean(self):
        """Метод, выполняющий валидацию полей формы."""
        cleaned_data = super().clean()
        date_start = cleaned_data.get("date_start")
        date_end = cleaned_data.get("date_end")
        if date_start and date_end and date_start > date_end:
            raise forms.ValidationError(
                "Дата окончания соревнования должна "
                "быть позже или совпадать с датой "
                "начала.",
            )
        return cleaned_data


class TeamField(forms.ModelChoiceField):
    """
    Заказное поле для выбора названия команды.

    Работает с виджетом TextInput.
    Для корректного отображения на вэб-странице должен быть элемент:
        <datalist id="available_teams">
            <option_value="Название команды"></option>
            ...и так для каждой команды в списке.
        </datalist>.
    """

    def __init__(self, competition: Competition):
        """
        Метод инициализации экземпляра класса.

        1. Добавляет виджет для поиска команды по названию
        2. Добавляет атрибут competition.
        """
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
                },
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


class CompetitionUpdateForm(CompetitionForm):
    """Форма для обновления соревнований."""

    def __init__(self, *args, **kwargs):
        """
        Метод инициализации экземпляра класса.

        1. Добавляет множественное поле выбора для disciplines
        2. Добавляет множественное поле выбора для available_disciplines.
        """
        super(CompetitionForm, self).__init__(*args, **kwargs)
        if queryset := self.instance.disciplines.all():
            self.fields["disciplines"] = CustomDisciplineMultipleChoiceField(
                queryset=queryset,
                required=True,
                help_text=FORM_HELP_TEXTS["disciplines"],
                label="Дисциплины",
            )
        queryset_available = DisciplineName.objects.all().difference(queryset)
        self.fields["available_disciplines"] = (
            CustomDisciplineMultipleChoiceField(
                queryset=queryset_available,
                required=False,
                help_text=FORM_HELP_TEXTS["available_disciplines"],
                label="Дисциплины",
            )
        )


class CompetitionTeamForm(forms.ModelForm):
    """
    Форма для добавления команд в соревнование.

    Работает с промежуточной моделью Competition_Team.
    """

    def __init__(self, *args, **kwargs):
        """
        Метод инициализации экземпляра класса.

        1. Добавляет атрибут competition
        2. Добавляет поле выбора team.
        """
        self.competition = kwargs.pop("competition")
        super(CompetitionTeamForm, self).__init__(*args, **kwargs)
        self.fields["team"] = TeamField(competition=self.competition)

    class Meta:
        model = Competition.teams.through
        fields = ["team"]

    def save(self, commit=True):
        """Метод создает и сохраняет объект в базе данных."""
        instance = super(CompetitionTeamForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
