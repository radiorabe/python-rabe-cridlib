"""Tests for nowplaying strategy."""

import cridlib
import cridlib.strategy.now


def test_get_show(klangbecken_mock):  # noqa: ARG001
    """Test get_data."""

    show = cridlib.strategy.now.get_show()
    assert show == "test"
