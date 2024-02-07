# Tests for full openEO workflows (process graphs)


## Development/status notes

The following notes give a snapshot of the status of the workflow tests
around the development time of this test suite module (Dec 2023).

### VITO

```bash
unset OPENEO_AUTH_METHOD
pytest --openeo-backend-url=https://openeo.vito.be/openeo/1.2/ --s2-collection=https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE
```

Known issues:
1. When specifying a spatial_extent in WGS84 in load_stac, the returned area is much bigger than expected, works fine with the original data projection (EPSG:32632). This makes the returned data size large and slow down all the requests (see time below).
2. If not specifying a spatial_extent, the returned data has a no data padding that make it slightly larger.
3. VITO returns always a netCDF that has to be decoded as an xarray.Dataset. This makes the test where the bands dim (NDVI) is reduced to fail, since the result contain always a band (with default name "var")

```
========= 3 failed, 7 passed, 1 warning, 1 error in 269.97s (0:04:29) ==========
```

### CDSE

```bash
unset OPENEO_AUTH_METHOD
pytest --openeo-backend-url=https://openeo.dataspace.copernicus.eu/openeo/1.2 --s2-collection=https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE
```
Known issues:
1. Same as for VITO

### EURAC

```bash
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

```
========= 3 failed, 7 passed, 1 warning, 1 error in 10.54s ==========
```

### EODC

```bash
unset OPENEO_AUTH_METHOD
pytest --openeo-backend-url=https://openeo.eodc.eu/openeo/1.1.0 --s2-collection=https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2
```

Known issues:
1. Internal error ` Error: local variable 'days' referenced before ...
` doesn't allow to test anything

```
========= 10 failed, 1 error in 32.52s ==========
```

### SentinelHub

```bash
unset OPENEO_AUTH_METHOD
pytest --openeo-backend-url=https://openeo.sentinel-hub.com/production --s2-collection=SENTINEL2_L2A
```

1. `load_stac` is not supported, need to set to use SENTINEL2_L2A openEO Collection of the STAC url in conftest.py.
2. Can't run most of the tests, since they rely on netCDF output format (not supported).
3. The single test using geoTIFF as output format fails with:
```
FAILED test_load_save.py::test_load_save_geotiff - openeo.rest.OpenEoApiError: [400] ProcessGraphComplexity: The process is too complex for synchronous processing....
```

```
========= 10 failed, 1 error in 13.50s ==========
```
