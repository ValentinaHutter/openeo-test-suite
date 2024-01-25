from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray


def test_reduce_time(
    skipper,
    cube_red_nir,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()

    filename = tmp_path / "test_reduce_time.nc"
    b_dim = collection_dims["b_dim"]
    t_dim = collection_dims["t_dim"]

    cube = cube_red_nir.reduce_dimension(dimension=t_dim, reducer="mean")
    skipper.skip_if_unselected_process(cube)
    cube.download(filename)

    assert filename.exists()
    data = load_netcdf_dataarray(filename, band_dim_name=b_dim)

    assert len(data.dims) == 3  # 2 spatial + 1 band
