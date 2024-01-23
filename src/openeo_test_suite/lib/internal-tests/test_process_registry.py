import pytest

from openeo_test_suite.lib.process_registry import ProcessRegistry


class TestProcessRegistry:
    # Some example processes for some levels
    PROCESS_EXAMPLES_L1 = ["add", "divide", "apply_dimension", "reduce_dimension"]
    PROCESS_EXAMPLES_L2 = ["aggregate_temporal", "if"]
    PROCESS_EXAMPLES_L3 = ["apply_neighborhood", "merge_cubes"]
    PROCESS_EXAMPLES_EXPERIMENTAL = ["apply_polygon"]

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

    def test_get_processes_filtered_default(self, process_registry):
        pids = [p.process_id for p in process_registry.get_processes_filtered()]
        assert len(pids) > 100
        for pid in (
            self.PROCESS_EXAMPLES_L1
            + self.PROCESS_EXAMPLES_L2
            + self.PROCESS_EXAMPLES_L3
        ):
            assert pid in pids
        for pid in self.PROCESS_EXAMPLES_EXPERIMENTAL:
            assert pid not in pids

    def test_get_processes_filtered_with_process_ids(self, process_registry):
        pids = [
            p.process_id
            for p in process_registry.get_processes_filtered(
                process_ids=["add", "divide"]
            )
        ]
        assert sorted(pids) == ["add", "divide"]

    def test_get_processes_filtered_with_process_levels(self, process_registry):
        pids_l1 = [
            p.process_id
            for p in process_registry.get_processes_filtered(process_levels=["L1"])
        ]
        pids_l23 = [
            p.process_id
            for p in process_registry.get_processes_filtered(
                process_levels=["L2", "L3"]
            )
        ]
        for pid in self.PROCESS_EXAMPLES_L1:
            assert pid in pids_l1
            assert pid not in pids_l23
        for pid in self.PROCESS_EXAMPLES_L2:
            assert pid not in pids_l1
            assert pid in pids_l23
        for pid in self.PROCESS_EXAMPLES_L3:
            assert pid not in pids_l1
            assert pid in pids_l23
        for pid in self.PROCESS_EXAMPLES_EXPERIMENTAL:
            assert pid not in pids_l1
            assert pid not in pids_l23

    def test_get_processes_filtered_with_process_ids_and_levels(self, process_registry):
        pids = [
            p.process_id
            for p in process_registry.get_processes_filtered(
                process_ids=["min", "max"], process_levels=["L2"]
            )
        ]
        for pid in ["min", "max"] + self.PROCESS_EXAMPLES_L2:
            assert pid in pids
        for pid in (
            self.PROCESS_EXAMPLES_L1
            + self.PROCESS_EXAMPLES_L3
            + self.PROCESS_EXAMPLES_EXPERIMENTAL
        ):
            assert pid not in pids

    def test_get_processes_filtered_with_experimental(self, process_registry):
        pids = [
            p.process_id
            for p in process_registry.get_processes_filtered(
                process_ids=["min", "max"], process_levels=["L3"], experimental=True
            )
        ]
        for pid in ["min", "max"] + self.PROCESS_EXAMPLES_L3:
            assert pid in pids
        for pid in self.PROCESS_EXAMPLES_EXPERIMENTAL:
            assert pid in pids
