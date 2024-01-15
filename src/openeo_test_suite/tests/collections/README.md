Tests for validation of collection metadata against specs like
the [openEO API](https://openeo.org/) and [STAC](https://stacspec.org/en).

## Usage

Usage example, to only run the collection metadata tests for `$BACKEND_URL`:

```bash
pytest --openeo-backend-url=$BACKEND_URL --html=reports/collections.html -v src/openeo_test_suite/tests/collections/
```
