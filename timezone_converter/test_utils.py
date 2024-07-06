import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
from .utils import convert_timestamp_to_timezone


@pytest.mark.parametrize(
    "timestamp, timezone, expected",
    [
        (
            "2024-01-01T00:00:00Z",
            "America/New_York",
            datetime(2023, 12, 31, 19, 0, 0, tzinfo=ZoneInfo("America/New_York")),
        ),
        (
            "2024-01-01T00:00:00Z",
            "Europe/London",
            datetime(2024, 1, 1, 0, 0, 0, tzinfo=ZoneInfo("Europe/London")),
        ),
        (
            "2024-01-01T00:00:00Z",
            "Asia/Tokyo",
            datetime(2024, 1, 1, 9, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
        ),
        (
            "2024-01-01T00:00:00Z",
            "Pacific/Auckland",
            datetime(2024, 1, 1, 13, 0, 0, tzinfo=ZoneInfo("Pacific/Auckland")),
        ),
    ],
)
def test_convert_timestamp_to_timezone(timestamp, timezone, expected):
    result = convert_timestamp_to_timezone(timestamp, timezone)
    assert result == expected
