"""Views for the markdown_editor app."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# A simple view to display the converter HTML template.
def markdown_editor(request: HttpRequest) -> HttpResponse:
    """Display the Markdown Editor template."""
    return render(
        request,
        "markdown_editor/markdown_editor.html",
    )
