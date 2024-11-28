"""Views for the debugging_app app."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def debugging_app(request: HttpRequest) -> HttpResponse:
    """View function for the debugging page."""
    context = {"meta": request.META}
    return render(request, "debugging_app/debugging.html", context)
