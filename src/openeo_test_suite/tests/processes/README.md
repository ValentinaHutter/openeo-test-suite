# Tests for (individual) processes

- tests for validation of process metadata against the [openEO API](https://openeo.org/).
- individual process testing, e.g. based on input-output examples.

## Process Metadata tests

...

## Individual Process Testing

### Examples

- `pytest --openeo-backend-url=https://openeo.cloud --processes=min,max`
- `pytest --runner=vito --process-levels=L1,L2,L2A`
- `pytest --runner=dask`
- `pytest src/openeo_test_suite/tests/processes/processing/test_example.py --runner=dask`

### Parameters

Specify `src/openeo_test_suite/tests/processes/processing/test_example.py` to only run individual process tests.

- `--runner`: The execution engine. One of:
  - `vito` (needs <https://github.com/Open-EO/openeo-python-driver> being installed)
  - `dask` (needs optional Dask dependencies)
  - `http` (**default**, requires `--openeo-backend-url` to be set)
- `--process-levels`: All [process profiles](https://openeo.org/documentation/1.0/developers/profiles/processes.html) to test against, separated by comma. You need to list all levels explicitly, e.g., L2 does **not** include L1 automatically. Example: `L1,L2,L2A`. By default tests against all processes.
- `--processes`: A list of processes to test against, separated by comma. Example: `apply,reduce_dimension`. By default tests against all processes.

### Runners

The individual process testing ships 3 experimental runners:

- [HTTP](../../lib/process_runner/http.py) (subset of processes due to JSON limitations)
  Executes all 1000 tests via the openEO API synchronously, expect 1000+ requests to hit your back-end in a short amount of time.
- [Dask](../../lib/process_runner/dask.py) (all implemented processes)
  Executes the tests directly via the [openEO Dask implementation](https://github.com/Open-EO/openeo-processes-dask) (used by EODC, EURAC, and others)
- [VITO](../../lib/process_runner/vito.py) (subset of processes due to the underlying architecture of the back-end implementation)
  Executes the tests directly via the [openEO Python Driver implementation](https://github.com/Open-EO/openeo-python-driver) (used by CDSE, VITO, and others)

You can implement your own runner by implementing the process runner base class:
<https://github.com/Open-EO/openeo-test-suite/blob/main/src/openeo_test_suite/lib/process_runner/base.py>

See the runners above for examples.
