"""Main "get" interface for RaBe CRID's."""

from datetime import datetime

from .lib import CRID
from .strategy import future, now, past


def get(timestamp=None) -> CRID:
    """Get a RaBe CRID."""
    _now = datetime.now()
    _ts = timestamp or _now
    _show = ""
    if _ts == _now:
        _show = now.get_show()
    elif _ts < _now:
        _show = past.get_show(past=_ts)
    elif _ts > _now:  # pragma: no cover
        _show = future.get_show(future=_ts)

    _tscode = f"{_ts.strftime('%Y%m%dT%H%M%S.%f')[:-4]}Z"
    return CRID(f"crid://rabe.ch/v1/{_show}#t=clock={_tscode}")
