import json5
import math
from pathlib import Path
import pytest
import warnings

# glob path to the test files
examples_path = "assets/processes/tests/*.json5"
# for debugging purposes, you can limit the tests to specific processes
processes = []

def get_examples():
    examples = []
    package_root_folder = Path(__file__).parents[5]
    files = package_root_folder.glob(examples_path)
    for file in files:
        id = file.stem
        # if specific processes are specified above, skip all others
        if len(processes) > 0 and id not in processes:
            continue
        try:
            with file.open() as f:
                data = json5.load(f)
                examples += map(lambda test: [id, test], data["tests"])
        except Exception as e:
            warnings.warn("Failed to load {} due to {}".format(file, e))
    
    return examples

@pytest.mark.parametrize("id,example", get_examples())
def test_process(connection, id, example):
    # check whether the process is available
    try:
        connection.describe_process(id)
    except:
        pytest.skip("Process {} not supported by the backend".format(id))

    # check whether any additionally required processes are available
    if "required" in example:
        for pid in example["required"]:
            try:
                connection.describe_process(pid)
            except:
                pytest.skip("Test requires additional process {} which is not available".format(pid))

    # prepare the arguments from test JSON encoding to internal backend representations
    # or skip if not supported by the test runner
    try:
        arguments = prepare_arguments(example["arguments"], connection)
    except Exception as e:
        pytest.skip(str(e))

    # build the process to run
    pg = {
        "process_graph": {
            "node": {
                "process_id": id,
                "arguments": arguments,
                "result": True,
            }
        }
    }

    # todo: handle experimental processes (warning instead of error?)
    experimental = example["experimental"] if "experimental" in example else False
    throws = bool(example["throws"]) if "throws" in example else False
    returns = "returns" in example

    # execute the process (synchronously)
    try:
        result = connection.execute(pg)
    except Exception as e:
        result = e

    # check the process results / behavior
    if throws and returns:
        if isinstance(result, Exception):
            check_exception(example, result)
        else:
            check_return_value(example, result, connection)
    elif throws:
        check_exception(example, result)
    elif returns:
        check_return_value(example, result, connection)
    else:
        pytest.skip("Test doesn't provide an expected result")

def prepare_arguments(arguments, connection):
    for name in arguments:
        arg = arguments[name]
        # handle external references to files
        if isinstance(arg, dict) and "$ref" in arg:
            raise Exception("external references to files not implemented yet")
        # handle custom types of data
        elif isinstance(arg, dict) and "type" in arg:
            # labeled arrays
            if arg["type"] == "labeled-array":
                arg = connection.encode_labeled_array(arg)
            # datacubes
            elif arg["type"] == "datacube":
                arg = connection.encode_datacube(arg)

        if connection.is_json_only():
            check_non_json_values(arg)
    
    return arguments

def check_non_json_values(value):
    if isinstance(value, float):
        if math.isnan(value):
            raise Exception("HTTP JSON APIs don't support NaN values")
        elif math.isinf(value):
            raise Exception("HTTP JSON APIs don't support infinity values")
    elif isinstance(value, dict):
        for key in value:
            check_non_json_values(value[key])
    elif isinstance(value, list):
        for item in value:
            check_non_json_values(item)

def check_exception(example, result):
    assert isinstance(result, Exception)
    if isinstance(example["throws"], str):
        if result.__class__.__name__ != example["throws"]:
            warnings.warn("Expected exception {} but got {}".format(example['throws'], result.__class__.__name__))
        # todo: we should enable this end remove the two lines above, but right now tooling doesn't really implement this
        # assert result.__class__.__name__ == example["throws"]

def check_return_value(example, result, connection):
    # handle custom types of data
    result = connection.decode_data(result)

    if isinstance(example["returns"], float) and math.isnan(example["returns"]):
        assert math.isnan(result)
    elif isinstance(example["returns"], float) or isinstance(example["returns"], int):
        assert isinstance(result, float) or isinstance(result, int), "Expected a numerical result but got {} of type {}".format(result, type(result))
        # handle numerical data with a delta
        delta = example["delta"] if "delta" in example else 0.0000000001
        assert result == pytest.approx(example["returns"], delta)
    else:
        assert result == example["returns"], "Expected {} but got {}".format(example["returns"], result)
