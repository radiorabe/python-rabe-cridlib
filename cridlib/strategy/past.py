"""The past strategy implements getting data from archiv.rabe.ch."""

from datetime import datetime

import requests

from cridlib.const import ARCHIV_BROADCASTS_URL


def get_show(past: datetime) -> str:
    """Return the a show slug from a past show."""

    _url = f"{ARCHIV_BROADCASTS_URL}{past.year}/{past.month:02d}/{past.day:02d}/{past.hour:02d}{past.minute:02d}{past.second:02d}"  # pylint: disable=line-too-long
    _resp = requests.get(_url, timeout=10)
    _json = _resp.json()
    _data = _json.get("data")
    _label = str(_data[0].get("attributes").get("label"))

    return _label.lower().replace(" ", "-")
