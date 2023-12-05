import math
import pytest
import requests_cache
import warnings

spec_url = "https://raw.githubusercontent.com/Open-EO/openeo-processes/add-tests/tests/{}.json5"

def add_id(test, id):
    test["process_id"] = id
    return test

def get_examples(url_template, ids):
    examples = []
    for id in ids:
        session = requests_cache.CachedSession("openeo-processes-tests", expire_after=12*60*60) # cache for 12 hours
        try:
            url = url_template.format(id)
            data = session.get(url).json()
            examples += map(lambda test: add_id(test, id), data["tests"])
        except:
            warnings.warn("No tests available for process " + id)
    
    return examples

def get_test_parameters():
    # todo: how can we access the connection or parameter here to create a new one?
    from openeo_test_suite.lib.dask import dask_connection
    connection = dask_connection()

    process_ids = map(lambda process: process["id"], connection.list_processes())
    return pytest.mark.parametrize(
        "example", 
        get_examples(spec_url, process_ids)
    )

pytestmark = get_test_parameters()

def test_process(connection, example):
    pg = {
        "process_graph": {
            "node": {
                "process_id": example["process_id"],
                "arguments": example["arguments"],
                "result": True,
            }
        }
    }

    # todo: handle experimental processes (warning instead of error?)
    experimental = example["experimental"] if "experimental" in example else False

    if "throws" in example and not "returns" in example:
        with pytest.raises(Exception):
            # todo: check that the exception is of the right type (if example["throws"] is given as string)
            result = connection.execute(pg)
    else:
        result = connection.execute(pg)

    # todo: handle external references to files
    # todo: handle labeled arrays
    # todo: handle datacube metadata
    if "throws" in example and "returns" in example:
        # todo: handle exceptions correctly
        warnings.warn("Can't handle throws and returns at the same time yet")
    elif math.isnan(example["returns"]):
        assert math.isnan(result)
    elif isinstance(example["returns"], float):
        assert isinstance(result, float)
        delta = example["delta"] if "delta" in example else 0.0000000001
        assert result == pytest.approx(example["returns"], delta)
    else:
        assert result == example["returns"]
