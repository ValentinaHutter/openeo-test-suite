Tests for (individual) processes:

- tests for validation of process metadata against the [openEO API](https://openeo.org/).
- individual process testing, e.g. based on input-output examples.

Examples:

- `pytest --openeo-backend-url=https://openeo.example`
- `pytest --openeo-backend-url=http://127.0.0.1:5000/openeo/1.2/ --runner=vito-http`
- `pytest --runner=vito` - needs <https://github.com/Open-EO/openeo-python-driver> being installed
- `pytest --runner=dask` - needs optional Dask dependencies