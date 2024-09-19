from django.utils.translation import gettext_lazy as _

GENDER_CHOICES = [
    ("F", _("Mujer")),
    ("M", _("Varón")),
    ("NB", _("No binario")),
    ("TG", _("Trans")),
    ("I", _("Intersexual")),
    ("Q", _("Queer")),
    ("N", _("Prefiero no decirlo")),
    ("O", _("Otro")),
]

SUSCRIBE_CHOICES = [
    ("1", _("Email")),
]
