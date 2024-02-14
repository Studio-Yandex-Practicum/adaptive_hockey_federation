from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, Select, TextInput
from main.models import City, DisciplineName, Player, StaffTeamMember, Team
from users.models import User


class PlayerForm(forms.ModelForm):
    identity_document = forms.CharField(
        widget=forms.TextInput,
        label='Удостоверение личности',
        help_text='Удостоверение личности'
    )
    level_revision = forms.CharField(
        widget=forms.TextInput,
        label='Уровень ревизии',
        help_text='Уровень ревизии',
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
            "identity_document",
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
            widget=TextInput(attrs={
                'class': 'form-control',
                'list': 'cities',
                'placeholder': 'Введите или выберите название города'
            }),
            required=True,
            error_messages={
                'required': 'Пожалуйста, выберите город из списка.'
            },
            label='Город откуда команда',
        )

    def clean(self, value: Any) -> Any:
        """Переопределенный метод родительского класса.
        Прежде, чем вызвать родительский метод, получает объект города (
        City) по введенному названию, проверяет наличие введенного
        наименования города в БД. Если такого города в БД нет, то создает
        соответствующий город (объект класса City) и возвращает его на
        дальнейшую стандартную валидацию формы."""
        value = value.strip()

        if (not isinstance(value, str) or
                value in self.empty_values):
            raise ValidationError(self.error_messages['required'])

        if city := City.get_by_name(value):
            return super().clean(city)

        city = City.objects.create(name=value)
        return super().clean(city)


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields[
            'curator'
        ].label_from_instance = lambda obj: obj.get_full_name()

    city = CityChoiceField()

    curator = ModelChoiceField(
        queryset=User.objects.filter(role='agent'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Куратор команды',
        empty_label='Выберите куратора',
        error_messages={
            'required': 'Пожалуйста, выберите куратора из списка.'
        }
    )
    staff_team_member = forms.ModelChoiceField(
        queryset=StaffTeamMember.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Сотрудник команды',
        empty_label='Выберите сотрудника команды',
        error_messages={
            'required': 'Пожалуйста, выберите сотрудника из списка.'
        }
    )
    discipline_name = forms.ModelChoiceField(
        queryset=DisciplineName.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Дисциплина команды',
        empty_label='Выберите дисциплину команды',
        error_messages={
            'required': 'Пожалуйста, выберите дисциплину из списка.'
        }
    )

    class Meta:
        model = Team
        fields = [
            'name',
            'city',
            'staff_team_member',
            'discipline_name',
            'curator'
        ]
        widgets = {
            'name': TextInput(
                attrs={'placeholder': 'Введите название команды'}
            ),
            'staff_team_member': Select(),
            'discipline_name': Select(),
            'curator': Select(),
        }

        def save(self, commit=True):
            instance = super(TeamForm, self).save(commit=False)
            if commit:
                instance.save()
            return instance
