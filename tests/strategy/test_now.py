"""Tests for nowplaying strategy."""

import cridlib
import cridlib.strategy.now


def test_get_show(klangbecken_mock):  # pylint: disable=unused-argument
    """Test get_data."""

    show = cridlib.strategy.now.get_show()
    assert show == "test"
