"""Test high level cridlib API."""
from datetime import datetime
from unittest.mock import patch

from freezegun import freeze_time
from pytest import raises

import cridlib


def test_crid():
    """Test CRID class."""
    cridlib.setup()

    # basic minimal roundtrip
    with freeze_time("1993-03-01 13:12"):
        crid = cridlib.lib.CRID("crid://rabe.ch/v1/test#t=clock=19930301T131200.00Z")
    assert str(crid) == "crid://rabe.ch/v1/test#t=clock=19930301T131200.00Z"
    assert crid.version == "v1"
    assert crid.show == "test"
    assert crid.start == datetime(1993, 3, 1, 13, 12)

    # test for scheme mismatch
    with raises(cridlib.lib.CRIDSchemeMismatchError):
        cridlib.lib.CRID("https://rabe.ch/v1/test")

    # test for hostname mismatch
    with raises(cridlib.lib.CRIDSchemeHostMismatchError):
        cridlib.lib.CRID("crid://example.org/v1/test")

    # test for version mismatch
    with raises(cridlib.lib.CRIDUnsupportedVersionError):
        cridlib.lib.CRID("crid://rabe.ch/vX/test")

    # test for lack of fragments
    with raises(cridlib.lib.CRIDMissingMediaFragmentError):
        cridlib.lib.CRID("crid://rabe.ch/v1/test")


@patch("uri.scheme.URLScheme")
def test_setup(urlscheme_mock):
    """Test setup."""
    cridlib.setup()
    urlscheme_mock.assert_called_once_with("crid")
