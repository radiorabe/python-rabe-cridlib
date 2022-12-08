"""The now strategy implements getting data from Songticker."""

import xml.etree.ElementTree as ET

import requests
from uri import URI  # type: ignore

from cridlib.const import SONGTICKER_URL


def get_show() -> str:
    """Return the currently running shows slug from nowplaying."""

    _resp = requests.get(SONGTICKER_URL, timeout=10)
    _tree = ET.fromstring(_resp.text)
    _uri = URI(f"{_tree[3][1].text}")
    return _uri.path.stem
