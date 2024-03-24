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


class CustomUserCreateForm(forms.ModelForm):

    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=False,
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
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "Введите фамилию (обязательно)"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Введите Имя (обязательно)"}
            ),
            "patronymic": forms.TextInput(
                attrs={"placeholder": "Введите отчество"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Введите email (обязательно)"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "Введите номер игрока"}
            ),
        }
        help_texts = {
            "email": FORM_HELP_TEXTS["email"],
            "role": FORM_HELP_TEXTS["role"],
        }

    def clean_team(self):
        """
        Проверка команды при создании пользователя
        """
        if choice_team := self.cleaned_data["team"]:
            if choice_team.curator is not None:
                raise ValidationError(
                    "У команды есть куратор!"
                    f"{choice_team.curator.get_full_name()}"
                )
        return choice_team


class CustomUserUpdateForm(CustomUserCreateForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)
        if team := self.instance.team.all():
            self.fields["team"].initial = team[0]

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
