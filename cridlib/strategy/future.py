"""Handle shows in the future."""

from datetime import datetime, timezone
from pathlib import PurePath

from uritools import urisplit  # type: ignore[import-untyped]

from cridlib.util import get_session

__LIBRETIME_INFOV2_URL = (
    "https://airtime.service.int.rabe.ch/api/live-info-v2/format/json"
)


def get_show(future: datetime) -> str:  # pragma: no cover
    """Return the slug for a show from LibreTime if it is in the next 7 days.

    Only returns a show for the next seven days because everything futher than
    that is considered unreliable as of early 2023.

    Args:
    ----
        future: Date to get the show name for.

    Returns:
    -------
        Name of the show scheduled for `future`.

    """
    _resp = get_session().get(
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
            tzinfo=timezone.utc,
        )
        _end = datetime.fromisoformat(_show.get("ends")).replace(tzinfo=timezone.utc)
        if _start <= future <= _end:
            _path = PurePath(urisplit(_show.get("url")).path)
            return _path.stem

    return ""
