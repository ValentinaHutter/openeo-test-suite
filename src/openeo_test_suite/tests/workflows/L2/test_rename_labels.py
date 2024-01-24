from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray


def test_rename_labels_bands(
    skipper,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()

    filename = tmp_path / "test_rename_labels_bands.nc"
    b_dim = collection_dims["b_dim"]

    renamed_cube = cube_one_day_red_nir.rename_labels(
        dimension=b_dim, source=["B04", "B08"], target=["red", "nir"]
    )
    skipper.skip_if_unselected_process(renamed_cube)
    renamed_cube.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 4  # 2 spatial + 1 temporal + 1 bands
    assert b_dim in data.dims
    assert data[b_dim].values[0] == "red"
    assert data[b_dim].values[1] == "nir"


def test_rename_labels_time(
    skipper,
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()

    filename = tmp_path / "test_rename_labels_time.nc"
    t_dim = collection_dims["t_dim"]
    b_dim = collection_dims["b_dim"]

    t_labels = cube_one_day_red_nir.dimension_labels(dimension=t_dim)
    renamed_cube = cube_one_day_red_nir.rename_labels(
        dimension=t_dim, source=t_labels, target=["first_date"]
    )
    skipper.skip_if_unselected_process(renamed_cube)
    renamed_cube.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 4  # 2 spatial + 1 temporal + 1 bands
    assert t_dim in data.dims
    assert data[t_dim].values == ["first_date"]
