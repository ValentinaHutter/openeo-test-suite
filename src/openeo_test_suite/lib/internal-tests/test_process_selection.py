from openeo_test_suite.lib.process_selection import csv_to_list, get_selected_processes


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


def test_get_selected_processes_caching():
    processes = get_selected_processes()
    assert len(processes) > 0

    processes2 = get_selected_processes()
    assert processes2 is processes
    assert len(processes2) > 0
