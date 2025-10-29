"""App configuration for Home app."""

from django.apps import AppConfig


class HomeConfig(AppConfig):
    """Home app configuration."""

    # pyrefly: ignore [bad-override]
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"
