from django.utils.translation import gettext_lazy as _

GENDER_CHOICES = [
    ("F", _("Female")),
    ("M", _("Male")),
    ("NB", _("Non-Binary")),
    ("TG", _("Transgender")),
    ("I", _("Intersex")),
    ("Q", _("Queer")),
    ("N", _("Prefer Not to Say")),
    ("O", _("Other")),
]

SUSCRIBE_CHOICES = [
    ("1", _("Email")),
]
