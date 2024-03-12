from typing import Any

from core.constants import ROLE_AGENT
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, Select, TextInput
from main.models import (
    City,
    DisciplineName,
    Player,
    StaffMember,
    StaffTeamMember,
    Team,
)
from users.models import User


class PlayerForm(forms.ModelForm):
    identity_document = forms.CharField(
        widget=forms.TextInput,
        label="Удостоверение личности",
        help_text="Удостоверение личности",
    )
    level_revision = forms.CharField(
        widget=forms.TextInput,
        label="Уровень ревизии",
        help_text="Уровень ревизии",
    )

    class Meta:
        model = Player
        fields = [
            "surname",
            "name",
            "patronymic",
            "gender",
            "birthday",
            "discipline",
            "diagnosis",
            "level_revision",
            "team",
            "is_captain",
            "is_assistent",
            "position",
            "number",
            "identity_document",
        ]


class CityChoiceField(ModelChoiceField):
    """Самодельное поле для выбора города."""

    def __init__(self):
        super().__init__(
            queryset=City.objects.all(),
            widget=TextInput(
                attrs={
                    "class": "form-control",
                    "list": "cities",
                    "placeholder": "Введите или выберите название города",
                }
            ),
            required=True,
            error_messages={
                "required": "Пожалуйста, выберите город из списка."
            },
            label="Город откуда команда",
        )

    def clean(self, value: Any) -> Any:
        """Переопределенный метод родительского класса.
        Прежде, чем вызвать родительский метод, получает объект города (
        City) по введенному названию, проверяет наличие введенного
        наименования города в БД. Если такого города в БД нет, то создает
        соответствующий город (объект класса City) и возвращает его на
        дальнейшую стандартную валидацию формы."""

        if not isinstance(value, str) or value in self.empty_values:
            raise ValidationError(self.error_messages["required"])

        value = value.strip()

        if city := City.get_by_name(value):
            return super().clean(city)

        city = City.objects.create(name=value)
        return super().clean(city)


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields["curator"].label_from_instance = (
            lambda obj: obj.get_full_name()
        )

    city = CityChoiceField()

    curator = ModelChoiceField(
        queryset=User.objects.filter(role=ROLE_AGENT),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Куратор команды",
        empty_label="Выберите куратора",
        error_messages={
            "required": "Пожалуйста, выберите куратора из списка."
        },
    )
    discipline_name = forms.ModelChoiceField(
        queryset=DisciplineName.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Дисциплина команды",
        empty_label="Выберите дисциплину команды",
        error_messages={
            "required": "Пожалуйста, выберите дисциплину из списка."
        },
    )

    class Meta:
        model = Team
        fields = ["name", "city", "discipline_name", "curator"]
        widgets = {
            "name": TextInput(
                attrs={"placeholder": "Введите название команды"}
            ),
            "staff_team_member": Select(),
            "city": Select(),
            "discipline_name": Select(),
            "curator": Select(),
        }

        def save(self, commit=True):
            instance = super(TeamForm, self).save(commit=False)
            if commit:
                instance.save()
            return instance


class PlayerTeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlayerTeamForm, self).__init__(*args, **kwargs)
        self.fields["player"].label_from_instance = (
            lambda obj: obj.get_name_and_position()
        )

    class Meta:
        labels = {
            "player": "Игрок",
            "team": "Название команды",
        }


class StaffTeamMemberTeamForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StaffTeamMemberTeamForm, self).__init__(*args, **kwargs)
        self.fields["staffteammember"].label_from_instance = (
            lambda obj: obj.get_name_and_staff_position()
        )

    class Meta:
        labels = {
            'staffteammember': 'Сотрудник команды',
            'team': 'Команда',
        }


class StaffTeamMemberForm(forms.ModelForm):

    class Meta:
        model = StaffTeamMember
        fields = ("staff_position", "team", "qualification", "notes",)


class StaffMemberForm(forms.ModelForm):

    class Meta:
        model = StaffMember
        fields = ("id", "surname", "name", "patronymic", "phone",)
