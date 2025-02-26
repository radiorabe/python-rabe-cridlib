"""Test high level cridlib API."""

from datetime import UTC, datetime

import pytest
from freezegun import freeze_time

import cridlib


@pytest.mark.parametrize(
    ("crid_str", "expected"),
    [
        (
            "crid://rabe.ch/v1/test#t=clock=19930301T131200.00Z",
            {
                "version": "v1",
                "show": "test",
                "start": datetime(1993, 3, 1, 12, 12, tzinfo=UTC),
            },
        ),
        (
            "crid://rabe.ch/v1",
            {
                "version": "v1",
                "show": None,
                "start": None,
            },
        ),
        (
            "crid://rabe.ch/v1#t=clock=19930301T131200.00Z",
            {
                "version": "v1",
                "show": None,
                "start": datetime(1993, 3, 1, 12, 12, tzinfo=UTC),
            },
        ),
    ],
)
def test_crid_roundtrip(crid_str, expected):
    with freeze_time("1993-03-01 12:12 UTC"):
        crid = cridlib.lib.CRID(crid_str)
    assert str(crid) == crid_str
    assert crid.version == expected["version"]
    assert crid.show == expected["show"]
    assert crid.start == expected["start"]


def test_crid_scheme_mismatch():
    with pytest.raises(cridlib.lib.CRIDSchemeMismatchError):
        cridlib.lib.CRID("https://rabe.ch/v1/test")


def test_crid_hostname_mismatch():
    with pytest.raises(cridlib.lib.CRIDSchemeAuthorityMismatchError):
        cridlib.lib.CRID("crid://example.org/v1/test")


def test_crid_version_mismatch():
    with pytest.raises(cridlib.lib.CRIDUnsupportedVersionError):
        cridlib.lib.CRID("crid://rabe.ch/vX/test")


def test_crid_missing_media_fragment():
    with pytest.raises(cridlib.lib.CRIDMissingMediaFragmentError):
        cridlib.lib.CRID("crid://rabe.ch/v1/test#t=wrong=10")


@pytest.mark.parametrize(
    ("show", "expected"),
    [
        ("à suivre #42", "a-suivre-42"),
    ],
)
def test_canonicalize_show(show, expected):
    assert expected == cridlib.lib.canonicalize_show(show)
