"""Views for the markdown_editor app."""

from typing import TYPE_CHECKING

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


# A simple view to display the converter HTML template.
def markdown_editor(request: HttpRequest) -> HttpResponse:
    """Display the Markdown Editor template."""
    return render(
        request,
        "markdown_editor/markdown_editor.html",
    )
