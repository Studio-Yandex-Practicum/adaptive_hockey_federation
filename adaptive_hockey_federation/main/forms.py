from django import forms
from main.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
            'city',
            'staff_team_member',
            'discipline_name',
            'curator'
        ]
