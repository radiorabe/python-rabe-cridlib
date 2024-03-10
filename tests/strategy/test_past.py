"""Tests for nowplaying strategy."""

from datetime import datetime

from freezegun import freeze_time

import cridlib
import cridlib.strategy.past


def test_get_show(archiv_mock):  # noqa: ARG001
    """Test get_data."""

    with freeze_time("1993-03-01 13:12:00 UTC"):
        show = cridlib.strategy.past.get_show(datetime.now())  # noqa: DTZ005
    assert show == "test"


def test_get_show_empty(empty_archiv_mock):  # noqa: ARG001
    """Test get_data."""

    with freeze_time("1993-03-01 13:12:00 UTC"):
        show = cridlib.strategy.past.get_show(datetime.now())  # noqa: DTZ005
    assert show == ""
