from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Participant


class ParticipantForm(forms.ModelForm):
    def clean(self):
        if not self.cleaned_data.get("year_of_birth"):
            self.add_error("year_of_birth", _("This field is required"))
        if not self.cleaned_data.get("nick_name"):
            self.add_error("nick_name", _("This field is required"))
        if not self.cleaned_data.get("gender"):
            self.add_error("gender", _("This field is required"))
        return super().clean()

    class Meta:
        model = Participant
        fields = [
            "nick_name",
            "gender",
            "year_of_birth",
            "territory",
            "affinity",
        ]


class ParticipantUpdateForm(forms.ModelForm):
    def clean(self):
        if not self.cleaned_data.get("year_of_birth"):
            self.add_error("year_of_birth", _("This field is required"))
        if not self.cleaned_data.get("nick_name"):
            self.add_error("nick_name", _("This field is required"))
        if not self.cleaned_data.get("gender"):
            self.add_error("gender", _("This field is required"))
        return super().clean()

    class Meta:
        model = Participant
        fields = [
            "nick_name",
            "gender",
            "year_of_birth",
            "territory",
            "affinity",
        ]
