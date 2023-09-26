import logging
import os
import pytest

_log = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--openeo-backend-url",
        action="store",
        default=None,
        help="The openEO backend URL to connect to.",
    )


@pytest.fixture(scope="session")
def backend_url(request) -> str:
    """
    Fixture to get the desired openEO back-end URL to test against.
    """
    # TODO: also support getting it from a config file?
    if request.config.getoption("--openeo-backend-url"):
        url = request.config.getoption("--openeo-backend-url")
    elif "OPENEO_BACKEND_URL" in os.environ:
        url = os.environ["OPENEO_BACKEND_URL"]
    else:
        raise RuntimeError(
            "No openEO backend URL found. Specify it using the `--openeo-backend-url` command line option or through the 'OPENEO_BACKEND_URL' environment variable"
        )

    if "://" not in url:
        url = f"https://{url}"

    _log.info(f"Using openEO back-end URL {url!r}")

    return url
