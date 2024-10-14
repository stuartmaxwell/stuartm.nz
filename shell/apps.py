"""This file contains the configuration of the shell app."""

from django.apps import AppConfig


class ShellConfig(AppConfig):
    """Configuration for the shell app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "shell"
