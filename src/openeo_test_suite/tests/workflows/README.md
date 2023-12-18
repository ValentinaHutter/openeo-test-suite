Tests for validation of full process graphs.


Notes:

Before running the tests, it is necessary to modify the t_dim and b_dim fixtures to reflect the back-end naming convention.

VITO https://openeo.vito.be/openeo/1.2/:
```
export OPENEO_BACKEND_URL=https://openeo.vito.be/openeo/1.2/
unset OPENEO_AUTH_METHOD
```

1. 1. Unocmment line to use "https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE" in [conftest.py](https://github.com/Open-EO/openeo-test-suite/blob/main/src/openeo_test_suite/tests/workflows/conftest.py). t_dim = "t", b_dim="bands", the dimension names are given default names and not the ones specififed in the metadata. This STAC Collection matches the default naming convention and lets the tests to run: https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE
2. When specifying a spatial_extent in WGS84 in load_stac, the returned area is much bigger than expected, works fine with the original data projection (EPSG:32632). This makes the returned data size large and slow down all the requests (see time below).
3. If not specifying a spatial_extent, the returned data has a no data padding that make it slightly larger.
3. VITO returns always a netCDF that has to be decoded as an xarray.Dataset. This makes the test where the bands dim (NDVI) is reduced to fail, since the result contain always a band (with default name "var")
4. An old discussion about apply_dimension: https://discuss.eodc.eu/t/quantiles-with-apply-dimension/481/2

`========= 3 failed, 7 passed, 1 warning, 1 error in 269.97s (0:04:29) ==========`

EURAC https://dev.openeo.eurac.edu:
```
export OPENEO_BACKEND_URL=https://dev.openeo.eurac.edu
export OPENEO_AUTH_METHOD=basic
export OPENEO_AUTH_BASIC_USERNAME=guest
export OPENEO_AUTH_BASIC_PASSWORD=changeme
```
1. Unocmment line to use "https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2" in [conftest.py](https://github.com/Open-EO/openeo-test-suite/blob/main/src/openeo_test_suite/tests/workflows/conftest.py)
t_dim = "time", b_dim="band", the dimension names are given default names and not the ones specififed in the metadata (due to stackstac, same would be for odc-stac). This STAC Collection matches the default naming convention and lets the tests to run: https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2 . Opened issues for the used libraries https://github.com/opendatacube/odc-stac/issues/136 https://github.com/gjoseph92/stackstac/issues/236
2. The loaded data has a 5 meters shift compared to the original COGs: https://github.com/gjoseph92/stackstac/issues/207
3. Clarify apply_dimension behaviour: https://github.com/Open-EO/openeo-processes-dask/issues/213

Currently, dev.openeo.eurac.edu stores the results in xarray.DataArray in the netCDFs. openeo.cloud store them as xarray.Dataset. Need to align them.

`========= 3 failed, 7 passed, 1 warning, 1 error in 10.54s ==========`

EODC https://openeo.eodc.eu/openeo/1.1.0:
```
export OPENEO_BACKEND_URL=https://openeo.eodc.eu/openeo/1.1.0
unset OPENEO_AUTH_METHOD
```

1. Internal error ` Error: local variable 'days' referenced before ...
` doesn't allow to test anything

`=========10 failed, 1 error in 32.52s ==========`
