from django import forms
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


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class TeamForm(forms.ModelForm):
    curator = UserChoiceField(
        queryset=User.objects.all(),
        label='Куратор',
        help_text='Куратор команды',
    )

    # class Meta:
    #     model = Team
    #     fields = [
    #         'name',
    #         'city',
    #         'staff_team_member',
    #         'discipline_name',
    #         'curator'
    #     ]
