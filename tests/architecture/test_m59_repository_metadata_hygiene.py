"""Protect the repository's tool-neutral tracked metadata convention."""

from __future__ import annotations

import subprocess
from pathlib import Path

from pytest import MonkeyPatch

_ROOT = Path(__file__).resolve().parents[2]
_RETIRED_MARKER_HEX = (
    "636f646578",
    "2e6169",
    "2e6167656e7473",
    "2e636f646578",
    "6167656e74732e6d64",
    "617373697374616e74",
    "6f70656e6169",
    "63686174677074",
    "6169206167656e74",
    "6172746966696369616c20696e74656c6c6967656e6365",
    "6c61726765206c616e6775616765206d6f64656c",
    "67656e65726174697665206169",
)
_RETIRED_EXACT_MARKER_HEX = ("4147454e5453",)
_RETIRED_ROOT_PATH_HEX = (
    "2e6169",
    "2e6167656e7473",
    "2e636f646578",
    "4147454e54532e6d64",
)


def _decode(value: str) -> str:
    return bytes.fromhex(value).decode("ascii")


def _contains_retired_marker(value: str) -> bool:
    folded = value.casefold()
    return any(_decode(marker).casefold() in folded for marker in _RETIRED_MARKER_HEX) or any(
        _decode(marker) in value for marker in _RETIRED_EXACT_MARKER_HEX
    )


def _repository_text_paths() -> tuple[Path, ...]:
    completed = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
        ],
        cwd=_ROOT,
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    return tuple(_ROOT / relative for relative in completed.stdout.split("\0") if relative)


def _retired_root_path_violations(root: Path = _ROOT) -> tuple[Path, ...]:
    violations: list[Path] = []
    for encoded in _RETIRED_ROOT_PATH_HEX:
        path = root / _decode(encoded)
        if path.exists() or path.is_symlink():
            violations.append(path)
    return tuple(violations)


def test_repository_text_is_free_of_retired_tooling_identity_markers() -> None:
    violations: list[str] = []

    for path in _repository_text_paths():
        relative = path.relative_to(_ROOT).as_posix()
        if _contains_retired_marker(relative):
            violations.append(relative)
            continue
        if path.is_symlink():
            if _contains_retired_marker(path.readlink().as_posix()):
                violations.append(relative)
            continue
        payload = path.read_bytes()
        if b"\0" in payload:
            continue
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if _contains_retired_marker(text):
            violations.append(relative)

    assert violations == []


def test_hygiene_matcher_preserves_product_agent_terminology() -> None:
    for encoded in (*_RETIRED_MARKER_HEX, *_RETIRED_EXACT_MARKER_HEX):
        assert _contains_retired_marker(_decode(encoded))
    assert not _contains_retired_marker("software agents operate the same world")
    assert not _contains_retired_marker("src/ludoweave/agent/service.py")


def test_retired_root_control_paths_remain_absent() -> None:
    assert _retired_root_path_violations() == ()


def test_dangling_retired_root_symlink_is_not_considered_absent(
    monkeypatch: MonkeyPatch,
) -> None:
    dangling = _ROOT / _decode(_RETIRED_ROOT_PATH_HEX[0])

    def missing(_path: Path) -> bool:
        return False

    def is_dangling(path: Path) -> bool:
        return path == dangling

    monkeypatch.setattr(Path, "exists", missing)
    monkeypatch.setattr(Path, "is_symlink", is_dangling)

    assert _retired_root_path_violations() == (dangling,)


def test_repository_metadata_hygiene_contract_is_documented() -> None:
    required = {
        _ROOT / "README.md": ("tool-neutral repository metadata",),
        _ROOT / "MAINTAINERS.md": (
            "M59 current-tree metadata hygiene",
            "does not rewrite Git history",
        ),
        _ROOT / "CHANGELOG.md": ("M59/RFC-0042",),
        _ROOT / "ROADMAP.md": ("M59 repository metadata hygiene",),
        _ROOT / "docs" / "rfcs" / "0042-tool-neutral-repository-metadata.md": (
            "current tracked tree",
            "Product-facing agent terminology",
        ),
        _ROOT / "docs" / "rfcs" / "index.md": ("RFC-0042: tool-neutral repository metadata",),
        _ROOT / "mkdocs.yml": ("0042-tool-neutral-repository-metadata.md",),
    }

    for path, values in required.items():
        assert path.is_file()
        text = path.read_text(encoding="utf-8")
        assert all(value in text for value in values)
