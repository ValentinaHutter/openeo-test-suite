import json
import logging

import pytest
import requests
from stac_validator import stac_validator

_log = logging.getLogger(__name__)


def test_collections_links_presence(backend_url):
    """
    Tests if the /collections endpoint returns a JSON
    containing the collections list and the links list.
    Both of them are mandatory, see here:
    https://api.openeo.org/#tag/EO-Data-Discovery/operation/list-collections
    """
    collections_url = backend_url + "/collections"
    resp = requests.get(url=collections_url)
    data = resp.json()
    assert "collections" in data
    assert "links" in data


def test_valid_stac_general(backend_url):
    """
    Tests if the JSON document describing each Collection
    is a valid STAC.
    For each invalid Collection logs an informative error.
    """
    collections_url = backend_url + "/collections"
    resp = requests.get(url=collections_url)
    data = resp.json()
    # with open("collections_eurac_dev.json","r") as f:
    #     data = json.load(f)
    collections = data["collections"]
    all_collections_valid_stac = True
    all_specific_collections_valid_stac = True
    for c in collections:
        stac = stac_validator.StacValidate()
        is_valid_stac = stac.validate_dict(c)
        c_id = c["id"]
        if not is_valid_stac:
            _log.error(
                f"The general collection JSON for {c_id} is not a valid STAC. stac-validator message: {stac.message}"
            )
            all_collections_valid_stac = False
        specific_collection_url = collections_url + "/" + c_id
        resp = requests.get(url=specific_collection_url)
        data = resp.json()
        stac = stac_validator.StacValidate()
        is_valid_stac = stac.validate_dict(data)
        c_id = data["id"]
        if not is_valid_stac:
            _log.error(
                f"The specifc collection JSON for {c_id} is not a valid STAC. stac-validator message: {stac.message}"
            )
            all_specific_collections_valid_stac = False
    assert all_collections_valid_stac
    assert all_specific_collections_valid_stac
