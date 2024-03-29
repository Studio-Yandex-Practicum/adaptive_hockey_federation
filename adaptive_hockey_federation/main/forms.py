import re
from datetime import datetime
from typing import Any

from core.constants import (
    FORM_HELP_TEXTS,
    ROLE_AGENT,
    MAX_AGE_PlAYER,
    MIN_AGE_PlAYER,
)
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

    now = datetime.now()
    month_day = format(now.strftime("%m-%d"))
    min_date = f"{str(now.year - MAX_AGE_PlAYER)}-{month_day}"
    max_date = f"{str(now.year - MIN_AGE_PlAYER)}-{month_day}"

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.fields["team"].required = False

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
        widgets = {
            "surname": forms.TextInput(
                attrs={"placeholder": "Введите фамилию"}
            ),
            "name": forms.TextInput(
                attrs={"placeholder": "Введите Имя"}
            ),
            "patronymic": forms.TextInput(
                attrs={"placeholder": "Введите отчество"}
            ),
            "identity_document": forms.TextInput(
                attrs={"placeholder": "Введите название документа"}
            ),
            "number": forms.TextInput(
                attrs={"placeholder": "Введите номер игрока"}
            ),
            "level_revision": forms.TextInput(
                attrs={"placeholder": "Введите уровень ревизии"}
            ),
            "birthday": forms.TextInput(
                attrs={"placeholder": "Введите дату рождения", "type": "date"}
            ),
        }
        help_texts = {
            "identity_document": FORM_HELP_TEXTS["identity_document"],
            "birthday": FORM_HELP_TEXTS["birthday"],
            "team": FORM_HELP_TEXTS["team"],
        }

    def save_m2m(self):
        self.instance.team.through.objects.filter(
            team__in=self.cleaned_data["team"]
        ).delete()
        self.instance.team.set(self.cleaned_data["team"])

    def save(self, *args, **kwargs):
        instance = super().save()
        self.save_m2m()
        return instance

    def clean_identity_document(self):
        document = self.cleaned_data["identity_document"]
        if re.fullmatch(r"Паспорт \d{4}\s\d{6}", document) or re.fullmatch(
            r"Свидетельство о рождении \D{4}\s\d{6}", document
        ):
            return document
        raise ValidationError(
            "Введите данные в формате 'Паспорт ХХХХ ХХХХХХ' или"
            "'Свидетельство о рождении X-XX XXXXXX'"
        )


class CityChoiceField(ModelChoiceField):
    """Самодельное поле для выбора города."""

    def __init__(self, label: str | None = None):
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
            label=label or "Выберите город",
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
        self.user: User | None = kwargs.pop("user", None)
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields["curator"].label_from_instance = (
            lambda obj: obj.get_full_name()
        )
        if self.user:
            self.fields["curator"].disabled = self.user.is_agent

    city = CityChoiceField(label="Выберите город, откуда команда.")

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
            "staffteammember": "Сотрудник команды",
            "team": "Команда",
        }


class StaffTeamMemberForm(forms.ModelForm):
    class Meta:
        model = StaffTeamMember
        fields = (
            "staff_position",
            "team",
            "qualification",
            "notes",
        )
        help_texts = {
            "team": FORM_HELP_TEXTS["team"],
        }


class StaffMemberForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = (
            "surname",
            "name",
            "patronymic",
            "phone",
        )
        widgets = {
            "surname": forms.TextInput(
                attrs={"placeholder": "Введите фамилию"}
            ),
            "name": forms.TextInput(
                attrs={"placeholder": "Введите Имя"}
            ),
            "patronymic": forms.TextInput(
                attrs={"placeholder": "Введите отчество"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "Введите номер телефон"}
            ),
        }
