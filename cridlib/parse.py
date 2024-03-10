"""Parse an existing CRID."""

from .lib import CRID


def parse(value: str) -> CRID:
    """Get CRID dataclass from CRID.

    Args:
    ----
        value: CRID URL as a string.

    Returns:
    -------
        CRID: The parsed CRID.

    """
    return CRID(value)
