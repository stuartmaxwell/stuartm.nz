"""Utility functions for the timezone_converter app."""

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def convert_timestamp_to_timezone(timestamp: str, timezone: str) -> datetime:
    """Convert a timestamp to a different timezone.

    Args:
        timestamp: The timestamp to convert. This must be in ISO 8601 format.
        timezone: The timezone to convert the timestamp to.

    Returns:
        The converted timestamp.
    """
    # Convert the timestamp to a datetime object.
    try:
        datetime_obj: datetime = datetime.fromisoformat(timestamp)
    except ValueError as exc:
        msg = "Invalid timestamp. Please use the ISO 8601 format."
        raise ValueError(msg) from exc

    # Check that the timezone is valid.
    try:
        tz = ZoneInfo(timezone)
    except ZoneInfoNotFoundError as exc:
        msg = "Invalid timezone. Please use a valid timezone."
        raise ValueError(msg) from exc

    # Convert the datetime object to the given timezone.
    return datetime_obj.astimezone(tz)
