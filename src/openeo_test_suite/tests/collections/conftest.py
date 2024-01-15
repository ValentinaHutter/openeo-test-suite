import pytest
import requests


@pytest.fixture
def openeo_get_collections(backend_url):
    """
    Given the openEO back-end url, performs a GET request to
    the /collections endpoint and returns the JSON response.
    """
    # TODO #18 replace with backend_under_test approach
    collections_url = backend_url + "/collections"
    resp = requests.get(url=collections_url)
    return resp.json()


@pytest.fixture
def openeo_collections_ids(openeo_get_collections):
    """
    Return the list of collection ids available under /collections.
    """
    # TODO #18 replace with backend_under_test approach
    return [c["id"] for c in openeo_get_collections["collections"]]
