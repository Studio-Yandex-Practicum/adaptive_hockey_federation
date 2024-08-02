import re
from typing import Any

from django.core.exceptions import ValidationError
from django.forms import (
    ModelChoiceField,
    ModelMultipleChoiceField,
    MultipleChoiceField,
    TextInput,
)
from django.shortcuts import get_object_or_404

from main.models import City, Diagnosis, StaffTeamMember, Team


class CustomMultipleChoiceField(MultipleChoiceField):
    """Класс для расширения множественного поля выбора."""

    def validate(self, value):
        """Метод для валидации обязательного значения."""
        if self.required and not value:
            raise ValidationError(
                self.error_messages["required"],
                code="required",
            )


class CustomModelMultipleChoiceField(ModelMultipleChoiceField):
    """Класс для расширения множественного поля выбора модели."""

    def _check_values(self, value):
        """Метод, проверяющий правильно ли указан список команд."""
        try:
            value = frozenset(value)
        except TypeError:
            raise ValidationError("Неверный список команд!")
        value = list(value)
        qs = Team.objects.filter(pk__in=value)
        return qs


class CustomDiagnosisChoiceField(ModelChoiceField):
    """Самодельное поле для ввода диагноза."""

    def __init__(self, label: str | None = None):
        """
        Метод инициализации экземпляра класса.

        Добавляет виджет к полю выбора для поиска диагноза по названию.
        """
        super().__init__(
            queryset=Diagnosis.objects.all(),
            required=True,
            widget=TextInput(
                attrs={
                    "list": "diagnosis",
                    "placeholder": "Введите название диагноза",
                },
            ),
            error_messages={
                "required": "Пожалуйста, выберите диагноз из списка.",
            },
            label=label or "Выберите диагноз",
        )

    def clean(self, value: Any) -> Any:
        """
        Метод валидации поля.

        Прежде, чем вызвать родительский метод, получает объект диагноза
        (Diagnosis) по введенному названию, проверяет наличие введенного
        наименования диагноза в БД.
        """
        if not value:
            raise ValidationError(self.error_messages["required"])
        return value


class CityChoiceField(ModelChoiceField):
    """Самодельное поле для выбора города."""

    def __init__(self, label: str | None = None):
        """
        Метод инициализации экземпляра класса.

        Добавляет виджет к полю выбора для поиска города по названию.
        """
        super().__init__(
            queryset=City.objects.all(),
            widget=TextInput(
                attrs={
                    "list": "cities",
                    "placeholder": "Введите или выберите название города",
                },
            ),
            required=True,
            error_messages={
                "required": "Пожалуйста, выберите город из списка.",
            },
            label=label or "Выберите город",
        )

    def clean(self, value: Any) -> Any:
        """
        Переопределенный метод родительского класса.

        Прежде, чем вызвать родительский метод, получает объект города (
        City) по введенному названию, проверяет наличие введенного
        наименования города в БД. Если такого города в БД нет, то создает
        соответствующий город (объект класса City) и возвращает его на
        дальнейшую стандартную валидацию формы.
        """
        if not value:
            raise ValidationError(self.error_messages["required"])

        if value.isdigit():
            return super().clean(value)
        else:
            city, created = City.objects.get_or_create(name=value)
            return city


class StaffTeamMemberChoiceField(ModelChoiceField):
    """Самодельное поле выбора сотрудника команды."""

    def __init__(self, team: Team, data_list: str, label: str | None = None):
        """
        Метод инициализации экземпляра класса.

        Добавляет виджет к полю выбора для поиска сотрудника команды.
        """
        super().__init__(
            queryset=StaffTeamMember.objects.all(),
            widget=TextInput(
                attrs={
                    "list": data_list,
                    "placeholder": "Начните ввод и выберите из списка",
                },
            ),
            required=True,
            error_messages={
                "required": "Пожалуйста, выберите сотрудника из списка.",
            },
            label=label or "Выберите сотрудника",
        )
        self.team = team

    def clean(self, value: Any) -> Any:
        """
        Переопределенный метод родительского класса.

        Прежде, чем вызвать родительский метод, получает объект
        StaffTeamMember и возвращает его на
        дальнейшую стандартную валидацию формы.
        """
        if not value:
            raise ValidationError(self.error_messages["required"])

        if value.isdigit():
            value = value
        elif m := re.search(r"\d+\)\Z", value):
            value = int(m.group()[:-1])
        else:
            raise ValidationError("Неверный формат введенных данных.")
        staff_team_member = get_object_or_404(StaffTeamMember, id=value)
        if StaffTeamMember.team.through.objects.filter(
            staffteammember=staff_team_member,
            team=self.team,
        ).exists():
            raise ValidationError("Этот сотрудник уже есть в команде.")
        return super().clean(value)
