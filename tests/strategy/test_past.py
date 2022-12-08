"""Tests for nowplaying strategy."""

from datetime import datetime

from freezegun import freeze_time

import cridlib
import cridlib.strategy.past


def test_get_show(archiv_mock):  # pylint: disable=unused-argument
    """Test get_data."""

    with freeze_time("1993-03-01 13:12:00"):
        show = cridlib.strategy.past.get_show(datetime.now())
    assert show == "test"
