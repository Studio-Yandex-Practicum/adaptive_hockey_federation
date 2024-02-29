import unicodedata

from core.constants import ROLES_CHOICES
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.forms import Select
from django.utils.crypto import get_random_string
from main.models import Team
from users.utilits.reset_password import send_password_reset_email
from users.utils import set_team_curator

User = get_user_model()


class EmailField(forms.EmailField):
    def to_python(self, value):
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
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.through.objects.filter(
            user__in=self.cleaned_data["users"]
        ).delete()

        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        instance = super().save()
        self.save_m2m()
        return instance


class UserAdminForm(UserChangeForm):
    email = EmailField(label="Электронная почта", required=True)
    is_staff = forms.CharField(widget=forms.HiddenInput())
    is_superuser = forms.CharField(widget=forms.HiddenInput())

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        return user

    def clean(self):
        groups = self.cleaned_data["groups"]
        if groups.count() > 1:
            raise ValidationError("Выбрать можно только одну группу.")
        return super().clean()


class UserAdminCreationForm(UserCreationForm):
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
        super().__init__(*args, **kwargs)
        self.fields["password1"].required = False
        self.fields["password2"].required = False

    def save(self, commit=True):
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


class UsersCreationForm(forms.ModelForm):
    """Форма создания пользователя на странице users"""

    role = forms.ChoiceField(
        choices=ROLES_CHOICES[:-1],
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Роль пользователя",
        error_messages={"required": "Пожалуйста, выберите роль из списка."},
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Команда представителя",
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
        error_messages = {
            "email": {
                "unique": "Электронная почта должна быть уникальной!",
            },
        }
        widgets = {
            "role": Select(),
            "team": Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["patronymic"].required = False
        self.fields["role"].required = True
        self.fields["phone"].required = True

    def clean_team(self):
        """
        Проверка команды при создании пользователя
        """
        if choice_team := self.cleaned_data["team"]:
            choice_team = Team.objects.get(id=choice_team.id)
            if choice_team.curator is not None:
                raise ValidationError(
                    "У команды есть куратор!"
                    f"{choice_team.curator.get_full_name()}"
                )
        return choice_team

    def save(self, commit=True):
        user = super(UsersCreationForm, self).save(commit=False)
        set_team_curator(user, self.cleaned_data["team"])
        send_password_reset_email(user)
        return user


class UpdateUserForm(UsersCreationForm):
    """Форма редактирования пользователя"""

    def clean_team(self):
        """
        Проверка команды при редактировании пользователя
        """
        if choice_team := self.cleaned_data["team"]:
            choice_team = Team.objects.get(id=choice_team.id)
            current_team = self.instance.team.all()
            if current_team and current_team[0] == choice_team:
                return choice_team
            if choice_team.curator is not None:
                raise ValidationError(
                    "У команды есть куратор!"
                    f"{choice_team.curator.get_full_name()}"
                )
        return choice_team

    def save(self, commit=True):
        user = super(UsersCreationForm, self).save(commit=False)
        set_team_curator(user, self.cleaned_data["team"])
        if commit:
            user.save()
        return user
