"""URLs for contact form app."""

from django.urls import path

from contact_form.views import contact_form

app_name = "contact_form"

urlpatterns = [
    path("", contact_form, name="contact_form"),
]
