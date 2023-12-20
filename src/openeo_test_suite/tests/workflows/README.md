# Tests for full openEO workflows (process graphs)

The tests are designed to run using [syncronous calls](https://open-eo.github.io/openeo-python-client/basics.html#download-synchronously) and a Sentinel-2 Collection.

Examples:

- `pytest --openeo-backend-url=https://openeo.dataspace.copernicus.eu/openeo/1.2 --s2-collection=https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE`
- `pytest --openeo-backend-url=https://openeo.dataspace.copernicus.eu/openeo/1.2 --s2-collection=https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE --process-levels=L1,L2,L2A`

Parameters:

- `--s2-collection`: the data collection to test against. It can be either a Sentinel-2 STAC Collection or the name of an openEO Sentinel-2 Collection provided by the back-end.
- `--process-levels`: all process profiles to test against, separated by comma. You need to list all levels explicitly, e.g., L2 does not include L1 automatically. Example: L1,L2,L2A. By default tests against all processes.


## Notes

- Only the workflows containing processes that are exposed under the `/processes` endpoint are tested. If `load_stac` is not available, the `--s2-collection` parameter must be set to an existing openEO S2 collection.

- Tests are divided by process levels, defined [here](https://openeo.org/documentation/1.0/developers/profiles/processes.html).


### VITO

```
unset OPENEO_AUTH_METHOD
pytest --openeo-backend-url=https://openeo.vito.be/openeo/1.2/ --s2-collection=https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE
```

Known issues:
1. When specifying a spatial_extent in WGS84 in load_stac, the returned area is much bigger than expected, works fine with the original data projection (EPSG:32632). This makes the returned data size large and slow down all the requests (see time below).
2. If not specifying a spatial_extent, the returned data has a no data padding that make it slightly larger.
3. VITO returns always a netCDF that has to be decoded as an xarray.Dataset. This makes the test where the bands dim (NDVI) is reduced to fail, since the result contain always a band (with default name "var")

`========= 3 failed, 7 passed, 1 warning, 1 error in 269.97s (0:04:29) ==========`

### CDSE

```
unset OPENEO_AUTH_METHOD
pytest --openeo-backend-url=https://openeo.dataspace.copernicus.eu/openeo/1.2 --s2-collection=https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE
```
Known issues:
1. Same as for VITO

### EURAC

```
export OPENEO_AUTH_METHOD=basic
export OPENEO_AUTH_BASIC_USERNAME=guest
export OPENEO_AUTH_BASIC_PASSWORD=changeme
pytest --openeo-backend-url=https://dev.openeo.eurac.edu --s2-collection=https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2
```

Known issues:
1. Opened issues for the default dimension names for the used libraries https://github.com/gjoseph92/stackstac/issues/236 (also here https://github.com/opendatacube/odc-stac/issues/136)
2. The loaded data has a 5 meters shift compared to the original COGs: https://github.com/gjoseph92/stackstac/issues/207
3. Clarify apply_dimension behaviour: https://github.com/Open-EO/openeo-processes-dask/issues/213
4. Currently, dev.openeo.eurac.edu stores the results in xarray.DataArray in the netCDFs. CDSE/VITO store them as xarray.Dataset. Need to align them?

`========= 3 failed, 7 passed, 1 warning, 1 error in 10.54s ==========`

### EODC

```
unset OPENEO_AUTH_METHOD
pytest --openeo-backend-url=https://openeo.eodc.eu/openeo/1.1.0 --s2-collection=https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2
```

Known issues:
1. Internal error ` Error: local variable 'days' referenced before ...
` doesn't allow to test anything

`========= 10 failed, 1 error in 32.52s ==========`

### SentinelHub

```
unset OPENEO_AUTH_METHOD
pytest --openeo-backend-url=https://openeo.sentinel-hub.com/production --s2-collection=SENTINEL2_L2A
```

1. `load_stac` is not supported, need to set to use SENTINEL2_L2A instead of the STAC url in conftest.py.
2. Can't run most of the tests, since they rely on netCDF output format (not supported).
3. The single test using geoTIFF as output format fails with:
```
FAILED test_load_save.py::test_load_save_geotiff - openeo.rest.OpenEoApiError: [400] ProcessGraphComplexity: The process is too complex for synchronous processing....
```

`========= 10 failed, 1 error in 13.50s ==========`


### Additional Info

The reason behind the creation of two test collections is due to the fact of non-optimal implementation of the `load_stac` process in the various back-ends.
1. CDSE and VITO load the data assigning to the temporal dimension the `t` label and to the bands dimension the `bands` label. To test this back-end it is necessary to use the https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE collection.
2. EURAC and EODC load the data assigning to the temporal dimension the `time` label and to the bands dimension the `band` label. To test this back-end it is necessary to use the https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2 collection.
