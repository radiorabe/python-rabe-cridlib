"""Low-level cridlib implemenetation bits."""

from datetime import datetime
from pathlib import PurePath
from typing import Optional
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


CRIDPath = PurePath


class CRID:
    """Represent CRIDs using uri."""

    def __init__(self, _uri=None) -> None:
        self._show: Optional[str] = None
        self._start: Optional[datetime] = None

        self._uri = urisplit(_uri)
        if self.scheme != "crid":
            raise CRIDSchemeMismatchError(self.scheme)
        if self.authority != "rabe.ch":
            raise CRIDSchemeAuthorityMismatchError(self.authority)
        # parent.stem contains version in /v1/foo paths, stem in generic root /v1 path
        if self.path.parent.stem != "v1" and self.path.stem != "v1":
            raise CRIDUnsupportedVersionError(self.path)
        self._version = self.path.parent.stem or self.path.stem
        # only store show if we have one
        if self.path.stem != "v1":
            self._show = self.path.relative_to(self.path.parent).stem
        # fragments are optional, but if provided we want them to contain t=code
        if self.fragment:
            try:
                self._start = datetime.strptime(
                    parse_qs(parse_qs(self.fragment)["t"][0])["clock"][0],
                    "%Y%m%dT%H%M%S.%fZ",
                )
            except KeyError as ex:
                raise CRIDMissingMediaFragmentError(self.fragment) from ex
            except ValueError as ex:  # pragma: no cover
                raise CRIDMalformedMediaFragmentError(self.fragment) from ex

    def __str__(self) -> str:
        return uricompose(*self._uri)

    def __repr__(self) -> str:
        """Pretty print CRID.

        >>> CRID("crid://rabe.ch/v1/test#t=clock=19930301T131200.00Z")
        <class 'cridlib.lib.CRID' for 'crid://rabe.ch/v1/test#t=clock=19930301T131200.00Z'>

        """
        _fqcn = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        return f"<class '{_fqcn}' for '{str(self)}'>"

    @property
    def scheme(self) -> str:
        """Get RaBe CRID scheme."""
        return self._uri.scheme

    @property
    def authority(self) -> str:
        """Get RaBe CRID authority."""
        return self._uri.authority

    @property
    def path(self) -> CRIDPath:
        """Get RaBe CRID path."""
        return CRIDPath(self._uri.path)

    @property
    def fragment(self) -> str:
        """Get RaBe CRID fragment."""
        return self._uri.fragment

    @property
    def version(self) -> str:
        """Get RaBe CRID version."""
        return self._version

    @property
    def show(self) -> Optional[str]:
        """Get RaBe CRID show."""
        return self._show

    @property
    def start(self) -> Optional[datetime]:
        """Get RaBe CRID start time."""
        return self._start
