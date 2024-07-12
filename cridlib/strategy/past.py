"""Handle shows from the past."""

from datetime import datetime

from pytz import timezone

from cridlib.util import get_session

__ARCHIV_BROADCASTS_URL = "https://archiv.rabe.ch/api/broadcasts/"
__ARCHIV_TIMEZONE = "Europe/Zurich"


def get_show(past: datetime) -> str:
    """Return a show from the past.

    Asks the the [raar](https://github.com/radiorabe/raar) archive for the info.

    Args:
    ----
        past: Date to get the show name for.

    Returns:
    -------
        Show name from the archive for `past`.

    """
    local = past
    if past.tzname != __ARCHIV_TIMEZONE:
        local = past.astimezone(timezone(__ARCHIV_TIMEZONE))

    _url = f"{__ARCHIV_BROADCASTS_URL}{local.year}/{local.month:02d}/{local.day:02d}/{local.hour:02d}{local.minute:02d}{local.second:02d}"  # noqa: E501
    _resp = get_session().get(_url, timeout=10)
    _json = _resp.json()
    _data = _json.get("data")
    _label = str(_data[0].get("attributes").get("label")) if len(_data) == 1 else ""

    return _label.lower().replace(" ", "-")
