import xarray as xr
import pytest

LEVEL = "L3"

def test_apply_dimension_order(
    netcdf_not_supported,
    process_levels,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    
    if netcdf_not_supported:
        pytest.skip("NetCDF not supported as output file format!")

    if len(process_levels) > 0 and LEVEL not in process_levels:
        pytest.skip(f"Skipping {LEVEL} workflow because the specified levels are: {process_levels}")

    filename = tmp_path / "test_apply_dimension_order.nc"
    b_dim = collection_dims["b_dim"]

    from openeo.processes import order

    cube = cube_one_day_red_nir.apply_dimension(
        process=lambda d: order(d),
        dimension=b_dim,
    )

    cube.download(filename)
    assert filename.exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    assert len(data[b_dim]) == 2
