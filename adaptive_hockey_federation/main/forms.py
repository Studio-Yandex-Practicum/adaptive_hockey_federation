from django import forms
from django.forms import ModelChoiceField, Select, TextInput
from main.models import City, DisciplineName, StaffTeamMember, Team
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


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields[
            'curator'
        ].label_from_instance = lambda obj: obj.get_full_name()

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=Select(attrs={'class': 'form-control'}),
        required=True,
        error_messages={
            'required': 'Пожалуйста, выберите город из списка.'
        },
        label='Город откуда команда',
        empty_label='Выберите название города'
    )
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
            'city': Select(),
            'staff_team_member': Select(),
            'discipline_name': Select(),
            'curator': Select(),
        }

        def save(self, commit=True):
            instance = super(TeamForm, self).save(commit=False)
            if commit:
                instance.save()
            return instance
