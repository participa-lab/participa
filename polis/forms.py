from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Participant


class ParticipantForm(forms.ModelForm):
    CHOICES = [
        ("1", _("Participate anonymusly")),
        ("2", _("Login to Add Photo")),
    ]
    login = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        required=True,
    )

    class Meta:
        model = Participant
        fields = ["name", "gender", "year_of_birth", "territory", "affinity", "email"]
