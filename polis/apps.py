from django.apps import AppConfig


class PolisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "polis"

    def ready(self):
        import polis.signals

        print(polis.signals.__name__)
