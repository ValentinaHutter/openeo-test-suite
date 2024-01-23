from unittest import mock

import pytest

from openeo_test_suite.lib.backend_under_test import (
    NoBackend,
    get_backend_under_test,
    get_backend_url,
    get_collection_ids,
    get_process_ids,
)


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


def test_get_backend_under_test():
    but = get_backend_under_test()
    assert isinstance(but, NoBackend)


def test_get_collection_ids():
    assert get_collection_ids() == []


def test_get_process_ids():
    assert get_process_ids() == []
