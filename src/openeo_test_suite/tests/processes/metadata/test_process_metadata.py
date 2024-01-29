import json
import pytest
import requests
from openeo_test_suite.lib.process_selection import get_selected_processes
from openeo_test_suite.lib.backend_under_test import get_backend_url


@pytest.fixture(scope="module")
def api_processes(request):
    endpoint_path = "processes"
    base_url = get_backend_url(request.config)
    if not base_url:
        raise ValueError("No backend URL configured")
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    full_endpoint_url = f"{base_url}/{endpoint_path}"
    response = json.loads(requests.get(full_endpoint_url).content)
    return response["processes"]


_get_selected_processes = get_selected_processes.__wrapped__


def get_examples():
    """Collect process examples/tests from examples root folder containing JSON5 files."""
    return [process for process in _get_selected_processes()]


@pytest.mark.parametrize(
    "expected_process",
    [process for process in get_examples() if process.metadata != {}],
    ids=[process.process_id for process in get_examples() if process.metadata != {}],
)
def test_process_metadata_functional(api_processes, expected_process):
    """
    Tests if the metadata of processes are correct, first tests if the process exists,
    then tests if the parameters of processes are correct and finally tests if the return type of processes is correct.

    Any process that has no metadata is skipped.

    These are the functional parts of the process metadata, e.g. existence (has to be checked) the parameters and return type.
    """
    # Tests if the process exists
    assert expected_process.process_id in [
        process["id"] for process in api_processes
    ], f"The process '{expected_process.process_id}' was not found on the backend"

    # Tests if the parameters of processes are correct

    expected_parameters = expected_process.metadata.get("parameters", [])
    actual_parameters = [
        process
        for process in api_processes
        if process["id"] == expected_process.process_id
    ][0]["parameters"]
    for expected_parameter, actual_parameter in zip(
        expected_parameters, actual_parameters
    ):
        # Tests if parameter names are equivalent
        assert (
            expected_parameter["name"] == actual_parameter["name"]
        ), f"The parameter named '{actual_parameter['name']}' of the process \
            '{expected_process.process_id}' should be named '{expected_parameter['name']}'"
        # Tests if optionality of parameters is equivalent
        assert expected_parameter.get("optional", False) == actual_parameter.get(
            "optional", False
        ), f"The parameter named '{actual_parameter['name']}' of the process \
            '{expected_process.process_id}' should have '{expected_parameter.get('optional', False)}' optionality"
        # Tests if the type of parameters is equivalent
        assert (
            expected_parameter["schema"] == actual_parameter["schema"]
        ), f"The parameter named '{actual_parameter['name']}' of the process \
            '{expected_process.process_id}' should have the schema '{expected_parameter['schema']}' \
            but has the schema '{actual_parameter['schema']}'"

    # Tests if the return type of processes is correct
    expected_return_type = expected_process.metadata.get("returns", {})

    actual_return_type = [
        process
        for process in api_processes
        if process["id"] == expected_process.process_id
    ][0]["returns"]
    print()
    assert (
        expected_return_type["schema"] == actual_return_type["schema"]
    ), f"The return type of the process '{expected_process.process_id}' should be \
        '{expected_return_type['schema']}' but is actually '{actual_return_type['schema']}'"


@pytest.mark.parametrize(
    "expected_process",
    [process for process in get_examples() if process.metadata != {}],
    ids=[process.process_id for process in get_examples() if process.metadata != {}],
)
def test_process_metadata_non_functional(api_processes, expected_process):
    """
    Tests if the non-functional metadata of processes are correct (descriptions and categories), first tests if the process exists,
    then tests if the categories of processes are correct.
    """

    assert expected_process.process_id in [
        process["id"] for process in api_processes
    ], f"The process '{expected_process.process_id}' was not found on the backend"

    # Tests if the categories of processes is equivalent
    assert (
        expected_process.metadata.get("categories", [])
        == [
            process
            for process in api_processes
            if process["id"] == expected_process.process_id
        ][0]["categories"]
    ), f"The process '{expected_process.process_id}' has the wrong categories, \
        should be '{expected_process.metadata.get('categories', [])}'\
        but is actually '{[process for process in api_processes if process['id'] == expected_process.process_id][0]['categories']}'"

    # Tests if the description of processes is equivalent
    assert (
        expected_process.metadata.get("description", "")
        == [
            process
            for process in api_processes
            if process["id"] == expected_process.process_id
        ][0]["description"]
    ), f"The process '{expected_process.process_id}' has the wrong description, \
        should be '{expected_process.metadata.get('description', '')}'\
        but is actually '{[process for process in api_processes if process['id'] == expected_process.process_id][0]['description']}'"

    # Tests if the summary of processes is equivalent
    assert (
        expected_process.metadata.get("summary", "")
        == [
            process
            for process in api_processes
            if process["id"] == expected_process.process_id
        ][0]["summary"]
    ), f"The process '{expected_process.process_id}' has the wrong summary, \
        should be '{expected_process.metadata.get('summary', '')}'\
        but is actually '{[process for process in api_processes if process['id'] == expected_process.process_id][0]['summary']}'"

    # Tests if the description of parameters is equivalent
    expected_parameters = expected_process.metadata.get("parameters", [])
    actual_parameters = [
        process
        for process in api_processes
        if process["id"] == expected_process.process_id
    ][0]["parameters"]

    for expected_parameter, actual_parameter in zip(
        expected_parameters, actual_parameters
    ):
        assert expected_parameter.get("description", "") == actual_parameter.get(
            "description", ""
        ), f"The parameter named '{actual_parameter['name']}' of the process \
            '{expected_process.process_id}' should have the description '{expected_parameter.get('description', '')}' \
            but has the description '{actual_parameter.get('description', '')}'"

    # Tests if the description of returns is equivalent
    expected_return_type = expected_process.metadata.get("returns", {})
    actual_return_type = [
        process
        for process in api_processes
        if process["id"] == expected_process.process_id
    ][0]["returns"]
    assert expected_return_type.get("description", "") == actual_return_type.get(
        "description", ""
    ), f"The return type of the process '{expected_process.process_id}' should have the description \
        '{expected_return_type.get('description', '')}' but has the description '{actual_return_type.get('description', '')}'"

    # Tests if the links of processes are equivalent
    expected_links = expected_process.metadata.get("links", [])
    actual_links = [
        process
        for process in api_processes
        if process["id"] == expected_process.process_id
    ][0]["links"]
    for expected_link, actual_link in zip(expected_links, actual_links):
        assert expected_link.get("href", "") == actual_link.get(
            "href", ""
        ), f"The link of the process '{expected_process.process_id}' should be \
            '{expected_link.get('href', '')}' but is actually '{actual_link.get('href', '')}'"
        assert expected_link.get("rel", "") == actual_link.get(
            "rel", ""
        ), f"The link of the process '{expected_process.process_id}' should be \
            '{expected_link.get('rel', '')}' but is actually '{actual_link.get('rel', '')}'"
        assert expected_link.get("title", "") == actual_link.get(
            "title", ""
        ), f"The link of the process '{expected_process.process_id}' should be \
            '{expected_link.get('title', '')}' but is actually '{actual_link.get('title', '')}'"
