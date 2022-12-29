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
    assert str(crid) == "crid://rabe.ch/v1/test#t=clock=19930301T131200.00Z"

    # show with additional local args in fragments
    with freeze_time("1993-03-02 00:00:00 UTC"):
        crid = cridlib.get(
            timestamp=datetime(1993, 3, 1, 13, 12, 00, tzinfo=timezone.utc),
            fragment="myid=1234",
        )
    assert crid.version == "v1"
    assert crid.show == "test"
    assert str(crid) == "crid://rabe.ch/v1/test#t=clock=19930301T131200.00Z&myid=1234"
