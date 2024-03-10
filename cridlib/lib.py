"""Main Cridlib library."""

from __future__ import annotations

from datetime import datetime
from pathlib import PurePath
from typing import Self
from urllib.parse import parse_qs

from slugify import slugify
from uritools import uricompose, urisplit  # type: ignore[import-untyped]


def canonicalize_show(show: str) -> str:
    """Get the slug for a show.

    Uses [python-slugify](https://github.com/un33k/python-slugify).

    Args:
    ----
        show: Name of show with non-ascii chars.

    Returns:
    -------
        slugified show name.

    """
    return slugify(show)


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
    """Represent CRIDs and can parse, validate and render them.

    Examples
    --------
        Generate a CRID from an URL and render it's repr:
        ```python
        >>> CRID("crid://rabe.ch/v1/test#t=clock=19930301T131200.00Z")
        <class 'cridlib.lib.CRID' for 'crid://rabe.ch/v1/test#t=clock=19930301T131200.00Z'>

        ```

        Generate a CRID and render it as str:
        ```python
        >>> str(CRID("crid://rabe.ch/v1/test#t=clock=19930301T131200.00Z"))
        'crid://rabe.ch/v1/test#t=clock=19930301T131200.00Z'

        ```

    """

    def __init__(self: Self, uri: str | None = None) -> None:
        """Create new CRID.

        Args:
        ----
            uri: CRID URL to base the new CRID off of.

        """
        self._show: str | None = None
        self._start: datetime | None = None

        self._uri = urisplit(uri)
        if self.scheme != "crid":
            raise CRIDSchemeMismatchError(self.scheme, uri)
        if self.authority != "rabe.ch":
            raise CRIDSchemeAuthorityMismatchError(self.authority, uri)
        # parent.stem contains version in /v1/foo paths, stem in generic root /v1 path
        if self.path.parent.stem != "v1" and self.path.stem != "v1":
            raise CRIDUnsupportedVersionError(self.path, uri)
        self._version = self.path.parent.stem or self.path.stem
        # only store show if we have one
        if self.path.stem != "v1":
            self._show = self.path.relative_to(self.path.parent).stem
        # fragments are optional, but if provided we want them to contain t=code
        if self.fragment:
            try:
                # TODO(hairmare): investigate noqa for bug
                # https://github.com/radiorabe/python-rabe-cridlib/issues/244
                self._start = datetime.strptime(  # noqa: DTZ007
                    parse_qs(parse_qs(self.fragment)["t"][0])["clock"][0],
                    "%Y%m%dT%H%M%S.%fZ",
                )
            except KeyError as ex:
                raise CRIDMissingMediaFragmentError(self.fragment, uri) from ex
            except ValueError as ex:  # pragma: no cover
                raise CRIDMalformedMediaFragmentError(self.fragment, uri) from ex

    def __str__(self: Self) -> str:
        """Stringfy.

        Returns
        -------
            CRID URL rendered as string.

        """
        return uricompose(*self._uri)

    def __repr__(self: Self) -> str:
        """Repr."""
        _fqcn = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        return f"<class '{_fqcn}' for '{self!s}'>"

    @property
    def scheme(self: Self) -> str:
        """Scheme.

        Returns
        -------
            Scheme part of the CRID.

        """
        return self._uri.scheme

    @property
    def authority(self: Self) -> str:
        """Authority.

        Returns
        -------
            Authority part (aka hostname) of CRID.

        """
        return self._uri.authority

    @property
    def path(self: Self) -> CRIDPath:
        """Path.

        Returns
        -------
            Path part of CRID.

        """
        return CRIDPath(self._uri.path)

    @property
    def fragment(self: Self) -> str:
        """Fragment.

        Returns
        -------
            Fragment part of CRID.

        """
        return self._uri.fragment

    @property
    def version(self: Self) -> str:
        """Version.

        Returns
        -------
            Version from CRIDs path.

        """
        return self._version

    @property
    def show(self: Self) -> str | None:
        """Slug.

        Returns
        -------
            Show slug from CRIDs path.

        """
        return self._show

    @property
    def start(self: Self) -> datetime | None:
        """Start time.

        Returns
        -------
            Start time form CRIDs media fragment.

        """
        return self._start
