"""djpress_admin views file."""

import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from djpress.utils import render_markdown

logger = logging.getLogger(__name__)


def index(
    request: HttpRequest,
) -> HttpResponse:
    """View for the index page."""
    if not request.user.is_authenticated:
        return redirect(f"{reverse('djpress:index')}")

    return render(
        request,
        "djpress_admin/index.html",
    )


def preview_markdown(request: HttpRequest) -> HttpResponse:
    """View for the preview markdown page."""
    if not request.user.is_authenticated:
        return redirect(f"{reverse('djpress:index')}")

    html = ""
    error = ""

    if request.method == "POST" and "content" in request.POST:
        try:
            html = render_markdown(request.POST["content"])
        except Exception as e:
            msg = f"Error rendering markdown: {e}"
            logger.exception(msg)
            error = msg

    return render(
        request,
        "djpress_admin/preview_markdown.html",
        {"html": html, "error": error},
    )
