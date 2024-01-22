from pathlib import Path
from typing import Union

import rioxarray
import xarray


def load_netcdf_dataarray(
    path: Union[str, Path],
    *,
    band_dim_name: str = "bands",
) -> xarray.DataArray:
    """Load a data cube from a NetCDF file as a xarray DataArray"""
    try:
        # TODO: avoid the try-except, and just work from `open_dataset`?
        data = xarray.open_dataarray(path)
    except ValueError:
        data = xarray.open_dataset(path, decode_coords="all")
        # VITO/CDSE write a Dataset even if there are no bands, with a default name 'var'
        if len(data.data_vars) == 1 and [v for v in data.data_vars] == ["var"]:
            data = data["var"]
        else:
            data = data.to_dataarray(dim=band_dim_name)
    return data


def load_geotiff_dataarray(
    path: Union[str, Path],
) -> xarray.DataArray:
    data = rioxarray.open_rasterio(path)
    return data
