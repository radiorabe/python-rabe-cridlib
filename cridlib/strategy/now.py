import xml.etree.ElementTree as ET
from pathlib import PurePath

from uritools import urisplit  # type: ignore

from ..util import get_session

__SONGTICKER_URL = "https://songticker.rabe.ch/songticker/0.9.3/current.xml"


def get_show() -> str:
    """Return the currently running show.

    Calls the the [nowplaying](https://github.com/radiorabe/nowplaying) songticker's API.

    Returns:
        Name of the currently running show.
    """

    _resp = get_session().get(__SONGTICKER_URL, timeout=10)
    _tree = ET.fromstring(_resp.text)
    _path = PurePath(urisplit(_tree[3][1].text).path)
    return _path.stem
