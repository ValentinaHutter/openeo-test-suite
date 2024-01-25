import numpy as np

from openeo_test_suite.lib.workflows.io import load_netcdf_dataarray


def test_apply_kernel(
    skipper,
    cube_red_10x10,
    collection_dims,
    tmp_path,
):
    skipper.skip_if_no_netcdf_support()

    filename_0 = tmp_path / "test_apply_kernel_source.nc"
    filename_1 = tmp_path / "test_apply_kernel.nc"
    b_dim = collection_dims["b_dim"]

    blur_cube = cube_red_10x10.apply_kernel(kernel=np.ones((3, 3)), factor=1 / 9)

    skipper.skip_if_unselected_process(cube_red_10x10)
    skipper.skip_if_unselected_process(blur_cube)
    cube_red_10x10.download(filename_0)
    blur_cube.download(filename_1)

    data_source = load_netcdf_dataarray(filename_0, band_dim_name=b_dim)
    data_out = load_netcdf_dataarray(filename_1, band_dim_name=b_dim)

    assert np.isclose(np.sum(data_source[0, 0, :2, :2]) / 9, data_out[0, 0, 0, 0])
