"""Views for the timezone_converter app."""

from typing import TYPE_CHECKING

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from timezone_converter.utils import convert_timestamp_to_timezone

if TYPE_CHECKING:
    from datetime import datetime


# A simple view to display the converter HTML template.
def converter(request: HttpRequest) -> HttpResponse:
    """Display the converter HTML template."""
    return render(
        request,
        "timezone_converter/converter.html",
    )


# A view to receive a timestamp and timezone POSTed from the converter form and return
# the converted time using a template.
def convert(request: HttpRequest) -> HttpResponse:
    """Convert a timestamp to a different timezone and display the result."""
    # Get the timestamp and timezone from the POST request.
    timestamp: str | None = request.POST.get("timestamp")
    timezone: str | None = request.POST.get("timezone")

    error_message: str = ""

    if not timezone or not timestamp:
        error_message = "Please provide a timestamp and timezone."
        return render(
            request,
            "timezone_converter/converted.html",
            {"error_message": error_message},
        )

    try:
        # Convert the timestamp to the given timezone.
        converted_time: datetime = convert_timestamp_to_timezone(timestamp, timezone)
    except ValueError as exc:
        error_message = str(exc)
        return render(
            request,
            "timezone_converter/converted.html",
            {"error_message": error_message},
        )

    return render(
        request,
        "timezone_converter/converted.html",
        {"converted_time": converted_time, "error_message": error_message},
    )
