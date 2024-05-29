"""djpress_admin URLs file."""

from django.urls import path

from djpress_admin.views import markdown_previewer

app_name = "djpress_admin"

urlpatterns = [
    path("", markdown_previewer, name="markdown_previewer"),
]
