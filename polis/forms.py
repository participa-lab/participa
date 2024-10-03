from django import forms
from django.utils.translation import gettext_lazy as _
from .choices import GENDER_CHOICES
from .models import Participant, Territory


class ParticipantForm(forms.ModelForm):
    nick_name = forms.CharField(
        label=_("Tu apodo"),
        widget=forms.TextInput(attrs={"placeholder": _("Tu apodo")}),
    )
    gender = forms.ChoiceField(
        label=_("Tu género"),
        choices=[("", _("Seleccionar"))] + GENDER_CHOICES,
        widget=forms.Select(attrs={"placeholder": _("Tu género")}),
    )
    year_of_birth = forms.CharField(
        label=_("Año Nacimiento"),
        widget=forms.TextInput(attrs={"placeholder": _("Tu año de nacimiento")}),
    )
    territory = forms.ModelChoiceField(
        queryset=Territory.objects.all(),
        label=_("Tu territorio"),
        empty_label=_("Seleccionar"),
        widget=forms.Select(attrs={"placeholder": _("Tu territorio")}),
        required=False,
    )

    def clean(self):
        if not self.cleaned_data.get("year_of_birth"):
            self.add_error("year_of_birth", _("Este campo es requerido"))
        if not self.cleaned_data.get("nick_name"):
            self.add_error("nick_name", _("Este campo es requerido"))
        if not self.cleaned_data.get("gender"):
            self.add_error("gender", _("Este campo es requerido"))
        return super().clean()

    class Meta:
        model = Participant
        fields = [
            "nick_name",
            "gender",
            "year_of_birth",
            "territory",
        ]


class ContactForm(forms.Form):
    name = forms.CharField(label=_("Tu nombre y apellido"))
    email = forms.EmailField(label=_("Email"))
    subject = forms.CharField(label=_("Asunto"), max_length=150)
    message = forms.CharField(
        label=_("Tu mensaje"), widget=forms.Textarea, max_length=300
    )
