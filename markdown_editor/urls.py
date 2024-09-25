"""URLs for markdown_editor app."""

from django.urls import path

from markdown_editor.views import markdown_editor

app_name = "markdown_editor"

urlpatterns = [
    path("", markdown_editor, name="markdown_editor"),
]
