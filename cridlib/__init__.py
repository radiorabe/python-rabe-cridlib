"""Generate RaBe Content Reference Idenitifier Spcification (CRID) Identifiers.

# `get(timestamp=None, fragment='')`
::: cridlib.get.get
    options:
      show_source: false

# `parse(value)`
::: cridlib.parse.parse
    options:
      show_source: false
"""

from .get import get
from .lib import CRIDError
from .parse import parse
