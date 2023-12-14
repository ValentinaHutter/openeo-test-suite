from pathlib import Path

import xarray as xr

# Currently, dev.openeo.eurac.edu stores the results in xarray.DataArray in the netCDFs
# openeo.cloud seems to store them as xarray.Dataset. Need to align them.


def test_apply(
    cube_one_day_red,
    b_dim,
    tmp_path,
):
    from openeo.processes import clip

    filename = tmp_path / "test_apply.nc"
    cube = cube_one_day_red.apply(lambda x: x.clip(0, 1))
    cube.download(filename)

    assert Path(filename).exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    assert (data.max().item(0)) == 1


def test_apply_dimension(
    cube_one_day_red_nir,
    b_dim,
    tmp_path,
):
    filename = tmp_path / "test_apply_dimension.nc"
    cube = cube_one_day_red_nir.apply_dimension(dimension=b_dim, process="max")
    cube.download(filename)

    assert Path(filename).exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    assert len(data[b_dim]) == 2
