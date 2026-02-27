"""Tests for the future show strategy."""

from datetime import datetime, timezone

from freezegun import freeze_time

import cridlib.strategy.future


def test_get_show(libretime_mock):  # noqa: ARG001
    """Test that the correct future show is returned for a given timestamp."""
    with freeze_time("1993-03-01 00:00:00 UTC"):
        show = cridlib.strategy.future.get_show(
            future=datetime(1993, 3, 1, 11, 15, 0, tzinfo=timezone.utc),
        )
    assert show == "info"


def test_get_show_no_match(libretime_mock):  # noqa: ARG001
    """Test that an empty string is returned when no show matches the timestamp."""
    with freeze_time("1993-03-01 00:00:00 UTC"):
        show = cridlib.strategy.future.get_show(
            future=datetime(1993, 3, 8, 13, 12, 0, tzinfo=timezone.utc),
        )
    assert show == ""
