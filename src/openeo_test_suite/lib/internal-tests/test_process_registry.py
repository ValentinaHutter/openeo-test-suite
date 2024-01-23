import pytest

from openeo_test_suite.lib.process_registry import ProcessRegistry


class TestProcessRegistry:
    @pytest.fixture(scope="class")
    def process_registry(self) -> ProcessRegistry:
        return ProcessRegistry()

    def test_get_all_processes_basic(self, process_registry):
        processes = list(process_registry.get_all_processes())
        assert len(processes) > 0

    def test_get_all_processes_add(self, process_registry):
        (add,) = [
            p for p in process_registry.get_all_processes() if p.process_id == "add"
        ]

        assert add.level == "L1"
        assert add.experimental is False
        assert add.path.name == "add.json5"
        assert len(add.tests)

        add00 = {"arguments": {"x": 0, "y": 0}, "returns": 0}
        assert add00 in add.tests

    def test_get_all_processes_divide(self, process_registry):
        (divide,) = [
            p for p in process_registry.get_all_processes() if p.process_id == "divide"
        ]

        assert divide.level == "L1"
        assert divide.experimental is False
        assert divide.path.name == "divide.json5"
        assert len(divide.tests)

        divide0 = {
            "arguments": {"x": 1, "y": 0},
            "returns": float("inf"),
            "throws": "DivisionByZero",
        }
        assert divide0 in divide.tests
