"""Tests for high-level get API."""

from datetime import datetime, timezone

from freezegun import freeze_time

import cridlib


def test_get(klangbecken_mock, archiv_mock):  # pylint: disable=unused-argument
    """Test get."""

    # current show
    crid = cridlib.get()
    assert crid.version == "v1"
    assert crid.show == "test"

    # past show
    with freeze_time("1993-03-02 00:00:00 UTC"):
        crid = cridlib.get(
            timestamp=datetime(1993, 3, 1, 13, 12, 00, tzinfo=timezone.utc)
        )
    assert crid.version == "v1"
    assert crid.show == "test"
