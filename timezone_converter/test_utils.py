import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
from utils import convert_timestamp_to_timezone


@pytest.mark.parametrize(
    "timestamp, timezone, expected",
    [
        (
            "2022-01-01T00:00:00",
            "America/New_York",
            datetime(2021, 12, 31, 19, 0, 0, tzinfo=ZoneInfo("America/New_York")),
        ),
        (
            "2022-01-01T00:00:00",
            "Europe/London",
            datetime(2022, 1, 1, 5, 0, 0, tzinfo=ZoneInfo("Europe/London")),
        ),
        (
            "2022-01-01T00:00:00",
            "Asia/Tokyo",
            datetime(2022, 1, 1, 9, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
        ),
    ],
)
def test_convert_timestamp_to_timezone(timestamp, timezone, expected):
    result = convert_timestamp_to_timezone(timestamp, timezone)
    assert result == expected
