"""URLs for markdown_editor app."""

from django.urls import path

from contact_form.views import contact_form
from spf_generator.views import generate_spf_record

app_name = "spf_generator"

urlpatterns = [
    path("contact/", contact_form, {"contact_form_title": "Request a New SPF Record"}, name="contact_form"),
    path("", generate_spf_record, name="spf_generator"),
]
