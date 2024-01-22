import argparse
import logging
import os
from distutils.util import strtobool
from typing import List

import openeo
import pytest

from openeo_test_suite.lib.backend_under_test import get_backend_url
from openeo_test_suite.lib.skipping import Skipper

_log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def skip_experimental(request) -> bool:
    """
    Fixture to determine whether experimental functionality should be tested or not.
    """
    skip = not request.config.getoption("--experimental")
    _log.info(f"Skip experimental functionality {skip=}")
    return skip


@pytest.fixture(scope="session")
def process_levels(request) -> List[str]:
    """
    Fixture to get the desired openEO profiles levels.
    """
    levels_str = request.config.getoption("--process-levels")

    if isinstance(levels_str, str) and len(levels_str) > 0:
        _log.info(f"Testing process levels {levels_str!r}")
        return list(map(lambda l: l.strip(), levels_str.split(",")))
    else:
        return []


@pytest.fixture(scope="session")
def processes(request) -> List[str]:
    """
    Fixture to get the desired processes to test against.
    """
    processes_str = request.config.getoption("--processes")

    if isinstance(processes_str, str) and len(processes_str) > 0:
        _log.info(f"Testing processes {processes_str!r}")
        return list(map(lambda p: p.strip(), processes_str.split(",")))
    else:
        return []


@pytest.fixture(scope="module")
def auto_authenticate() -> bool:
    """
    Fixture to act as parameterizable toggle for authenticating the connection fixture.
    Allows per-test/folder configuration of auto-authentication.
    """
    return False


@pytest.fixture(scope="module")
def connection(request, auto_authenticate: bool, pytestconfig) -> openeo.Connection:
    backend_url = get_backend_url(request.config, required=True)
    con = openeo.connect(backend_url, auto_validate=False)

    if auto_authenticate:
        auth_method = os.environ.get("OPENEO_AUTH_METHOD")

        if auth_method == "none":
            pass
        elif auth_method == "basic":
            con.authenticate_basic(
                username=os.environ.get("OPENEO_AUTH_BASIC_USERNAME"),
                password=os.environ.get("OPENEO_AUTH_BASIC_PASSWORD"),
            )
        else:
            # Temporarily disable output capturing, to make sure that OIDC device code instructions (if any) are visible to the user.
            # Note: this is based on `capfd.disabled()`, but compatible with a wide fixture scopes (e.g. session or module)
            capmanager = pytestconfig.pluginmanager.getplugin("capturemanager")
            with capmanager.global_and_fixture_disabled():
                # Note: this generic `authenticate_oidc()` call allows both:
                # - device code/refresh token based authentication for manual test suite runs
                # - client credentials auth through env vars for automated/Jenkins CI runs
                #
                # See https://open-eo.github.io/openeo-python-client/auth.html#oidc-authentication-dynamic-method-selection
                con.authenticate_oidc()

    return con


@pytest.fixture
def skipper(connection, process_levels) -> Skipper:
    return Skipper(connection=connection, process_levels=process_levels)
