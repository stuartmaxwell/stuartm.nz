"""Views for the timezone_converter app."""

from datetime import datetime
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


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
    # pyrefly: ignore [bad-assignment]
    timestamp: str | None = request.POST.get("timestamp")
    # pyrefly: ignore [bad-assignment]
    timezone: str | None = request.POST.get("timezone")

    error_message: str = ""

    if not timezone or not timestamp:
        error_message = "Please provide a timestamp and timezone."
        return render(
            request,
            "timezone_converter/converted.html",
            {"error_message": error_message},
        )

    # Convert the timestamp to a datetime object.
    try:
        datetime_obj: datetime = datetime.fromisoformat(timestamp)
    except ValueError:
        error_message = "Invalid timestamp. Please use the ISO 8601 format."
        return render(
            request,
            "timezone_converter/converted.html",
            {"error_message": error_message},
        )

    # Check the converted timestamp is timezone aware
    if datetime_obj.tzinfo is None:
        error_message = (
            "The timestamp provided must be timezone aware. For example, use 'Z' for UTC, or provide an offset."
        )
        return render(
            request,
            "timezone_converter/converted.html",
            {"error_message": error_message},
        )

    # Check that the timezone is valid.
    try:
        ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        error_message = "Invalid timezone. Please use a valid timezone."
        return render(
            request,
            "timezone_converter/converted.html",
            {"error_message": error_message},
        )

    return render(
        request,
        "timezone_converter/converted.html",
        {"timestamp": datetime_obj, "timezone": timezone},
    )
