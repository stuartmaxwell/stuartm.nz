"""djpress_admin views file."""

import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

logger = logging.getLogger(__name__)


def markdown_previewer(
    request: HttpRequest,
) -> HttpResponse:
    """View for the index page."""
    if not request.user.is_authenticated:
        return redirect(f"{reverse('djpress:index')}")

    return render(
        request,
        "djpress_admin/markdown_previewer.html",
    )
