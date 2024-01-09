import xarray as xr
import pytest

LEVEL = "L3"

def test_reduce_time_merge(
    netcdf_not_supported,
    process_levels,
    cube_red_nir,
    collection_dims,
    tmp_path,
):
        
    if netcdf_not_supported:
        pytest.skip("NetCDF not supported as output file format!")

    if len(process_levels) > 0 and LEVEL not in process_levels:
        pytest.skip(f"Skipping {LEVEL} workflow because the specified levels are: {process_levels}")

    filename = tmp_path / "test_reduce_time_merge.nc"
    b_dim = collection_dims["b_dim"]
    t_dim = collection_dims["t_dim"]

    cube_0 = cube_red_nir.reduce_dimension(dimension=t_dim, reducer="mean")
    cube_1 = cube_red_nir.reduce_dimension(dimension=t_dim, reducer="median")

    cube_merged = cube_0.merge_cubes(cube_1, overlap_resolver="subtract")
    cube_merged.download(filename)

    assert filename.exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    assert len(data.dims) == 3  # 2 spatial + 1 band
