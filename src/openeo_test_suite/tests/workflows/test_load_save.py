from pathlib import Path

import numpy as np
import rioxarray
import xarray as xr

# import openeo_processes_dask


def test_load_save_netcdf(
    cube_full_extent,
    b_dim,
    tmp_path,
):
    filename = tmp_path / "test_load_save_netcdf.nc"
    cube_full_extent.download(filename)

    assert Path(filename).exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    assert len(data.dims) == 4


def test_load_save_10x10_netcdf(
    cube_red_10x10,
    b_dim,
    tmp_path,
):
    filename = tmp_path / "test_load_save_10x10_netcdf.nc"
    cube_red_10x10.download(filename)

    assert Path(filename).exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    # print(data.openeo.x_dim)
    assert (
        len(data.dims) == 4
    )  # TODO: use xarray accessor from openeo_processes_dask to get dim names
    assert np.prod(data.shape) == 100


# The next test will fail if the back-end allows to store only 3D (x,y,bands) cubes to geoTIFF
# In this test, only a single acquisition in time should be loaded
def test_load_save_geotiff(cube_one_day_red, tmp_path):
    filename = tmp_path / "test_load_save_geotiff.tiff"
    cube_one_day_red.download(filename)

    assert Path(filename).exists()
    assert (
        len(rioxarray.open_rasterio(filename).dims) >= 3
    )  # 2 spatial + 1 band + (maybe) 1 time
    # TODO: check if the content matches the requested AOI! With VITO works with orginal CRS but not with lat/lon (as in this case)
