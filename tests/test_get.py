"""Tests for high-level get API."""

from datetime import datetime, timezone

from freezegun import freeze_time

import cridlib


def test_get_now(klangbecken_mock):  # pylint: disable=unused-argument
    """Test meth:`get` for currently running show."""
    crid = cridlib.get()
    assert crid.version == "v1"
    assert crid.show == "test"


def test_get_past(archiv_mock):  # pylint: disable=unused-argument
    """Test meth:`get` for past shows."""
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


def test_get_future(libretime_mock):  # pylint: disable=unused-argument
    """Test meth:`get` for future shows."""
    with freeze_time("1993-03-01 00:00:00 UTC"):
        crid = cridlib.get(
            timestamp=datetime(1993, 3, 1, 11, 15, 00, tzinfo=timezone.utc),
        )
    assert crid.version == "v1"
    assert crid.show == "info"
    assert str(crid) == "crid://rabe.ch/v1/info#t=clock=19930301T111500.00Z"

    # for now we only read show info from libretime for the next week
    with freeze_time("1993-03-01 00:00:00 UTC"):
        crid = cridlib.get(
            timestamp=datetime(1993, 3, 8, 13, 12, 00, tzinfo=timezone.utc),
        )
    assert crid.show is None
    assert str(crid) == "crid://rabe.ch/v1#t=clock=19930308T131200.00Z"
