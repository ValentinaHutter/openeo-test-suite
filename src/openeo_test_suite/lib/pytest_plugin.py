import argparse

import openeo

from openeo_test_suite.lib.backend_under_test import (
    HttpBackend,
    NoBackend,
    get_backend_url,
    set_backend_under_test,
)
from openeo_test_suite.lib.process_selection import set_process_selection_from_config


def pytest_addoption(parser):
    """Implementation of `pytest_addoption` hook."""
    parser.addoption(
        "-U",
        "--openeo-backend-url",
        action="store",
        default=None,
        help="The openEO backend URL to connect to.",
    )

    parser.addoption(
        "--process-levels",
        action="store",
        default="",
        help="openEO process selection: "
        "the openEO process profiles/levels you want to test against, e.g. 'L1,L2,L2A'. "
        "Can be used in combination with `--processes`, in which case the union of both selections will be taken. ",
    )
    parser.addoption(
        "--processes",
        action="store",
        default="",
        help="openEO process selection: "
        "the openEO processes you want to test against, e.g. 'apply,reduce_dimension'. "
        "Can be used in combination with `--process-levels`, in which case the union of both selections will be taken.",
    )

    parser.addoption(
        "--experimental",
        type=bool,
        action=argparse.BooleanOptionalAction,
        default=False,
        help="openEO process selection: "
        "toggle to consider experimental processes (and experimental tests) in the test selection procedure. "
        "By default, experimental processes are ignored.",
    )

    parser.addoption(
        "--runner",
        action="store",
        default="skip",
        help="A specific test runner to use for individual process tests. If not provided, uses a default HTTP API runner.",
    )

    parser.addoption(
        "--s2-collection",
        action="store",
        default=None,
        help="The data collection to test against. It can be either a Sentinel-2 STAC Collection or the name of an openEO Sentinel-2 Collection provided by the back-end.",
    )


def pytest_configure(config):
    """Implementation of `pytest_configure` hook."""
    backend_url = get_backend_url(config)
    if backend_url is None:
        backend = NoBackend()
    else:
        connection = openeo.connect(url=backend_url, auto_validate=False)
        backend = HttpBackend(connection=connection)
    set_backend_under_test(backend)

    set_process_selection_from_config(config)
