import pytest
import requests

def add_id(test, id):
    test["id"] = id
    return test

def get_examples(url, ids):
    examples = []
    for id in ids:
        url = url.format(id)
        try:
            data = requests.get(url).json()
        except:
            print("No tests available for process " + id)
            continue
        examples += map(lambda test: add_id(test, id), data["tests"])
    
    return examples

def get_test_parameters():
    # todo: how can we access the connection or parameter here to create a new one?
    from openeo_test_suite.lib.dask import dask_connection
    connection = dask_connection()

    process_ids = map(lambda process: process["id"], connection.list_processes())
    spec_url = "https://raw.githubusercontent.com/Open-EO/openeo-processes/add-tests/tests/{}.json5"
    return pytest.mark.parametrize(
        "example", 
        get_examples(spec_url, process_ids)
    )

pytestmark = get_test_parameters()

def test_process(connection, example):
    pg = {
        "process_graph": {
            "node": {
                "process_id": example["id"],
                "arguments": example["arguments"],
                "result": True,
            }
        }
    }

    response = connection.execute(pg)
    assert response == example["returns"]
