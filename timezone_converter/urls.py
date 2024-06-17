"""URLs for timezone_converter app."""

from django.urls import path

from timezone_converter.views import convert, converter

app_name = "timezone_converter"

urlpatterns = [
    path("", converter, name="converter"),
    path("convert/", convert, name="convert"),
]
