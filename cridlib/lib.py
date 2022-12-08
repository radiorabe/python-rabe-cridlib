"""Low-level cridlib implemenetation bits."""

from datetime import datetime
from urllib.parse import parse_qs

import uri  # type: ignore


class CRIDError(Exception):
    """Represent all cridlib errors."""


class CRIDSchemeMismatchError(CRIDError):
    """Scheme in URI does not match 'crid'."""


class CRIDSchemeHostMismatchError(CRIDError):
    """Hostname part of URI does not match 'rabe.ch'."""


class CRIDUnsupportedVersionError(CRIDError):
    """Unsupported version in path of URI."""


class CRIDMissingMediaFragmentError(CRIDError):
    """Missing media-fragment with clock code."""


class CRIDMalformedMediaFragmentError(CRIDError):
    """Missing media-fragment with clock code."""


class CRID(uri.URI):
    """Represent CRIDs using uri."""

    def __init__(
        self, _uri: uri.typing.Optional[uri.typing.URILike] = None, **parts
    ) -> None:
        super().__init__(_uri, **parts)
        if self.scheme != "crid":
            raise CRIDSchemeMismatchError(self.scheme)
        if self.host != "rabe.ch":
            raise CRIDSchemeHostMismatchError(self.host)
        if not self.path.match("/v1/*"):
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


def setup():
    """Setup RaBe cridlib."""
    uri.part.scheme.SchemePart.registry["crid"] = uri.scheme.URLScheme("crid")
