"""Utility functions for cridlib."""

from requests import Session
from requests.adapters import HTTPAdapter, Retry


def get_session(
    retries: int = 5,
    backoff_factor: float = 0.1,
) -> Session:
    """Get a requests session with retry/backoff.

    Args:
    ----
        retries: How often to retry.
        backoff_factor: A backoff factor to apply between attempts after the
            second try (most errors are resolved immediately by a second try
            without a delay). urllib3 will sleep for::
                {backoff factor} * (2 ** ({number of total retries} - 1))
            seconds. If the backoff_factor is 0.1, then :func:`Retry.sleep`
            will sleep for [0.0s, 0.2s, 0.4s, ...] between retries. It will
            never be longer than `backoff_max`.
            By default, backoff is set to 0.1.

    """
    session = Session()
    session.mount(
        "https://",
        HTTPAdapter(
            max_retries=Retry(
                total=retries,
                backoff_factor=backoff_factor,
            ),
        ),
    )
    return session
