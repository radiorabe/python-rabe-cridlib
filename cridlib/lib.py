"""Low-level cridlib implemenetation bits."""

from datetime import datetime
from pathlib import PurePath
from urllib.parse import parse_qs

from uritools import uricompose, urisplit  # type: ignore


class CRIDError(Exception):
    """Represent all cridlib errors."""


class CRIDSchemeMismatchError(CRIDError):
    """Scheme in URI does not match 'crid'."""


class CRIDSchemeAuthorityMismatchError(CRIDError):
    """Hostname part of URI does not match 'rabe.ch'."""


class CRIDUnsupportedVersionError(CRIDError):
    """Unsupported version in path of URI."""


class CRIDMissingMediaFragmentError(CRIDError):
    """Missing media-fragment with clock code."""


class CRIDMalformedMediaFragmentError(CRIDError):
    """Missing media-fragment with clock code."""


class CRID:
    """Represent CRIDs using uri."""

    def __init__(self, _uri=None) -> None:
        self._uri = urisplit(_uri)
        if self.scheme != "crid":
            raise CRIDSchemeMismatchError(self.scheme)
        if self.authority != "rabe.ch":
            raise CRIDSchemeAuthorityMismatchError(self.authority)
        if self.path.parent.stem != "v1":
            raise CRIDUnsupportedVersionError(self.path)
        self._version = self.path.parent.stem
        self._show = self.path.relative_to(self.path.parent).stem
        try:
            self._start = datetime.strptime(
                parse_qs(parse_qs(self.fragment)["t"][0])["clock"][0],
                "%Y%m%dT%H%M%S.%fZ",
            )
        except KeyError as ex:
            raise CRIDMissingMediaFragmentError(self.fragment) from ex
        except ValueError as ex:  # pragma: no cover
            raise CRIDMalformedMediaFragmentError(self.fragment) from ex

    def __str__(self):
        return uricompose(*self._uri)

    def __repr__(self):  # pragma: no cover
        return f"{self.__class__}: {str(self)}"

    @property
    def scheme(self):
        """Get RaBe CRID scheme."""
        return self._uri.scheme

    @property
    def authority(self):
        """Get RaBe CRID authority."""
        return self._uri.authority

    @property
    def path(self):
        """Get RaBe CRID path."""
        return PurePath(self._uri.path)

    @property
    def fragment(self):
        """Get RaBe CRID fragment."""
        return self._uri.fragment

    @property
    def version(self):
        """Get RaBe CRID version."""
        return self._version

    @property
    def show(self):
        """Get RaBe CRID show."""
        return self._show

    @property
    def start(self):
        """Get RaBe CRID start time."""
        return self._start
