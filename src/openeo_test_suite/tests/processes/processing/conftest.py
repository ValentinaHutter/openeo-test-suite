import openeo
import pytest


@pytest.fixture
def auto_authenticate() -> bool:
    # Automatically authenticate the connection fixture for all tests under this folder
    return True
