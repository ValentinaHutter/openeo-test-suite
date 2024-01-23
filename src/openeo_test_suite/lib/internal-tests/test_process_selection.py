from openeo_test_suite.lib.process_selection import csv_to_list


def test_csv_to_list():
    assert csv_to_list() == []
    assert csv_to_list("") == []
    assert csv_to_list("   ") == []
    assert csv_to_list(" ,  ") == []
    assert csv_to_list("foo") == ["foo"]
    assert csv_to_list("foo,bar,baz") == ["foo", "bar", "baz"]
    assert csv_to_list(",foo,bar,baz,") == ["foo", "bar", "baz"]
    assert csv_to_list("  ,foo , bar,  baz , ") == ["foo", "bar", "baz"]
    assert csv_to_list("  ,foo ,,, bar, , baz , ") == ["foo", "bar", "baz"]


def test_csv_to_list_none_on_empty():
    assert csv_to_list(none_on_empty=True) is None
    assert csv_to_list("", none_on_empty=True) is None
    assert csv_to_list("   ", none_on_empty=True) is None
    assert csv_to_list(" ,  ", none_on_empty=True) is None
