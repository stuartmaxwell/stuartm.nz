"""App configuration for the SPF Generator app."""

from django.apps import AppConfig


class SpfGeneratorConfig(AppConfig):
    """App configuration for the SPF Generator app."""

    # pyrefly: ignore [bad-override]
    default_auto_field = "django.db.models.BigAutoField"
    name = "spf_generator"
