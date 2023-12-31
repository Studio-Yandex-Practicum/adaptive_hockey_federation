import unicodedata

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

User = get_user_model()


class EmailField(forms.EmailField):
    def to_python(self, value):
        value = super().to_python(value)
        return None if value is None else unicodedata.normalize("NFKC", value)


class CreateUserForm(forms.ModelForm):
    """Форма создания юзера"""

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'patronymic',
            'email',
            'phone',
        ]


class UpdateUserForm(CreateUserForm):
    """Форма редактирования пользователя"""


class GroupAdminForm(forms.ModelForm):
    """Дополнительное поле "Пользователи" для групп."""

    class Meta:
        model = Group
        exclude = []

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
            user__in=self.cleaned_data["users"]).delete()

        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        instance = super().save()
        self.save_m2m()
        return instance


class UserAdminForm(UserChangeForm):
    email = EmailField(label="Электронная почта", required=True)
    password = forms.CharField(widget=forms.HiddenInput())
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
