import pytest
import requests


def test_add35(connection):
    pg = {
        "add35": {
            "process_id": "add",
            "arguments": {"x": 3, "y": 5},
            "result": True,
        }
    }
    response = connection.execute(pg)
    assert response == 8


def get_examples(url):
    data = requests.get(url).json()
    return data["tests"]


@pytest.mark.parametrize(
    "example",
    get_examples(
        "https://raw.githubusercontent.com/Open-EO/openeo-processes/add-tests/tests/add.json5"
    ),
)
def test_add(connection, example):
    pg = {
        "add": {
            "process_id": "add",
            "arguments": example["arguments"],
            "result": True,
        }
    }
    response = connection.execute(pg)
    assert response == example["returns"]
