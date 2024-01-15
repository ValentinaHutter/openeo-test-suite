import json
import logging
import re

import pytest
import requests
from stac_validator import stac_validator

_log = logging.getLogger(__name__)


# TODO #18 eliminate delayed_assert usage


class OpeneoApiCollectionTests:
    def __init__(self, collection):
        self.test_stac_version(collection)
        self.test_id(collection)
        self.test_version_and_deprecated(collection)
        self.test_cube_dimensions(collection)
        self.test_summaries(collection)
        self.test_assets(collection)

    def test_stac_version(self, collection):
        r"""
        string (stac_version) ^(0\.9.\d+|1\.\d+.\d+)

        The version of the STAC specification, which MAY
        not be equal to the STAC API version.
        Supports versions 0.9.x and 1.x.x.
        """

        delayed_assert.expect("stac_version" in collection)
        delayed_assert.expect(isinstance(collection["stac_version"], str))

        p = re.compile(r"^(0\.9.\d+|1\.\d+.\d+)")
        delayed_assert.expect(p.match(collection["stac_version"]) is not None)

    def test_id(self, collection):
        r"""
        string (collection_id) ^[\w\-\.~\/]+$

        A unique identifier for the collection, which MUST
        match the specified pattern.
        """

        delayed_assert.expect("id" in collection)
        delayed_assert.expect(isinstance(collection["id"], str))

        p = re.compile(r"^[\w\-\.~\/]+$")
        delayed_assert.expect(p.match(collection["id"]) is not None)

    def test_version_and_deprecated(self, collection):
        """
        string

        Version of the collection.

        This property REQUIRES to add version (STAC < 1.0.0-rc.1)
        or https://stac-extensions.github.io/version/v1.2.0/schema.json
        (STAC >= 1.0.0-rc.1) to the list of stac_extensions.
        """
        raise_error = False
        if "version" in collection or "deprecated" in collection:
            if "stac_extensions" not in collection:
                raise_error = True
            if collection["stac_version"][0] == "0":
                if "version" not in collection["stac_extensions"]:
                    raise_error = True
            if collection["stac_version"][0] == "1":
                if (
                    "https://stac-extensions.github.io/version/v1.2.0/schema.json"
                    not in collection["stac_extensions"]
                ):
                    raise_error = True
            if raise_error:
                _log.error(
                    f"{collection['id']}: The version and/or deprecated properties REQUIRES to add version (STAC < 1.0.0-rc.1) or https://stac-extensions.github.io/version/v1.2.0/schema.json (STAC >= 1.0.0-rc.1) to the list of stac_extensions."
                )
                delayed_assert.expect(0)

    def test_cube_dimensions(self, collection):
        """
        object (STAC Collection Cube Dimensions)

        The named default dimensions of the data cube. Names must be unique per collection.

        The keys of the object are the dimension names. For interoperability, it is RECOMMENDED to use the following dimension names if there is only a single dimension with the specified criteria:

        x for the dimension of type spatial with the axis set to x
        y for the dimension of type spatial with the axis set to y
        z for the dimension of type spatial with the axis set to z
        t for the dimension of type temporal
        bands for dimensions of type bands
        geometry for dimensions of type geometry

        This property REQUIRES to add a version of the data cube extension to the list of stac_extensions, e.g. https://stac-extensions.github.io/datacube/v2.2.0/schema.json.
        """

        delayed_assert.expect("cube:dimensions" in collection)
        delayed_assert.expect("stac_extensions" in collection)
        raise_error = True
        for stac_ext in collection["stac_extensions"]:
            if "https://stac-extensions.github.io/datacube/" in stac_ext:
                raise_error = False
                break
        if raise_error:
            _log.error(
                f"{collection['id']}: The cube:dimensions property REQUIRES to add a version of the data cube extension to the list of stac_extensions, e.g. https://stac-extensions.github.io/datacube/v2.2.0/schema.json."
            )
            delayed_assert.expect(0)

    def test_summaries(self, collection):
        """
        object (STAC Summaries (Collection Properties))

        Collection properties from STAC extensions (e.g. EO, SAR, Satellite or Scientific) or even custom extensions.

        Summaries are either a unique set of all available values, statistics or a JSON Schema. Statistics only specify the range (minimum and maximum values) by default, but can optionally be accompanied by additional statistical values. The range can specify the potential range of values, but it is recommended to be as precise as possible. The set of values MUST contain at least one element and it is strongly RECOMMENDED to list all values. It is recommended to list as many properties as reasonable so that consumers get a full overview of the Collection. Properties that are covered by the Collection specification (e.g. providers and license) SHOULD NOT be repeated in the summaries.

        Potential fields for the summaries can be found here:

            STAC Common Metadata: A list of commonly used fields throughout all domains
            Content Extensions: Domain-specific fields for domains such as EO, SAR and point clouds.
            Custom Properties: It is generally allowed to add custom fields.
        """
        delayed_assert.expect("summaries" in collection)
        delayed_assert.expect(isinstance(collection["summaries"], dict))

    def test_assets(self, collection):
        """
        object (Assets)

        Dictionary of asset objects for data that can be downloaded, each with a unique key. The keys MAY be used by clients as file names.

        Implementing this property REQUIRES to add collection-assets to the list of stac_extensions in STAC < 1.0.0-rc.1.
        """
        if "assets" in collection:
            delayed_assert.expect(isinstance(collection["assets"], dict))
            if collection["stac_version"][0] == "0":
                if "collection-assets" not in collection["stac_extensions"]:
                    _log.error(
                        f"{collection['id']}: The assets property REQUIRES to add collection-assets to the list of stac_extensions in STAC < 1.0.0-rc.1."
                    )
                    delayed_assert.expect(0)
