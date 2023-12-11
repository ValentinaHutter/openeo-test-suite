import openeo
import pytest
from openeo_test_suite.lib.process_runner.base import ProcessTestRunner

@pytest.fixture
def connection(backend_url: str, runner: str, auto_authenticate: bool, capfd) -> ProcessTestRunner:
    if runner == "dask":
        from openeo_test_suite.lib.process_runner.dask import Dask
        return Dask()
    elif runner == "vito":
        from openeo_test_suite.lib.process_runner.vito import Vito
        return Vito()
    elif runner == "vito-http":
        from openeo_test_suite.lib.process_runner.vito_http import VitoHttp
        con = openeo.connect(backend_url)
        return VitoHttp(con)
    else:
        from openeo_test_suite.lib.process_runner.http import Http
        con = openeo.connect(backend_url)
        if auto_authenticate:
            with capfd.disabled():
                con.authenticate_oidc()
        
        return Http(con)