import datetime

import dateutil.tz
import numpy
import pandas
import pytest

from openeo_test_suite.lib.process_runner.util import (
    datetime_to_isostr,
    isostr_to_datetime,
)


@pytest.mark.parametrize(
    ["isostr", "expected"],
    [
        (
            "2020-01-02T03:04:05Z",
            datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=datetime.timezone.utc),
        ),
        (
            "2020-01-02T03:04:05",
            datetime.datetime(2020, 1, 2, 3, 4, 5),
        ),
        (
            "2020-01-02T03:04:05+00:00",
            datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=datetime.timezone.utc),
        ),
        (
            "2020-01-02T03:04:05+01:00",
            datetime.datetime(
                2020, 1, 2, 3, 4, 5, tzinfo=dateutil.tz.tzoffset(None, 3600)
            ),
        ),
    ],
)
def test_isostr_to_datetime(isostr, expected):
    assert isostr_to_datetime(isostr) == expected


def test_isostr_to_datetime_invalid():
    with pytest.raises(ValueError):
        _ = isostr_to_datetime("foobar")

    assert isostr_to_datetime("foobar", fail_on_error=False) == "foobar"


@pytest.mark.parametrize(
    ["dt", "expected"],
    [
        (
            datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=datetime.timezone.utc),
            "2020-01-02T03:04:05Z",
        ),
        (datetime.datetime(2020, 1, 2, 3, 4, 5), "2020-01-02T03:04:05"),
        (pandas.Timestamp("2020-01-02T03:04:05"), "2020-01-02T03:04:05"),
        (pandas.Timestamp("2020-01-02T03:04:05Z"), "2020-01-02T03:04:05Z"),
        (numpy.datetime64("2020-01-02T03:04:05Z"), "2020-01-02T03:04:05Z"),
        ("2020-01-02T03:04:05Z", "2020-01-02T03:04:05Z"),
    ],
)
def test_datetime_to_isostr(dt, expected):
    assert datetime_to_isostr(dt) == expected
