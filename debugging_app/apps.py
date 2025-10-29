"""App configuration for debugging_app."""

from django.apps import AppConfig


class DebuggingAppConfig(AppConfig):
    """App configuration."""

    # pyrefly: ignore [bad-override]
    default_auto_field = "django.db.models.BigAutoField"
    name = "debugging_app"
