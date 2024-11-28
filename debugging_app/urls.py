"""URLs for debugging app."""

from django.conf import settings
from django.urls import path

from debugging_app.views import debugging_app

app_name = "debugging_app"

urlpatterns = [
    path(settings.DEBUGGING_APP_PATH, debugging_app, name="debugging_app"),
]
