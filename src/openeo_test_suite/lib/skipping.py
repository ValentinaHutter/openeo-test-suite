import logging
from typing import Iterable, Iterator, List, Set, Union

import openeo
import pytest
from openeo.internal.graph_building import FlatGraphableMixin, as_flat_graph

_log = logging.getLogger(__name__)


class Skipper:
    """
    Helper class to compactly skip tests for based on
    backend capabilities and configuration.
    """

    def __init__(
        self, connection: openeo.Connection, selected_processes: Iterable[str]
    ):
        """
        :param connection: openeo connection
        :param selected_processes: list of active process selection
        """
        self._connection = connection

        self._selected_processes = set(selected_processes)

    def _get_output_formats(self) -> set:
        formats = set(
            f.lower() for f in self._connection.list_file_formats()["output"].keys()
        )
        _log.info("Detected output formats: %s", formats)
        return formats

    def skip_if_no_netcdf_support(self):
        output_formats = self._get_output_formats()
        if not output_formats.intersection({"netcdf", "nc"}):
            pytest.skip("NetCDF not supported as output file format")

    def skip_if_no_geotiff_support(self):
        output_formats = self._get_output_formats()
        if not output_formats.intersection({"geotiff", "gtiff"}):
            pytest.skip("GeoTIFF not supported as output file format")

    def _get_processes(
        self, processes: Union[str, List[str], Set[str], openeo.DataCube]
    ) -> Set[str]:
        """
        Generic process id extraction from:
        - string (single process id)
        - list/set of process ids
        - openeo.DataCube: extract process ids from process graph
        """
        if isinstance(processes, str):
            return {processes}
        elif isinstance(processes, (list, set)):
            return set(processes)
        elif isinstance(processes, openeo.DataCube):
            # TODO: wider isinstance check?
            return extract_processes_from_process_graph(processes)
        else:
            raise ValueError(processes)

    def skip_if_unselected_process(
        self, processes: Union[str, List[str], Set[str], openeo.DataCube]
    ):
        """
        Skip test if any of the provided processes is not in the active process selection.

        :param processes: single process id, list/set of process ids or an `openeo.DataCube` to extract process ids from
        """
        # TODO: automatically call this skipper from monkey-patched `cube.download()`?
        processes = self._get_processes(processes)
        unselected_processes = processes.difference(self._selected_processes)
        if unselected_processes:
            pytest.skip(f"Process selection does not cover: {unselected_processes}")

    def skip_if_unsupported_process(
        self, processes: Union[str, List[str], Set[str], openeo.DataCube]
    ):
        """
        Skip test if any of the provided processes is not supported by the backend.

        :param processes: single process id, list/set of process ids or an `openeo.DataCube` to extract process ids from
        """
        processes = self._get_processes(processes)

        # TODO: cache available processes?
        available_processes = set(p["id"] for p in self._connection.list_processes())
        unsupported_processes = processes.difference(available_processes)
        if unsupported_processes:
            pytest.skip(f"Backend does not support: {unsupported_processes}")


def extract_processes_from_process_graph(
    pg: Union[dict, FlatGraphableMixin]
) -> Set[str]:
    """Extract process ids from given process graph."""
    pg = as_flat_graph(pg)

    def extract(pg) -> Iterator[str]:
        for v in pg.values():
            yield v["process_id"]
            for arg in v["arguments"].values():
                if isinstance(arg, dict) and "process_graph" in arg:
                    yield from extract(arg["process_graph"])

    return set(extract(pg))
