"""djpress_admin URLs file."""

from django.urls import path

from djpress_admin.views import index, preview_markdown

app_name = "djpress_admin"

urlpatterns = [
    path("", index, name="index"),
    path("preview-markdown/", preview_markdown, name="preview_markdown"),
]
