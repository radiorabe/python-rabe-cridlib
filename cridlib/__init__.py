"""Generate RaBe Content Reference Idenitifier Spcification (CRID) Identifiers.

* [`cridlib.get(timestamp=None, fragment='')`](./get/#cridlib.get.get)
* [`cridlib.parse(value)`](./parse/#gridlib.parse.parse)
"""

from .get import get
from .lib import CRIDError
from .parse import parse

__all__ = [
    "CRIDError",
    "get",
    "parse",
]
