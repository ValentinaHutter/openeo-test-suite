# openEO tests for validation of full process graphs.

## Introduction

The tests are designed to run using [syncronous calls](https://open-eo.github.io/openeo-python-client/basics.html#download-synchronously) and a test collection available here: https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE . The same collection is provided with different temporal and bands dimension labels here: https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2 .
The reason behind the creation of two test collections is due to the fact of non-optimal implementation of the `load_stac` process in the various back-ends.
1. CDSE and VITO load the data assigning to the temporal dimension the `t` label and to the bands dimension the `bands` label. To test this back-end it is necessary to use the https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE collection.
2. EURAC and EODC load the data assigning to the temporal dimension the `time` label and to the bands dimension the `band` label. To test this back-end it is necessary to use the https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2 collection.

### Notes:

Before running the tests, it is necessary to modify the s2_collection fixture in conftest.py, depending on the load_stac availability and the back-end naming conventions.


### VITO

Uncomment line to use https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE in [conftest.py](https://github.com/Open-EO/openeo-test-suite/blob/main/src/openeo_test_suite/tests/workflows/conftest.py).

```
export OPENEO_BACKEND_URL=https://openeo.vito.be/openeo/1.2/
unset OPENEO_AUTH_METHOD
pytest
```

Known issues:
1. When specifying a spatial_extent in WGS84 in load_stac, the returned area is much bigger than expected, works fine with the original data projection (EPSG:32632). This makes the returned data size large and slow down all the requests (see time below).
2. If not specifying a spatial_extent, the returned data has a no data padding that make it slightly larger.
3. VITO returns always a netCDF that has to be decoded as an xarray.Dataset. This makes the test where the bands dim (NDVI) is reduced to fail, since the result contain always a band (with default name "var")

`========= 3 failed, 7 passed, 1 warning, 1 error in 269.97s (0:04:29) ==========`

### CDSE

Uncomment line to use https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE in [conftest.py](https://github.com/Open-EO/openeo-test-suite/blob/main/src/openeo_test_suite/tests/workflows/conftest.py).

```
export OPENEO_BACKEND_URL=https://openeo.dataspace.copernicus.eu/openeo/1.2
unset OPENEO_AUTH_METHOD
pytest
```
Known issues:
1. Same as for VITO

### EURAC

Uncomment line to use https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2 in [conftest.py](https://github.com/Open-EO/openeo-test-suite/blob/main/src/openeo_test_suite/tests/workflows/conftest.py).

```
export OPENEO_BACKEND_URL=https://dev.openeo.eurac.edu
export OPENEO_AUTH_METHOD=basic
export OPENEO_AUTH_BASIC_USERNAME=guest
export OPENEO_AUTH_BASIC_PASSWORD=changeme
pytest
```

Known issues:
1. Opened issues for the default dimension names for the used libraries https://github.com/gjoseph92/stackstac/issues/236 (also here https://github.com/opendatacube/odc-stac/issues/136)
2. The loaded data has a 5 meters shift compared to the original COGs: https://github.com/gjoseph92/stackstac/issues/207
3. Clarify apply_dimension behaviour: https://github.com/Open-EO/openeo-processes-dask/issues/213
4. Currently, dev.openeo.eurac.edu stores the results in xarray.DataArray in the netCDFs. CDSE/VITO store them as xarray.Dataset. Need to align them?

`========= 3 failed, 7 passed, 1 warning, 1 error in 10.54s ==========`

### EODC

Uncomment line to use https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2 in [conftest.py](https://github.com/Open-EO/openeo-test-suite/blob/main/src/openeo_test_suite/tests/workflows/conftest.py).

```
export OPENEO_BACKEND_URL=https://openeo.eodc.eu/openeo/1.1.0
unset OPENEO_AUTH_METHOD
pytest
```

Known issues:
1. Internal error ` Error: local variable 'days' referenced before ...
` doesn't allow to test anything

`========= 10 failed, 1 error in 32.52s ==========`

### SentinelHub

Uncomment line to use SENTINEL2_L2A instead of the STAC url in [conftest.py](https://github.com/Open-EO/openeo-test-suite/blob/main/src/openeo_test_suite/tests/workflows/conftest.py).

```
export OPENEO_BACKEND_URL=https://openeo.sentinel-hub.com/production
unset OPENEO_AUTH_METHOD
pytest
```

1. `load_stac` is not supported, need to set to use SENTINEL2_L2A instead of the STAC url in conftest.py.
2. Can't run most of the tests, since they rely on netCDF output format (not supported).
3. The single test using geoTIFF as output format fails with:
```
FAILED test_load_save.py::test_load_save_geotiff - openeo.rest.OpenEoApiError: [400] ProcessGraphComplexity: The process is too complex for synchronous processing....
```

`========= 10 failed, 1 error in 13.50s ==========`
