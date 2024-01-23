from unittest import mock

import pytest

from openeo_test_suite.lib.backend_under_test import get_backend_url


def test_get_backend_url_default(request):
    url = get_backend_url(config=request.config)
    assert url is None


@pytest.mark.parametrize(
    ["configured_url", "expected"],
    [
        ("https://openeo.test", "https://openeo.test"),
        ("openeo.test", "https://openeo.test"),
    ],
)
def test_get_backend_url_mocked_config(configured_url, expected):
    config = mock.Mock()
    config.getoption.return_value = configured_url
    url = get_backend_url(config=config, required=True)
    assert url == expected
