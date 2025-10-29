"""Views for the home app."""

from typing import TYPE_CHECKING

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home_view(request: HttpRequest) -> HttpResponse:
    """View function for the home page."""
    return render(request, "home/home.html")
