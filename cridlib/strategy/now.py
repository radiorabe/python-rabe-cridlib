"""The now strategy implements getting data from Songticker."""

import xml.etree.ElementTree as ET
from pathlib import PurePath

import requests
from uritools import urisplit  # type: ignore

__SONGTICKER_URL = "https://songticker.rabe.ch/songticker/0.9.3/current.xml"


def get_show() -> str:
    """Return the currently running shows slug from nowplaying."""

    _resp = requests.get(__SONGTICKER_URL, timeout=10)
    _tree = ET.fromstring(_resp.text)
    _path = PurePath(urisplit(_tree[3][1].text).path)
    return _path.stem
