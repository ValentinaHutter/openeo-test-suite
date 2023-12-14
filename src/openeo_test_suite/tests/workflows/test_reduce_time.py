import xarray as xr


def test_reduce_time(
    cube_red_nir,
    t_dim,
    b_dim,
    tmp_path,
):
    filename = tmp_path / "test_reduce_time.nc"

    cube = cube_red_nir.reduce_dimension(dimension=t_dim, reducer="mean")
    cube.download(filename)

    assert filename.exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    assert len(data.dims) == 3  # 2 spatial + 1 band


def test_reduce_time_merge(
    cube_red_nir,
    t_dim,
    b_dim,
    tmp_path,
):
    filename = tmp_path / "test_reduce_time_merge.nc"

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
