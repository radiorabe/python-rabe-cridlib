"""Main "get" interface for RaBe CRID's."""

from datetime import datetime, timezone

from .lib import CRID, canonicalize_show
from .strategy import future, now, past


def get(timestamp=None, fragment="") -> CRID:
    """Get a RaBe CRID.

    If you need to get the CRID for a specific point in RaBe time using a human-readable timezone:

    ```python
    >>> from datetime import datetime
    >>> from pytz import timezone
    >>> crid = get(datetime(2020, 3, 1, 00, 00, tzinfo=timezone('Europe/Zurich')))
    >>> print(f"version: {crid.version}, start: {crid.start}")
    version: v1, start: ...

    ```

    """
    _now = datetime.now(timezone.utc)
    _ts = timestamp or _now
    _show = ""
    if _ts == _now:
        _show = now.get_show()
    elif _ts < _now:
        _show = past.get_show(past=_ts)
    elif _ts > _now:  # pragma: no cover
        _show = future.get_show(future=_ts)

    if _show:
        _show = canonicalize_show(_show)

    _tscode = f"t=clock={_ts.strftime('%Y%m%dT%H%M%S.%f')[:-4]}Z"
    _fragment = f"{_tscode}{'&' + fragment if fragment else ''}"

    return CRID(f"crid://rabe.ch/v1{'/' + _show if _show else ''}#{_fragment}")
