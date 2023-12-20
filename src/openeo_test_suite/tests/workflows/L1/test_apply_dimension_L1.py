import xarray as xr


def test_apply_dimension_quantiles_0(
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    filename = tmp_path / "test_apply_dimension_quantiles_0.nc"
    b_dim = collection_dims["b_dim"]
    t_dim = collection_dims["t_dim"]

    from openeo.processes import quantiles

    cube = cube_one_day_red_nir.apply_dimension(
        process=lambda d: quantiles(d, [0.25, 0.5, 0.75]),
        dimension=b_dim,
    )

    cube.download(filename)
    assert filename.exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    assert len(data[b_dim]) == 3


def test_apply_dimension_quantiles_1(
    cube_red_nir,
    collection_dims,
    tmp_path,
):
    filename = tmp_path / "test_apply_dimension_quantiles_1.nc"
    b_dim = collection_dims["b_dim"]
    t_dim = collection_dims["t_dim"]

    from openeo.processes import quantiles

    cube = cube_red_nir.apply_dimension(
        process=lambda d: quantiles(d, [0.25, 0.5, 0.75]),
        dimension=t_dim,
        target_dimension=b_dim
    )

    cube.download(filename)
    assert filename.exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    assert len(data[b_dim]) == 3