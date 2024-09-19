from django import forms
from django.utils.translation import gettext_lazy as _
from .choices import GENDER_CHOICES
from .models import Participant, Territory, Affinity


class ParticipantForm(forms.ModelForm):
    nick_name = forms.CharField(
        label=_("Tu apodo"),
        widget=forms.TextInput(attrs={"placeholder": _("Tu apodo")}),
    )
    gender = forms.ChoiceField(
        label=_("Tu género"),
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={"placeholder": _("Tu género")}),
    )
    year_of_birth = forms.CharField(
        label=_("Tu año de nacimiento"),
        widget=forms.TextInput(attrs={"placeholder": _("Tu año de nacimiento")}),
    )
    territory = forms.ModelChoiceField(
        queryset=Territory.objects.all(),
        label=_("Tu territorio"),
        widget=forms.Select(attrs={"placeholder": _("Tu territorio")}),
    )
    affinity = forms.ModelChoiceField(
        queryset=Affinity.objects.all(),
        label=_("Tu afiliación"),
        widget=forms.Select(attrs={"placeholder": _("Tu afiliación")}),
    )

    def clean(self):
        if not self.cleaned_data.get("year_of_birth"):
            self.add_error("year_of_birth", _("Este campo es requerido"))
        if not self.cleaned_data.get("nick_name"):
            self.add_error("nick_name", _("Este campo es requerido"))
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
    nick_name = forms.CharField(
        label=_("Tu apodo"),
        widget=forms.TextInput(attrs={"placeholder": _("Tu apodo")}),
    )
    gender = forms.ChoiceField(
        label=_("Tu género"),
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={"placeholder": _("Tu género")}),
    )
    year_of_birth = forms.CharField(
        label=_("Tu año de nacimiento"),
        widget=forms.TextInput(attrs={"placeholder": _("Tu año de nacimiento")}),
    )
    territory = forms.ModelChoiceField(
        queryset=Territory.objects.all(),
        label=_("Tu territorio"),
        widget=forms.Select(attrs={"placeholder": _("Tu territorio")}),
    )
    affinity = forms.ModelChoiceField(
        queryset=Affinity.objects.all(),
        label=_("Tu afiliación"),
        widget=forms.Select(attrs={"placeholder": _("Tu afiliación")}),
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
            "affinity",
        ]
