import re
from typing import Any

from core.constants import FORM_HELP_TEXTS, ROLE_AGENT
from core.utils import max_date, min_date
from django import forms
from django.core.exceptions import ValidationError
from django.forms import (
    ModelChoiceField,
    ModelMultipleChoiceField,
    MultipleChoiceField,
    Select,
    TextInput,
)
from main.models import (
    City,
    DisciplineName,
    Player,
    StaffMember,
    StaffTeamMember,
    Team,
)
from users.models import User


class CustomMultipleChoiceField(MultipleChoiceField):

    def validate(self, value):
        if self.required and not value:
            raise ValidationError(
                self.error_messages["required"], code="required"
            )


class CustomModelMultipleChoiceField(ModelMultipleChoiceField):

    def _check_values(self, value):
        try:
            value = frozenset(value)
        except TypeError:
            raise ValidationError("Неверный список команд!")
        value = list(value)
        qs = Team.objects.filter(pk__in=value)
        return qs


class PlayerForm(forms.ModelForm):

    available_teams = ModelMultipleChoiceField(
        queryset=Team.objects.all().order_by("name"),
        required=False,
        help_text=FORM_HELP_TEXTS["available_teams"],
        label="Команды",
    )

    team = CustomMultipleChoiceField(
        required=True, help_text=FORM_HELP_TEXTS["teams"], label="Команды"
    )

    class Meta:
        model = Player
        fields = [
            "surname",
            "name",
            "patronymic",
            "gender",
            "birthday",
            "discipline_name",
            "discipline_level",
            "diagnosis",
            "level_revision",
            "team",
            "available_teams",
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
            "name": forms.TextInput(attrs={"placeholder": "Введите Имя"}),
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
                attrs={"placeholder": "Введите игровую классификацию"}
            ),
            "birthday": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={
                    "type": "date",
                    "placeholder": "Введите дату рождения",
                    "class": "form-control",
                    "min": min_date,
                    "max": max_date,
                },
            ),
        }
        help_texts = {
            "identity_document": FORM_HELP_TEXTS["identity_document"],
            "birthday": FORM_HELP_TEXTS["birthday"],
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


class PlayerUpdateForm(PlayerForm):

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        if queryset := self.instance.team.all():
            self.fields["team"] = CustomModelMultipleChoiceField(
                queryset=queryset,
                required=True,
                help_text=FORM_HELP_TEXTS["teams"],
                label="Команды",
            )
        queryset_available = Team.objects.all().difference(queryset)
        self.fields["available_teams"] = CustomModelMultipleChoiceField(
            queryset=queryset_available,
            required=False,
            help_text=FORM_HELP_TEXTS["available_teams"],
            label="Команды",
        )


class CityChoiceField(ModelChoiceField):
    """Самодельное поле для выбора города."""

    def __init__(self, label: str | None = None):
        super().__init__(
            queryset=City.objects.all(),
            widget=TextInput(
                attrs={
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

        if not value:
            raise ValidationError(self.error_messages["required"])

        if value.isdigit():
            return super().clean(value)
        else:
            city, created = City.objects.get_or_create(name=value)
            return city


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user: User | None = kwargs.pop("user", None)
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields["curator"].label_from_instance = (
            lambda obj: obj.get_full_name()
        )
        if self.user:
            self.fields["curator"].disabled = self.user.is_agent

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
            "discipline_name": Select(),
            "curator": Select(),
        }

    def save(self, commit=True):
        instance = super(TeamForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class TeamFilterForm(forms.Form):
    name = forms.ModelChoiceField(
        queryset=Team.objects.all().order_by("name"),
        required=False,
        label="Команда",
        widget=forms.Select(attrs={"class": "form-control arrow-before"}),
        empty_label="Все",
    )
    discipline = forms.ModelChoiceField(
        queryset=DisciplineName.objects.all().order_by("name"),
        required=False,
        label="Дисциплина",
        widget=forms.Select(attrs={"class": "form-control arrow-before"}),
        empty_label="Все",
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all().order_by("name"),
        required=False,
        label="Город",
        widget=forms.Select(attrs={"class": "form-control arrow-before"}),
        empty_label="Все",
    )

    class Meta:
        fields = ("name", "discipline", "city")


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
            "team": FORM_HELP_TEXTS["teams"],
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
            "name": forms.TextInput(attrs={"placeholder": "Введите Имя"}),
            "patronymic": forms.TextInput(
                attrs={"placeholder": "Введите отчество"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "Введите номер телефона"}
            ),
        }
