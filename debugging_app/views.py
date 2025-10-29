"""Views for the debugging_app app."""

from typing import TYPE_CHECKING

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def debugging_app(request: HttpRequest) -> HttpResponse:
    """View function for the debugging page."""
    context = {"meta": request.META}
    return render(request, "debugging_app/debugging.html", context)
