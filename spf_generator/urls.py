"""URLs for markdown_editor app."""

from django.urls import path

from spf_generator.views import generate_spf_record

app_name = "spf_generator"

urlpatterns = [
    path("", generate_spf_record, name="spf_generator"),
]
