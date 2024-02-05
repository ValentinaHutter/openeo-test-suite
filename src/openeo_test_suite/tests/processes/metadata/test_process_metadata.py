import json
import pytest
import requests
from openeo_test_suite.lib.process_selection import get_selected_processes
from openeo_test_suite.lib.backend_under_test import (
    get_backend_under_test,
)


@pytest.fixture(scope="module")
def api_processes():
    endpoint_path = "processes"
    base_url = get_backend_under_test().connection.root_url
    if not base_url:
        raise ValueError("No backend URL configured")
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    full_endpoint_url = f"{base_url}/{endpoint_path}"
    response = requests.get(full_endpoint_url)
    if response.status_code != 200:
        raise ValueError(
            f"Failed to get processes from {full_endpoint_url}: {response.content}"
        )
    return json.loads(response.content)["processes"]


@pytest.mark.parametrize(
    "expected_process",
    [process for process in get_selected_processes() if process.metadata != {}],
    ids=[
        process.process_id
        for process in get_selected_processes()
        if process.metadata != {}
    ],
)
def test_process_metadata_functional(api_processes, expected_process, skipper):
    """
    Tests if the metadata of processes are correct, first tests if the process exists,
    then tests if the parameters of processes are correct and finally tests if the return type of processes is correct.

    Any process that has no metadata is skipped.

    These are the functional parts of the process metadata, e.g. existence (has to be checked) the parameters and return type.
    """

    skipper.skip_if_unsupported_process(expected_process.process_id)

    actual_process = [
        process
        for process in api_processes
        if process["id"] == expected_process.process_id
    ][0]
    # Tests if the parameters of processes are correct

    expected_parameters = expected_process.metadata.get("parameters", [])
    actual_parameters = actual_process["parameters"]

    assert len(expected_parameters) == len(actual_parameters)

    for expected_parameter, actual_parameter in zip(
        expected_parameters, actual_parameters
    ):
        # Tests if parameter names are equivalent
        assert expected_parameter["name"] == actual_parameter["name"]
        # Tests if optionality of parameters is equivalent
        assert expected_parameter.get("optional", False) == actual_parameter.get(
            "optional", False
        )
        # Tests if the type of parameters is equivalent
        assert expected_parameter["schema"] == actual_parameter["schema"]

    # Tests if the return type of processes is correct
    expected_return_type = expected_process.metadata.get("returns", {})

    actual_return_type = actual_process["returns"]
    assert expected_return_type["schema"] == actual_return_type["schema"]


@pytest.mark.parametrize(
    "expected_process",
    [process for process in get_selected_processes() if process.metadata != {}],
    ids=[
        process.process_id
        for process in get_selected_processes()
        if process.metadata != {}
    ],
)
def test_process_metadata_non_functional(api_processes, expected_process, skipper):
    """
    Tests if the non-functional metadata of processes are correct (descriptions and categories), first tests if the process exists,
    then tests if the categories of processes are correct.
    """

    skipper.skip_if_unsupported_process(expected_process.process_id)

    actual_process = [
        process
        for process in api_processes
        if process["id"] == expected_process.process_id
    ][0]

    # Tests if the categories of processes is equivalent
    assert (
        expected_process.metadata.get("categories", []) == actual_process["categories"]
    )

    # Tests if the description of processes is equivalent
    assert (
        expected_process.metadata.get("description", "")
        == actual_process["description"]
    )

    # Tests if the summary of processes is equivalent
    assert expected_process.metadata.get("summary", "") == actual_process["summary"]

    # Tests if the description of parameters is equivalent
    expected_parameters = expected_process.metadata.get("parameters", [])
    actual_parameters = actual_process["parameters"]

    assert len(expected_parameters) == len(actual_parameters)

    for expected_parameter, actual_parameter in zip(
        expected_parameters, actual_parameters
    ):
        assert expected_parameter.get("description", "") == actual_parameter.get(
            "description", ""
        )

    # Tests if the description of returns is equivalent
    expected_return_type = expected_process.metadata.get("returns", {})
    actual_return_type = actual_process["returns"]
    assert expected_return_type.get("description", "") == actual_return_type.get(
        "description", ""
    )

    # Tests if the links of processes are equivalent
    expected_links = expected_process.metadata.get("links", [])
    actual_links = actual_process["links"]
    for expected_link, actual_link in zip(expected_links, actual_links):
        assert expected_link.get("href", "") == actual_link.get("href", "")
        assert expected_link.get("rel", "") == actual_link.get("rel", "")
        assert expected_link.get("title", "") == actual_link.get("title", "")
