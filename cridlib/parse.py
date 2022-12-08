"""Parse RaBe CRID's."""

from .lib import CRID


def parse(value: str) -> CRID:
    """Get CRID dataclass from CRID."""
    return CRID(value)
