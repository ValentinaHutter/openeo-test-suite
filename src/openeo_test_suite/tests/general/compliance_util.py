from typing import Union
from openapi_core import Spec
import yaml
import json
import os
import uuid
import requests
import time

from openeo_test_suite.lib.backend_under_test import (
    get_backend_url,
    get_backend_under_test,
)


from openapi_core import validate_response
from openapi_core.contrib.requests import RequestsOpenAPIRequest
from openapi_core.contrib.requests import RequestsOpenAPIResponse
from openapi_core import V30ResponseValidator


def test_endpoint(
    base_url: str,
    endpoint_path: str,
    test_name: str,
    spec: Spec,
    payload: dict = None,
    bearer_token: str = None,
    method: str = "GET",
    expected_status_codes: Union[list[int], int] = [200],
    return_response: bool = False,
):
    full_endpoint_url = f"{base_url}{endpoint_path}"

    if bearer_token is not None:
        if method == "POST":
            requests_response = requests.post(
                full_endpoint_url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"{bearer_token}",
                },
            )

            requests_request = requests.Request(
                "post",
                full_endpoint_url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"{bearer_token}",
                },
            )

        elif method == "PUT":
            requests_response = requests.put(
                full_endpoint_url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"{bearer_token}",
                },
            )

            requests_request = requests.Request(
                "put",
                full_endpoint_url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"{bearer_token}",
                },
            )

        elif method == "PATCH":
            requests_response = requests.patch(
                full_endpoint_url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"{bearer_token}",
                },
            )

            requests_request = requests.Request(
                "patch",
                full_endpoint_url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"{bearer_token}",
                },
            )

        if method == "GET":
            requests_response = requests.get(
                full_endpoint_url, headers={"Authorization": f"{bearer_token}"}
            )
            requests_request = requests.Request(
                "get", full_endpoint_url, headers={"Authorization": f"{bearer_token}"}
            )

        elif method == "DELETE":
            requests_response = requests.delete(
                full_endpoint_url, headers={"Authorization": f"{bearer_token}"}
            )
            requests_request = requests.Request(
                "delete",
                full_endpoint_url,
                headers={"Authorization": f"{bearer_token}"},
            )
        # if both payload and bearer token are None, it can only be a simple get
    else:
        requests_response = requests.get(full_endpoint_url)
        requests_request = requests.Request("get", full_endpoint_url)

    openapi_request = RequestsOpenAPIRequest(requests_request)
    openapi_response = RequestsOpenAPIResponse(requests_response)

    try:
        if check_status_code(expected_status_codes, openapi_response.status_code):
            validate_response(
                openapi_request, openapi_response, spec=spec, cls=V30ResponseValidator
            )
        else:
            raise UnexpectedStatusCodeException(
                endpoint=full_endpoint_url,
                expected_status_code=expected_status_codes,
                actual_status_code=openapi_response.status_code,
                auth=(bearer_token is not None),
            )
    except Exception as e:
        print_test_results(e, endpoint_path=endpoint_path, test_name=test_name)
        if return_response:
            return check_test_results(e), requests_response
        else:
            return check_test_results(e)
    else:
        if return_response:
            return "", requests_response
        else:
            return ""


def check_status_code(
    expected_status_codes: Union[list[int], int], actual_status_code: int
):
    if isinstance(expected_status_codes, int):
        return actual_status_code == expected_status_codes
    return actual_status_code in expected_status_codes


class UnexpectedStatusCodeException(Exception):
    def __init__(self, endpoint, expected_status_code, actual_status_code, auth):
        self.endpoint = endpoint
        self.expected_status_code = expected_status_code
        self.actual_status_code = actual_status_code
        self.auth = auth
        self.message = f'Unexpected status code for endpoint "{endpoint}": Expected {expected_status_code}, but received {actual_status_code}.'
        super().__init__(self.message)


def get_batch_job_status(base_url: str, bearer_token: str, job_id: str):
    return json.loads(
        requests.get(
            f"{base_url}/jobs/{job_id}", headers={"Authorization": f"{bearer_token}"}
        ).content
    )["status"]


def wait_job_statuses(
    base_url: str,
    bearer_token: str,
    job_ids: list[str],
    job_statuses: list[str],
    timeout: int = 10,
):
    """
    waits for jobs status to reach one of job_statuses, or times out after {timeout} seconds

    returns True if all jobs have reached desired status
    returns False if timeout has been reached
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        all_jobs_finished = True
        for job_id in job_ids:
            if all_jobs_finished:
                all_jobs_finished = (
                    get_batch_job_status(
                        base_url=base_url, bearer_token=bearer_token, job_id=job_id
                    )
                    in job_statuses
                )
            else:
                break
            if all_jobs_finished:
                print("All jobs have reached their desired status.")
                return True
        time.sleep(1)
        print("Waiting on jobs to reach desired status..")
    print("Jobs failed to reach desired state, timeout has been reached.")
    return False


def print_test_results(e: Exception, endpoint_path: str, test_name: str = "?"):
    """
    prints the results of a openapi-core validation test

    e: the exception that was raised as a part of the response validation test
    test_name: the name of the test that ought to be displayed
    """
    print("")
    print("------------------------------------------")
    print(
        f'Validation Errors from path: "{endpoint_path}" Path description: {test_name}'
    )

    # message is important
    if type(e) is UnexpectedStatusCodeException:
        print("")
        print(e.message)
        if e.auth and (e.actual_status_code == 500):
            print(
                "Bearer-Token invalid/no longer valid or if endpoint expects an id the item does not exist."
            )
        elif e.actual_status_code == 500:
            print("Endpoint expects an id and the item does not exist.")
        elif e.actual_status_code == 404 or e.actual_status_code == 501:
            print("Endpoint is not implemented, only an error if it is REQUIRED.")
        elif e.actual_status_code == 410:
            print(
                "Endpoint is not providing requested resource as it is gone. Logs are not provided if job is queued or created."
            )
        else:
            print(f"Some other unexpected error code. {e.actual_status_code}")
    # json_path and message are important
    elif hasattr(e.__cause__, "schema_errors"):
        errors = e.__cause__.schema_errors
        for error in errors:
            print("")
            print(error.message)
            print(error.json_path)
    else:
        print(e)
    print("------------------------------------------")
    print("")


def check_test_results(e: Exception):
    """
    prints the results of a openapi-core validation test

    e: the exception that was raised as a part of the response validation test
    test_name: the name of the test that ought to be displayed
    """

    # message is important

    fail_log = ""
    if type(e) is UnexpectedStatusCodeException:
        if e.auth and (e.actual_status_code == 500):
            fail_log = "Bearer-Token invalid/no longer valid or if endpoint expects an id the item does not exist."
        elif e.actual_status_code == 500:
            fail_log = "Endpoint expects an id and the item does not exist."
        elif e.actual_status_code == 404 or e.actual_status_code == 501:
            fail_log = "Endpoint is not implemented, only an error if it is REQUIRED."
        elif e.actual_status_code == 410:
            fail_log = "Endpoint is not providing requested resource as it is gone. Logs are not provided if job is queued or created."
        else:
            fail_log = f"Some other unexpected error code. {e.actual_status_code}"
    # json_path and message are important
    elif hasattr(e.__cause__, "schema_errors"):
        errors = e.__cause__.schema_errors
        for error in errors:
            fail_log += f"Message: {error.message} Json_path: {error.json_path} \n"
    else:
        fail_log = str(e)

    return fail_log


# THIS IS A WORKAROUND,
# this can be removed IF the cause of ServerNotFound Exception has been fixed
def adjust_server_in_json(path_to_json, endpoint):
    with open(path_to_json, "r") as file:
        data = json.load(file)

    if "servers" in data and isinstance(data["servers"], list):
        for server in data["servers"]:
            if "url" in server and isinstance(server["url"], str):
                server["url"] = endpoint
    return data


def adjust_spec_json(path_to_json: str, endpoint: str, domain: str):
    data = adjust_server_in_json(path_to_json=path_to_json, endpoint=endpoint)
    data = adjust_server_in_well_known_json(data=data, endpoint=domain)
    return Spec.from_dict(data, validator=None)


def adjust_server_in_well_known_json(data, endpoint):
    data["paths"]["/.well-known/openeo"]["get"]["servers"][0]["url"] = endpoint

    return data


def validate_uri(value):
    return True


extra_format_validators = {
    "uri": validate_uri,
}


def unmarshal_commonmark(value):
    return value


extra_format_unmarshallers = {
    "commonmark": unmarshal_commonmark,
}


def get_examples_path():
    return os.path.join(
        os.getcwd(), "src/openeo_test_suite/tests/general/payload_examples"
    )


def get_spec_path_json():
    return os.path.join(os.getcwd(), "src/openeo_test_suite/tests/general/openapi.json")


def load_payloads_from_directory(directory_path: str) -> list[dict]:
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r") as file:
                try:
                    # Load the JSON data from the file
                    data = json.load(file)
                    yield json.dumps(data)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {filename}")
                except Exception as e:
                    print(f"Error reading file: {filename} - {str(e)}")


def set_uuid_in_job(json_data):
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    # Generate a new UUID
    new_id = str(uuid.uuid4().hex)
    # Set the 'id' field to the generated UUID
    json_data["process"]["id"] = new_id
    # Return the modified JSON object
    return new_id, json.dumps(json_data)


def delete_id_resource(
    base_url: str, endpoint_path: str, bearer_token: str, ids: list[str]
):
    try:
        for id in ids:
            requests.delete(
                f"{base_url}/{endpoint_path}/{id}",
                headers={"Authorization": f"{bearer_token}"},
            )
    except Exception as e:
        print(e)


def put_process_graphs(base_url: str, bearer_token: str):  # TODO id and so forth
    directory_path = get_examples_path()
    examples_directory = "put_process_graphs"

    created_udp_ids = []
    payloads = load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}"
    )

    try:
        for payload in payloads:
            id = str(uuid.uuid4().hex)
            created_udp_ids.append(id)
            requests.put(
                f"{base_url}/process_graphs/{id}",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"{bearer_token}",
                },
            )
    except Exception as e:
        print(e)
    return created_udp_ids


def set_uuid_in_udp(json_data):
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    # Generate a new UUID
    new_id = str(uuid.uuid4().hex)
    # Set the 'id' field to the generated UUID
    json_data["id"] = new_id
    # Return the modified JSON object
    return new_id, json.dumps(json_data)


def post_jobs(base_url: str, bearer_token: str):
    endpoint_path = "jobs"
    directory_path = get_examples_path()
    examples_directory = "post_jobs"

    created_batch_job_ids = []

    payloads = load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}"
    )
    full_endpoint_url = f"{base_url}{endpoint_path}"

    # TESTING
    for payload in payloads:
        _, payload = set_uuid_in_job(payload)

        response = requests.post(
            full_endpoint_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"{bearer_token}",
            },
        )
        created_batch_job_ids.append(response.headers["OpenEO-Identifier"])

    return created_batch_job_ids


def post_start_jobs(base_url: str, bearer_token: str):
    created_batch_job_ids = post_jobs(base_url=base_url, bearer_token=bearer_token)

    endpoint_path = "jobs"
    endpoint_path_extra = "results"

    for job_id in created_batch_job_ids:
        full_endpoint_url = f"{base_url}/{endpoint_path}/{job_id}/{endpoint_path_extra}"
        requests.post(full_endpoint_url, headers={"Authorization": f"{bearer_token}"})

    wait_job_statuses(
        base_url=base_url,
        bearer_token=bearer_token,
        job_ids=created_batch_job_ids,
        job_statuses=["running"],
        timeout=60,
    )
    return created_batch_job_ids


def cancel_delete_jobs(base_url: str, bearer_token: str, job_ids: list[str]):
    """
    Deletes and cancels all jobs with the given ids
    """

    endpoint_path = "jobs"

    for job_id in job_ids:
        full_endpoint_url = f"{base_url}/{endpoint_path}/{job_id}"
        requests.delete(full_endpoint_url, headers={"Authorization": f"{bearer_token}"})


def process_list_generator(filename: str):
    with open(filename, "r") as file:
        data = json.load(file)
        for item in data:
            yield item


def get_process_list(base_url: str):
    endpoint_path = "processes"

    full_endpoint_url = f"{base_url}/{endpoint_path}"

    return json.loads(requests.get(full_endpoint_url).content)["processes"]


def get_access_token(pytestconfig):
    backend = get_backend_under_test()

    capmanager = pytestconfig.pluginmanager.getplugin("capturemanager")
    with capmanager.global_and_fixture_disabled():
        backend.connection.authenticate_oidc()
    # load_dotenv("..")
    if hasattr(backend.connection.auth, "bearer"):
        return backend.connection.auth.bearer
    return None


from urllib.parse import urlparse, urlunparse


def get_domain(request):
    url = get_backend_url(request.config)
    parsed_url = urlparse(url)
    # Reconstruct the URL with scheme and netloc only.
    return urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", ""))


def get_version(request):
    url = get_backend_url(request.config)
    parsed_url = urlparse(url)
    # Split the path and filter for the segment starting with 'openeo/' and having a version number format.
    for segment in parsed_url.path.split("/"):
        if segment.startswith("openeo") and len(segment.split("/")) > 1:
            return segment + "/"
    return ""


def get_base_url(request):
    url = get_backend_url(request.config)
    parsed_url = urlparse(url)
    # If the scheme is missing, add 'https://'.
    if not parsed_url.scheme:
        url = "https://" + url
    # If the path is missing or doesn't contain 'openeo', query the '.well-known' endpoint. this is a failsafe.
    if not parsed_url.path or "openeo" not in parsed_url.path:
        requests_response = requests.get(url + "/.well-known/openeo")
        data = json.loads(requests_response.content)
        url = data["versions"][-1]["url"]
    return url
