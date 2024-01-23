import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, List, Optional

import json5

import openeo_test_suite

_log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProcessData:
    """Process data, including profile level and list of tests"""

    process_id: str
    level: str
    tests: List[dict]  # TODO: also make dataclass for each test?
    experimental: bool
    path: Path


class ProcessRegistry:
    """
    Registry of processes and related tests defined in openeo-processes project
    """

    def __init__(self, root: Optional[Path] = None):
        """
        :param root: Root directory of the tests folder in  openeo-processes project
        """
        self._root = Path(
            root
            # TODO: eliminate need for this env var?
            or os.environ.get("OPENEO_TEST_SUITE_PROCESSES_TEST_ROOT")
            or self._guess_root()
        )

    def _guess_root(self):
        # TODO: avoid need for guessing and properly include assets in (installed) package
        project_root = Path(openeo_test_suite.__file__).parents[2]
        candidates = [
            project_root / "assets/processes/tests",
            Path("./assets/processes/tests"),
            Path("./openeo-test-suite/assets/processes/tests"),
        ]
        for candidate in candidates:
            if candidate.exists() and candidate.is_dir():
                return candidate
        raise ValueError(
            f"Could not find valid processes test root directory (tried {candidates})"
        )

    def get_all_processes(self) -> Iterator[ProcessData]:
        """Collect all processes"""
        # TODO: cache or preload this in __init__?
        if not self._root.is_dir():
            raise ValueError(f"Invalid process test root directory: {self._root}")
        _log.info(f"Loading process definitions from {self._root}")
        for path in self._root.glob("*.json5"):
            try:
                with path.open() as f:
                    data = json5.load(f)
                assert data["id"] == path.stem
                yield ProcessData(
                    process_id=data["id"],
                    level=data.get("level"),
                    tests=data.get("tests", []),
                    experimental=data.get("experimental", False),
                    path=path,
                )
            except Exception as e:
                # TODO: good idea to skip broken definitions? Why not just fail hard?
                _log.error(f"Failed to load process data from {path}: {e!r}")
