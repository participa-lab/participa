from django import forms

from .models import Participant


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "gender", "year_of_birth", "territory", "affinity"]
