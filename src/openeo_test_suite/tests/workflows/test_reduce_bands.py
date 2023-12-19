import xarray as xr


def test_ndvi_index(
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    filename = tmp_path / "test_ndvi_index.nc"
    b_dim = collection_dims["b_dim"]

    def compute_ndvi(data):
        from openeo.processes import array_element

        red = data.array_element(index=0)
        nir = data.array_element(index=1)
        return (nir - red) / (nir + red)

    ndvi = cube_one_day_red_nir.reduce_dimension(dimension=b_dim, reducer=compute_ndvi)
    ndvi.download(filename)

    assert filename.exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    assert len(data.dims) == 3  # 2 spatial + 1 temporal


# Fails if array_index + label is not supported
def test_ndvi_label(
    cube_one_day_red_nir,
    collection_dims,
    tmp_path,
):
    filename = tmp_path / "test_ndvi_label.nc"
    b_dim = collection_dims["b_dim"]

    def compute_ndvi(data):
        red = data.array_element(label="B04")
        nir = data.array_element(label="B08")
        return (nir - red) / (nir + red)

    ndvi = cube_one_day_red_nir.reduce_dimension(dimension=b_dim, reducer=compute_ndvi)
    ndvi.download(filename)

    assert filename.exists()
    try:
        data = xr.open_dataarray(filename)
    except ValueError:
        data = xr.open_dataset(filename, decode_coords="all").to_dataarray(dim=b_dim)
    assert len(data.dims) == 3  # 2 spatial + 1 temporal
