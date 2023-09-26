
# openEO Test Suite

Test suite for validation of openEO back-ends against the openEO API and related specifications.



## Running the test suite

The test suite at least requires an openEO backend URL to run against.
It can be specified through a `pytest` command line option

    pytest --openeo-backend-url=openeo.example

or through an environment variable `OPENEO_BACKEND_URL`

    export OPENEO_BACKEND_URL=openeo.example
    pytest

If no explicit protocol is specified, `https://` will be assumed automatically.
