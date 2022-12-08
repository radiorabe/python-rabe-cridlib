"""Test parse high-level api."""

import cridlib


def test_parse():
    """Test parse."""

    # hour zero case
    value = "crid://rabe.ch/v1/show#t=clock=19930301T131200.00Z"
    cridlib.parse(value)
