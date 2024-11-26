"""Views for the home app."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_view(request: HttpRequest) -> HttpResponse:
    """View function for the home page."""
    return render(request, "home/home.html")
