import unicodedata

from core.constants import FORM_HELP_TEXTS
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from main.models import Team

User = get_user_model()


class EmailField(forms.EmailField):
    """Класс для расширения поля email."""

    def to_python(self, value):
        """Преобразовать значение в знакомый для Python объект."""
        value = super().to_python(value)
        return None if value is None else unicodedata.normalize("NFKC", value)


class GroupAdminForm(forms.ModelForm):
    """Дополнительное поле "Пользователи" для групп."""

    class Meta:
        model = Group
        fields = ["name", "users", "permissions"]

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("пользователи", False),
        label="Пользователи",
    )

    def __init__(self, *args, **kwargs):
        """Метод инициализации экземпляра класса."""
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):
        """Метод устанавливает M2M связи между группой и пользователями."""
        self.instance.user_set.through.objects.filter(
            user__in=self.cleaned_data["users"],
        ).delete()

        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        """Метод создает и сохраняет объект в базе данных."""
        instance = super().save()
        self.save_m2m()
        return instance


class UserAdminForm(UserChangeForm):
    """Форма для обновления пользователя через админку."""

    email = EmailField(label="Электронная почта", required=True)
    is_staff = forms.CharField(widget=forms.HiddenInput())
    is_superuser = forms.CharField(widget=forms.HiddenInput())

    def save(self, commit=True):
        """Метод создает и сохраняет объект в базе данных."""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        return user

    def clean(self):
        """Метод для валидации данных полей формы."""
        groups = self.cleaned_data["groups"]
        if groups.count() > 1:
            raise ValidationError("Выбрать можно только одну группу.")
        return super().clean()


class UserAdminCreationForm(UserCreationForm):
    """Форма для создания пользователя через админку."""

    email = forms.EmailField(
        label="Email",
        help_text=(
            "Обязательное поле. На данную почту пользователю "
            "будет выслана ссылка для смены и восстановления пароля."
        ),
        required=True,
    )
    first_name = forms.CharField(label="Имя", help_text="Обязательное поле")
    last_name = forms.CharField(label="Фамилия", help_text="Обязательное поле")

    def __init__(self, *args, **kwargs):
        """Метод инициализации экземпляра класса."""
        super().__init__(*args, **kwargs)
        self.fields["password1"].required = False
        self.fields["password2"].required = False

    def save(self, commit=True):
        """Метод создает и сохраняет объект в базе данных."""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(get_random_string(length=8))
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )
        error_messages = {
            "email": {
                "unique": "Электронная почта должна быть уникальной!",
            },
        }


class CustomUserCreateForm(forms.ModelForm):
    """Форма для создания пользователя."""

    team = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        required=False,
        label="Команды",
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "phone",
            "role",
            "team",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "Введите фамилию (обязательно)"},
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Введите Имя (обязательно)"},
            ),
            "patronymic": forms.TextInput(
                attrs={"placeholder": "Введите отчество"},
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Введите email (обязательно)"},
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "Введите номер игрока"},
            ),
        }
        help_texts = {
            "email": FORM_HELP_TEXTS["email"],
            "role": FORM_HELP_TEXTS["role"],
        }

    def clean_team(self):
        """Проверка команды при создании пользователя."""
        busy_teams = None
        choice_team = None
        if choice_team := self.cleaned_data["team"]:
            busy_teams = [
                team for team in choice_team if team.curator is not None
            ]
            if len(busy_teams) > 0:
                message = [
                    f"У команды {team.name} уже есть куратор {team.curator}"
                    for team in busy_teams
                ]
                raise ValidationError(message)
        return choice_team


class CustomUserUpdateForm(CustomUserCreateForm):
    """Форма для обновления пользователя."""

    def __init__(self, *args, **kwargs):
        """Метод инициализации экземпляра класса."""
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)
        if self.instance.team.all():
            self.fields["team"].initial = self.instance.team.all()

    def clean_team(self):
        """Проверка команды при создании пользователя."""
        busy_teams = None
        choice_teams = None
        current_teams = list(self.instance.team.all())
        if choice_teams := self.cleaned_data["team"]:
            busy_teams = [
                team for team in choice_teams if team.curator is not None
            ]
            if len(current_teams) > 0:
                busy_teams = list(set(busy_teams) - set(current_teams))
            if len(busy_teams) > 0:
                message = [
                    f"У команды {team.name} уже есть куратор {team.curator}"
                    for team in busy_teams
                ]
                raise ValidationError(message)
        return choice_teams
