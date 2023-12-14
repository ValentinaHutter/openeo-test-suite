import numpy as np
import openeo
import pytest


@pytest.fixture
def auto_authenticate() -> bool:
    """
    Fixture to act as parameterizable toggle for authenticating the connection fixture.
    Allows per-test/folder configuration of auto-authentication.
    """
    return True


@pytest.fixture
def use_stac() -> bool:
    """
    Fixture to act as parameterizable toggle for authenticating the connection fixture.
    Allows per-test/folder configuration of auto-authentication.
    """
    return True


@pytest.fixture
def cube_one_day_red(
    connection,
    bounding_box,
    temporal_interval_one_day,
    use_stac,
    s2_collection,
    s2_stac_url,
) -> dict:
    if use_stac:
        cube = connection.load_stac(
            url=s2_stac_url,
            spatial_extent=bounding_box,
            temporal_extent=temporal_interval_one_day,
            bands=["B04"],
        )
    else:
        cube = connection.load_collection(
            s2_collection,
            spatial_extent=bounding_box,
            temporal_extent=temporal_interval_one_day,
            bands=["B04"],
        )
    return cube


@pytest.fixture
def cube_one_day_red_nir(
    connection,
    bounding_box,
    temporal_interval_one_day,
    use_stac,
    s2_collection,
    s2_stac_url,
) -> dict:
    if use_stac:
        cube = connection.load_stac(
            url=s2_stac_url,
            spatial_extent=bounding_box,
            temporal_extent=temporal_interval_one_day,
            bands=["B04", "B08"],
        )
    else:
        cube = connection.load_collection(
            s2_collection,
            spatial_extent=bounding_box,
            temporal_extent=temporal_interval_one_day,
            bands=["B04", "B08"],
        )
    return cube


@pytest.fixture
def cube_red_nir(
    connection,
    bounding_box,
    temporal_interval,
    use_stac,
    s2_collection,
    s2_stac_url,
) -> dict:
    if use_stac:
        cube = connection.load_stac(
            url=s2_stac_url,
            spatial_extent=bounding_box,
            temporal_extent=temporal_interval,
            bands=["B04", "B08"],
        )
    else:
        cube = connection.load_collection(
            s2_collection,
            spatial_extent=bounding_box,
            temporal_extent=temporal_interval,
            bands=["B04", "B08"],
        )
    return cube


@pytest.fixture
def cube_red_10x10(
    connection,
    bounding_box_32632_10x10,
    temporal_interval_one_day,
    use_stac,
    s2_collection,
    s2_stac_url,
) -> dict:
    if use_stac:
        cube = connection.load_stac(
            url=s2_stac_url,
            spatial_extent=bounding_box_32632_10x10,
            temporal_extent=temporal_interval_one_day,
            bands=["B04"],
        )
    else:
        cube = connection.load_collection(
            s2_collection,
            spatial_extent=bounding_box_32632_10x10,
            temporal_extent=temporal_interval_one_day,
            bands=["B04"],
        )
    return cube


@pytest.fixture
def cube_full_extent(
    connection,
    temporal_interval,
    use_stac,
    s2_collection,
    s2_stac_url,
) -> dict:
    if use_stac:
        cube = connection.load_stac(
            url=s2_stac_url,
            temporal_extent=temporal_interval,
        )
    else:
        cube = connection.load_collection(
            s2_collection,
            temporal_extent=temporal_interval,
        )
    return cube


@pytest.fixture
def bounding_box(
    west=10.342, east=11.352, south=46.490, north=46.495, crs="EPSG:4326"
) -> dict:
    spatial_extent = {
        "west": west,
        "east": east,
        "south": south,
        "north": north,
        "crs": crs,
    }
    return spatial_extent


@pytest.fixture
def bounding_box_32632_10x10(
    west=680000, east=680100, south=5151500, north=5151600, crs="EPSG:32632"
) -> dict:
    spatial_extent = {
        "west": west,
        "east": east,
        "south": south,
        "north": north,
        "crs": crs,
    }
    return spatial_extent


@pytest.fixture
def temporal_interval():
    return ["2022-06-01", "2022-07-01"]


@pytest.fixture
def temporal_interval_one_day():
    return ["2022-06-01", "2022-06-03"]


@pytest.fixture
def s2_stac_url():
    return "https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE"


@pytest.fixture
def s2_collection():
    return "SENTINEL2_L2A"


# TODO: the dimension names are back-end specific, even though they should be the ones from the STAC metadata
@pytest.fixture
def t_dim():
    return "t"


@pytest.fixture
def b_dim():
    return "bands"
