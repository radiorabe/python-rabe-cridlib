from datetime import datetime
from pathlib import PurePath
from typing import Optional
from urllib.parse import parse_qs

from slugify import slugify
from uritools import uricompose, urisplit  # type: ignore


def canonicalize_show(show: str) -> str:
    """Get the slug for a show.

    Uses [python-slugify](https://github.com/un33k/python-slugify).

    Parameters:
        show: Name of show with non-ascii chars.
    Returns:
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

    Examples:
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
    """  # noqa: E501

    def __init__(self, uri: Optional[str] = None) -> None:
        """
        Parameters:
            uri: CRID URL to base the new CRID off of.
        """
        self._show: Optional[str] = None
        self._start: Optional[datetime] = None

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
                self._start = datetime.strptime(
                    parse_qs(parse_qs(self.fragment)["t"][0])["clock"][0],
                    "%Y%m%dT%H%M%S.%fZ",
                )
            except KeyError as ex:
                raise CRIDMissingMediaFragmentError(self.fragment, uri) from ex
            except ValueError as ex:  # pragma: no cover
                raise CRIDMalformedMediaFragmentError(self.fragment, uri) from ex

    def __str__(self) -> str:
        """
        Returns:
            CRID URL  rendered as string.
        """
        return uricompose(*self._uri)

    def __repr__(self) -> str:
        _fqcn = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        return f"<class '{_fqcn}' for '{str(self)}'>"

    @property
    def scheme(self) -> str:
        """
        Returns:
            Scheme part of the CRID.
        """
        return self._uri.scheme

    @property
    def authority(self) -> str:
        """
        Returns:
            Authority part (aka hostname) of CRID.
        """
        return self._uri.authority

    @property
    def path(self) -> CRIDPath:
        """
        Returns:
            Path part of CRID.
        """
        return CRIDPath(self._uri.path)

    @property
    def fragment(self) -> str:
        """
        Returns:
            Framgment part of CRID.
        """
        return self._uri.fragment

    @property
    def version(self) -> str:
        """
        Returns:
            Version from CRIDs path.
        """
        return self._version

    @property
    def show(self) -> Optional[str]:
        """
        Returns:
            Show slug from CRIDs path.
        """
        return self._show

    @property
    def start(self) -> Optional[datetime]:
        """
        Returns:
            Start time form CRIDs media fragment.
        """
        return self._start
