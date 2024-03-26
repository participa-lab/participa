from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Participant


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "gender", "year_of_birth", "territory", "affinity", "email"]

    labels = {
        "name": _("Name"),
        "gender": _("Gender"),
        "year_of_birth": _("Year of birth"),
        "territory": _("Territory"),
        "affinity": _("Affinity"),
        "email": _("Email"),
    }
