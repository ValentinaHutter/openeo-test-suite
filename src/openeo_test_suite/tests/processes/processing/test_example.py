import json5
import math
from pathlib import Path
import pytest
import warnings

examples_path = "assets/processes/tests/*.json5"

def add_id(test, id):
    test["process_id"] = id
    return test

def get_examples():
    examples = []
    package_root_folder = Path(__file__).parents[5]
    files = package_root_folder.glob(examples_path)
    for file in files:
        id = file.stem
        try:
            with file.open() as f:
                data = json5.load(f)
                examples += map(lambda test: add_id(test, id), data["tests"])
        except Exception as e:
            warnings.warn(f"Failed to load {file} due to {e}")
    
    return examples

@pytest.mark.parametrize("example", get_examples())
def test_process(connection, example):
    try:
        connection.describe_process(example["process_id"])
    except:
        pytest.skip("Process {} not supported by the backend".format(example["process_id"]))

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
    throws = bool(example["throws"]) if "throws" in example else False
    returns = "returns" in example

    try:
        result = connection.execute(pg)
    except Exception as e:
        result = e

    if throws and returns:
        if isinstance(result, Exception):
            check_exception(example, result)
        else:
            check_return_value(example, result)
    elif throws:
        check_exception(example, result)
    elif returns:
        check_return_value(example, result)
    else:
        pytest.skip("Test doesn't provide an expected result")


def check_exception(example, result):
    assert isinstance(result, Exception)
    if isinstance(example["throws"], str):
        if result.__class__.__name__ != example["throws"]:
            warnings.warn(f"Expected exception {example['throws']} but got {result.__class__.__name__}")
        # todo: we should enable this end remove the two lines above, but right now tooling doesn't really implement this
        # assert result.__class__.__name__ == example["throws"]

def check_return_value(example, result):
    for name in example["arguments"]:
        arg = example["arguments"][name]
        # handle external references to files
        if isinstance(arg, dict) and "$ref" in arg:
            pytest.skip("external references to files not implemented yet") # todo
        # handle custom types of data
        elif isinstance(arg, dict) and "type" in arg:
            # labeled arrays
            if arg["type"] == "labeled-array":
                pytest.skip("labeled arrays not implemented yet") # todo
            # datacubes
            elif arg["type"] == "datacube":
                pytest.skip("datacubes not implemented yet") # todo

    if isinstance(example["returns"], float):
        assert isinstance(result, float)
        if math.isnan(example["returns"]):
            # handle NaN (not a number) specifically
            assert math.isnan(result)
        else:
            # handle numerical data with a delta
            delta = example["delta"] if "delta" in example else 0.0000000001
            assert result == pytest.approx(example["returns"], delta)
    else:
        assert result == example["returns"]