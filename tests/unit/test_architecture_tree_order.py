"""Frozen tree checks must not depend on the host's pathlib ordering flavour."""

from __future__ import annotations

import hashlib
import re
import runpy
from collections.abc import Callable
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
from typing import cast

import pytest

_FILES = ("README.md", "folder.py", "folder/Z.py", "a.txt", "A.txt")
_ORDER = ("A.txt", "a.txt", "folder/Z.py", "folder.py", "README.md")
_ARCHITECTURE = Path(__file__).parents[1] / "architecture"


class _Candidate:
    def __init__(self, name: str, flavour: type[PurePath]) -> None:
        self.path = flavour(name)
        self.parts = self.path.parts
        self.suffix = self.path.suffix

    def __lt__(self, other: _Candidate) -> bool:
        return self.path < other.path

    def is_file(self) -> bool:
        return True

    def read_bytes(self) -> bytes:
        return self.path.as_posix().encode("ascii")

    def relative_to(self, _root: object) -> PurePath:
        return self.path


class _Root:
    def __init__(self, flavour: type[PurePath], reverse: bool) -> None:
        names = (*_FILES, "__pycache__/ignored.pyc")
        self.candidates = [_Candidate(name, flavour) for name in names]
        if reverse:
            self.candidates.reverse()

    def rglob(self, pattern: str) -> list[_Candidate]:
        assert pattern == "*"
        return self.candidates


@pytest.mark.parametrize("flavour", [PurePosixPath, PureWindowsPath])
@pytest.mark.parametrize("reverse", [False, True])
def test_all_affected_tree_guards_use_one_explicit_order(
    flavour: type[PurePath], reverse: bool
) -> None:
    expected = hashlib.sha256()
    for name in _ORDER:
        expected.update(name.encode("ascii") + b"\0" + name.encode("ascii") + b"\0")
    count = 0
    for source in _ARCHITECTURE.glob("test_m*.py"):
        match = re.match(r"test_m(\d+)_", source.name)
        if match is None or not 153 <= int(match[1]) <= 235:
            continue
        namespace = runpy.run_path(str(source))
        tree_hash = cast(Callable[[object], str], namespace["_tree_sha256"])
        assert tree_hash(_Root(flavour, reverse)) == expected.hexdigest(), source.name
        count += 1
    assert count == 83
