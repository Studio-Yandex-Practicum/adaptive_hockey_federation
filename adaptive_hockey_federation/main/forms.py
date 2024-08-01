import re
from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.forms import (
    ModelChoiceField,
    ModelMultipleChoiceField,
    MultipleChoiceField,
    Select,
    TextInput,
)
from django.shortcuts import get_object_or_404

from core.constants import FORM_HELP_TEXTS, Role, StaffPosition
from core.utils import max_date, min_date
from main.models import (
    City,
    Diagnosis,
    DisciplineName,
    Nosology,
    Player,
    StaffMember,
    StaffTeamMember,
    Team,
)
from users.models import User


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


class PlayerForm(forms.ModelForm):
    """Форма для игрока."""

    nosology = ModelChoiceField(
        queryset=Nosology.objects.all(),
        required=True,
        error_messages={
            "required": "Пожалуйста, выберите нозологию из списка.",
        },
        label="Нозология",
    )

    diagnosis = CustomDiagnosisChoiceField()

    class Meta:
        model = Player
        fields = [
            "surname",
            "name",
            "patronymic",
            "gender",
            "birthday",
            "identity_document",
            "discipline_name",
            "discipline_level",
            "nosology",
            "diagnosis",
            "level_revision",
            "is_captain",
            "is_assistent",
            "position",
            "number",
        ]
        widgets = {
            "surname": forms.TextInput(
                attrs={"placeholder": "Введите фамилию"},
            ),
            "name": forms.TextInput(attrs={"placeholder": "Введите Имя"}),
            "patronymic": forms.TextInput(
                attrs={"placeholder": "Введите отчество"},
            ),
            "identity_document": forms.TextInput(
                attrs={"placeholder": "Введите название документа"},
            ),
            "number": forms.TextInput(
                attrs={"placeholder": "Введите номер игрока"},
            ),
            "level_revision": forms.TextInput(
                attrs={"placeholder": "Введите игровую классификацию"},
            ),
            "birthday": forms.DateInput(
                format="%Y-%m-%d",
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

    def __init__(self, *args, **kwargs):
        """Инициализация формы для игрока."""
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["nosology"].initial = self.instance.diagnosis.nosology
            self.fields["diagnosis"].initial = self.instance.diagnosis

    def save(self, commit=True):
        """Метод создает и сохраняет объект игрока в базе данных."""
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

    def clean_identity_document(self):
        """Метод, выполняющий валидацию документа, удостоверяющего личность."""
        document = self.cleaned_data["identity_document"]
        if re.search(r"[П|п]аспорт", document) or re.search(
            r"[С|с]видетельство о рождении",
            document,
        ):
            return document
        raise ValidationError(
            "Введите данные в формате 'Паспорт ХХХХ ХХХХХХ' или"
            "'Свидетельство о рождении X-XX XXXXXX'",
        )

    def clean_diagnosis(self):
        """Метод, выполняющий валидацию поля с диагнозом."""
        nosology = self.cleaned_data.get("nosology")
        diagnosis = self.cleaned_data.get("diagnosis")
        if Diagnosis.objects.filter(name=diagnosis).exists():
            diagnos = Diagnosis.objects.get(name=diagnosis)
            if diagnos.nosology != nosology:
                diagnos.nosology = nosology
                diagnos.save()
            return diagnos
        diagnos = Diagnosis.objects.create(name=diagnosis, nosology=nosology)
        return diagnos


class PlayerUpdateForm(PlayerForm):
    """Форма для обновления игрока."""

    def __init__(self, *args, **kwargs):
        """
        Метод инициализации экземпляра класса.

        Расширяет team и available_teams кастомными полями выбора.
        """
        super(PlayerUpdateForm, self).__init__(*args, **kwargs)
        queryset = self.instance.team.all()
        self.fields["team"] = CustomModelMultipleChoiceField(
            queryset=queryset,
            required=True,
            help_text=FORM_HELP_TEXTS["player_teams"],
            label="Команды",
        )
        queryset_available = Team.objects.all().difference(queryset)
        self.fields["available_teams"] = CustomModelMultipleChoiceField(
            queryset=queryset_available,
            required=False,
            help_text=FORM_HELP_TEXTS["available_teams"],
            label="Команды",
        )
        if self.instance.pk:
            self.fields["nosology"].initial = self.instance.diagnosis.nosology
            self.fields["diagnosis"].initial = self.instance.diagnosis

    def clean_number(self):
        """
        Метод, выполняющий валидацию номера игрока.

        Если номер игрока уже присвоен другому игроку в выбранной команде,
        то выбрасывается исключение.
        """
        number = self.cleaned_data["number"]
        selected_teams = self.cleaned_data.get(
            "team",
            self.instance.team.all(),
        )

        if (
            Player.objects.filter(number=number, team__in=selected_teams)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise ValidationError(
                "Этот номер уже используется другим игроком "
                "в выбранной команде.",
            )

        return number

    def save(self, commit=True):
        """
        Метод сохраняет объект игрока в базе данных.

        Сохраняется информация о командах игрока.
        """
        instance = super().save(commit=False)
        if commit:
            instance.save()
            instance.team.through.objects.filter(
                team__in=self.cleaned_data["team"],
            ).delete()
            instance.team.set(self.cleaned_data["team"])
        return instance


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


class TeamForm(forms.ModelForm):
    """Форма для команды."""

    def __init__(self, *args, **kwargs):
        """Метод инициализации экземпляра класса."""
        self.user: User | None = kwargs.pop("user", None)
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields["curator"].label_from_instance = (
            lambda obj: obj.get_full_name()
        )
        if self.user:
            self.fields["curator"].disabled = self.user.is_agent

    city = CityChoiceField()

    curator = ModelChoiceField(
        queryset=User.objects.filter(role=Role.AGENT),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Куратор команды",
        empty_label="Выберите куратора",
        error_messages={
            "required": "Пожалуйста, выберите куратора из списка.",
        },
    )
    discipline_name = forms.ModelChoiceField(
        queryset=DisciplineName.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Дисциплина команды",
        empty_label="Выберите дисциплину команды",
        error_messages={
            "required": "Пожалуйста, выберите дисциплину из списка.",
        },
    )

    class Meta:
        model = Team
        fields = ["name", "city", "discipline_name", "curator"]
        widgets = {
            "name": TextInput(
                attrs={"placeholder": "Введите название команды"},
            ),
            "staff_team_member": Select(),
            "discipline_name": Select(),
            "curator": Select(),
        }

    def save(self, commit=True):
        """Метод создает и сохраняет объект команды в базе данных."""
        instance = super(TeamForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class TeamFilterForm(forms.Form):
    """Форма для фильтрации команд."""

    name = forms.CharField(
        required=False,
        label="Команда",
        widget=forms.TextInput(attrs={"class": "form-control arrow-before"}),
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
    """Форма для игроков и команд."""

    def __init__(self, *args, **kwargs):
        """Метод инициализации экземпляра класса."""
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
    """Форма для сотрудников и команд."""

    def __init__(self, *args, **kwargs):
        """Метод инициализации экземпляра класса."""
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
    """Форма для сотрудников команд."""

    available_teams = ModelMultipleChoiceField(
        queryset=Team.objects.all().order_by("name"),
        required=False,
        help_text=FORM_HELP_TEXTS["available_teams"],
        label="Команды",
    )

    team = CustomMultipleChoiceField(
        required=True,
        help_text=FORM_HELP_TEXTS["staff_teams"],
        label="Команды",
    )

    class Meta:
        model = StaffTeamMember
        fields = (
            "available_teams",
            "team",
            "qualification",
            "notes",
        )
        help_texts = {
            "team": FORM_HELP_TEXTS["staff_teams"],
        }


class StaffTeamMemberEditForm(StaffTeamMemberForm):
    """Форма для обновления сотрудников команд."""

    def __init__(self, *args, **kwargs):
        """
        Метод инициализации экземпляра класса.

        Расширяет team и available_teams кастомными полями выбора.
        """
        super(StaffTeamMemberForm, self).__init__(*args, **kwargs)
        if queryset := self.instance.team.all():
            self.fields["team"] = CustomModelMultipleChoiceField(
                queryset=queryset,
                required=True,
                help_text=FORM_HELP_TEXTS["staff_teams"],
                label="Команды",
            )
        queryset_available = Team.objects.all().difference(queryset)
        self.fields["available_teams"] = CustomModelMultipleChoiceField(
            queryset=queryset_available,
            required=False,
            help_text=FORM_HELP_TEXTS["available_teams"],
            label="Команды",
        )


class StaffMemberForm(forms.ModelForm):
    """Форма для сотрудников."""

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
                attrs={"placeholder": "Введите фамилию"},
            ),
            "name": forms.TextInput(attrs={"placeholder": "Введите Имя"}),
            "patronymic": forms.TextInput(
                attrs={"placeholder": "Введите отчество"},
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "Введите номер телефона"},
            ),
        }


class StaffTeamMemberAddToTeamForm(forms.ModelForm):
    """Форма для добавления сотрудника в команду."""

    def __init__(self, position_filter: str | None = None, *args, **kwargs):
        """Метод инициализации экземпляра класса."""
        self.team = kwargs.pop("team")
        data_list_dict = {
            StaffPosition.TRAINER: "available_coaches",
            StaffPosition.OTHER: "available_pushers",
            "None": "available_staffs",
        }
        self.position_filter = position_filter or "None"
        self.data_list_id = data_list_dict[self.position_filter]
        super(StaffTeamMemberAddToTeamForm, self).__init__(*args, **kwargs)
        self.fields["staffteammember"] = StaffTeamMemberChoiceField(
            team=self.team,
            data_list=self.data_list_id,
        )

    class Meta:
        model = StaffTeamMember.team.through
        fields = ("staffteammember",)

    def save(self, commit=True):
        """Метод создает и сохраняет объект в базе данных."""
        instance = super(StaffTeamMemberAddToTeamForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
