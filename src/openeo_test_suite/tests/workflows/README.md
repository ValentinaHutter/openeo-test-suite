Tests for validation of full process graphs.


Notes:

Before running the tests, it is necessary to modify the t_dim and b_dim fixtures to reflect the back-end naming convention.

VITO https://openeo.vito.be/openeo/1.2/:
```
export OPENEO_BACKEND_URL=https://openeo.vito.be/openeo/1.2/
unset OPENEO_AUTH_METHOD
```

1. t_dim = "t", b_dim="bands", same as STAC metadata (cube:dimensions)
2. When specifying a spatial_extent in WGS84 in load_stac, the returned area is much bigger than expected, works fine with the original data projection (EPSG:32632). This makes the returned data size large and slow down all the requests (see time below).
3. If not specifying a spatial_extent, the returned data has a no data padding that make it slightly larger.
3. VITO returns always a netCDF that has to be decoded as an xarray.Dataset. This makes the test where the bands dim (NDVI) is reduced to fail, since the result contain always a band (with default name "var")

`========= 2 failed, 8 passed, 1 warning in 1562.87s (0:26:02) ==========`

EURAC https://dev.openeo.eurac.edu:
```
export OPENEO_BACKEND_URL=https://dev.openeo.eurac.edu
export OPENEO_AUTH_METHOD=basic
export OPENEO_AUTH_BASIC_USERNAME=guest
export OPENEO_AUTH_BASIC_PASSWORD=changeme
```
1. t_dim = "time", b_dim="band", the dimension names are given default names and not the ones specififed in the metadata (due to stackstac, same would be for odc-stac)
2. The loaded data has a 5 meters shift compared to the original COGs
3. Clarify apply_dimension behaviour

`========= 3 failed, 7 passed, 1 warning in 9.81s ==========`

EODC https://openeo.eodc.eu/openeo/1.1.0:
```
export OPENEO_BACKEND_URL=https://openeo.eodc.eu/openeo/1.1.0
unset OPENEO_AUTH_METHOD
```

1. Internal error ` Error: local variable 'days' referenced before ...
` doesn't allow to test anything

`========= 10 failed in 13.15s ==========`
