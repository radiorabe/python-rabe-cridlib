"""The future strategy implements getting data from LibreTime."""

from datetime import datetime, timezone
from pathlib import PurePath

import requests
from uritools import urisplit  # type: ignore

__LIBRETIME_INFOV2_URL = (
    "https://airtime.service.int.rabe.ch/api/live-info-v2/format/json"
)


def get_show(future: datetime) -> str:  # pragma: no cover
    """Return the slug for a show from LibreTime if it is in the next 7 days."""

    _resp = requests.get(
        __LIBRETIME_INFOV2_URL,
        params={
            "days": 7,
            "shows": 7000,
        },
        timeout=10,
    )

    _json = _resp.json()
    _tz = _json.get("station").get("timezone")
    _next = _json.get("shows").get("next")
    for _show in _next:
        _start = datetime.fromisoformat(_show.get("starts")).replace(
            tzinfo=timezone.utc
        )
        _end = datetime.fromisoformat(_show.get("ends")).replace(tzinfo=timezone.utc)
        if _start <= future <= _end:
            _path = PurePath(urisplit(_show.get("url")).path)
            return _path.stem

    return ""
