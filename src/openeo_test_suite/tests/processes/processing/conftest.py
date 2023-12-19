import logging
import os

import openeo
import pytest

from openeo_test_suite.lib.process_runner.base import ProcessTestRunner

_log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def runner(request) -> str:
    """
    Fixture to get the desired runner to test with.
    """
    # TODO: also support getting it from a config file?
    if request.config.getoption("--runner"):
        runner = request.config.getoption("--runner")
    elif "OPENEO_RUNNER" in os.environ:
        runner = os.environ["OPENEO_RUNNER"]
    else:
        runner = "http"

    _log.info(f"Using runner {runner!r}")

    return runner


@pytest.fixture
def connection(
    backend_url: str, runner: str, auto_authenticate: bool, capfd
) -> ProcessTestRunner:
    if runner == "dask":
        from openeo_test_suite.lib.process_runner.dask import Dask

        return Dask()
    elif runner == "vito":
        from openeo_test_suite.lib.process_runner.vito import Vito

        return Vito()
    else:
        from openeo_test_suite.lib.process_runner.http import Http

        con = openeo.connect(backend_url)
        if auto_authenticate:
            with capfd.disabled():
                con.authenticate_oidc()

        return Http(con)
