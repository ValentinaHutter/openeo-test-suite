import xarray as xr


def test_reduce_time(
    cube_red_nir,
    collection_dims,
    tmp_path,
):
    filename = tmp_path / "test_reduce_time.nc"
    b_dim = collection_dims["b_dim"]
    t_dim = collection_dims["t_dim"]

    cube = cube_red_nir.reduce_dimension(dimension=t_dim, reducer="mean")
    cube.download(filename)

    assert filename.exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    assert len(data.dims) == 3  # 2 spatial + 1 band
