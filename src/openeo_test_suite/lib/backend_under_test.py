"""

Pytest plugin to allow parameterizing tests over the available collections and processes
of the openEO backend under test.

Originally this was approximated through fixtures, but fixtures are evaluated at test execution time,
not test collection time, making it practically impossible to implement proper parametrization.


"""
import functools
import logging
import os
from typing import List, Union

import openeo
import pytest

_log = logging.getLogger(__name__)


# Internal singleton, pointing to backend under test,
# setup happens in `pytest_configure` hook
_connection: Union[None, openeo.Connection] = None


def pytest_addoption(parser):
    """Implementation of `pytest_addoption` hook."""
    parser.addoption(
        "-U",
        "--openeo-backend-url",
        action="store",
        default=None,
        help="The openEO backend URL to connect to.",
    )


def pytest_configure(config):
    """Implementation of `pytest_configure` hook."""
    global _connection
    assert _connection is None
    backend_url = get_backend_url(config)
    _connection = openeo.connect(url=backend_url, auto_validate=False)


def get_backend_url(config: pytest.Config) -> str:
    """
    Get openEO backend URL from command line option or environment variable.
    """
    url = config.getoption("--openeo-backend-url", default=None)
    if url:
        _log.info(f"Using openEO backend URL from command line option: {url!r}")
    elif os.environ.get("OPENEO_BACKEND_URL"):
        url = os.environ["OPENEO_BACKEND_URL"]
        _log.info(
            f"Using openEO backend URL from env var 'OPENEO_BACKEND_URL': {url!r}"
        )
    else:
        raise RuntimeError(
            "No openEO backend URL found."
            " Specify it using the `--openeo-backend-url` command line option"
            " or through the 'OPENEO_BACKEND_URL' environment variable"
        )

    if isinstance(url, str) and "://" not in url:
        url = f"https://{url}"

    return url


def get_connection() -> openeo.Connection:
    global _connection
    assert _connection is not None
    return _connection


@functools.lru_cache
def get_collection_ids() -> List[str]:
    return [c["id"] for c in get_connection().list_collections()]


@functools.lru_cache
def get_process_ids() -> List[str]:
    return [p["id"] for p in get_connection().list_processes()]
