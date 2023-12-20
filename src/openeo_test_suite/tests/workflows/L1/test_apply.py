import xarray as xr


def test_apply(
    cube_one_day_red,
    collection_dims,
    tmp_path,
):
    filename = tmp_path / "test_apply.nc"
    cube = cube_one_day_red.apply(lambda x: x.clip(0, 1))
    cube.download(filename)

    assert filename.exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(
            dim=collection_dims["b_dim"]
        )
    assert (data.max().item(0)) == 1
