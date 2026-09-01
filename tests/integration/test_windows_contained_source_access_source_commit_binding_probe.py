"""Test-only binding of the M220 retained source to its committed Git blob."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.integration import (
    test_windows_contained_source_access_source_binding_probe as _source_module,
)
from tests.integration.test_windows_contained_source_access_source_binding_probe import (
    _ERROR_ACCESS_DENIED,  # pyright: ignore[reportPrivateUsage]
    _SOURCE_BOUND_CONTENDER,  # pyright: ignore[reportPrivateUsage]
    _ContainedSourceBoundAccessProbe,  # pyright: ignore[reportPrivateUsage]
    _InheritedLaunchSource,  # pyright: ignore[reportPrivateUsage]
    _InheritedNullHandle,  # pyright: ignore[reportPrivateUsage]
    _NativeFailure,  # pyright: ignore[reportPrivateUsage]
    _require_source_access_allowed,  # pyright: ignore[reportPrivateUsage]
    _verify_source_stable,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _ImageSnapshot,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M221 binds the Windows retained contender source to the M220 Git blob",
)

_ROOT = Path(__file__).parents[2]
_M220_COMMIT = "734d4eb943c3da7a1a8357ef3e180cac4353cb6b"
_M220_TREE = "5575eeeb8123a0eaed9028a6281227b64fdfb73d"
_M220_PARENT = "09e6d3390040498371912d7d47bff5b75be03c35"
_M220_SOURCE_PATH = "tests/fixtures/windows_contained_source_access_bound_contender.py"
_M220_SOURCE_BLOB = "10b71fc7d2d555160bf4a2869190a0b3e66d3330"
_M220_SOURCE_BYTES = 3252
_M220_SOURCE_SHA256 = bytes.fromhex(
    "fa01dae3119f817c62d0b27b0f575642c9837ad5259d79507bd2a1c09c41d2dd"
)
_MAX_GIT_METADATA_BYTES = 256
_MAX_GIT_BLOB_BYTES = 4096
_GIT_TIMEOUT_SECONDS = 10.0
_CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


@dataclass(frozen=True, slots=True)
class _CommittedSourceSnapshot:
    commit: str
    tree: str
    parent: str
    path: str
    blob_oid: str
    size: int
    sha256: bytes


def _git_executable() -> Path:
    candidate = shutil.which("git")
    if candidate is None:
        raise RuntimeError("Git executable was unavailable") from None
    executable = Path(candidate).resolve(strict=True)
    if not executable.is_file() or not executable.is_absolute():
        raise RuntimeError("Git executable did not resolve to a file") from None
    return executable


def _git_environment() -> dict[str, str]:
    environment = {
        name: value for name, value in os.environ.items() if not name.upper().startswith("GIT_")
    }
    environment.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return environment


def _run_git(
    *arguments: str,
    max_output_bytes: int = _MAX_GIT_METADATA_BYTES,
) -> bytes:
    if max_output_bytes <= 0 or max_output_bytes > _MAX_GIT_BLOB_BYTES:
        raise RuntimeError("Git output bound was invalid") from None
    try:
        completed = subprocess.run(  # noqa: UP022 - explicit pipes are a protected boundary
            (
                str(_git_executable()),
                "--no-pager",
                "--no-replace-objects",
                "-C",
                str(_ROOT),
                *arguments,
            ),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            check=False,
            timeout=_GIT_TIMEOUT_SECONDS,
            creationflags=_CREATE_NO_WINDOW,
            env=_git_environment(),
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise RuntimeError("fixed Git object read failed") from error
    if completed.returncode != 0:
        raise RuntimeError("fixed Git object read returned nonzero") from None
    if completed.stderr != b"":
        raise RuntimeError("fixed Git object read produced stderr") from None
    if len(completed.stdout) > max_output_bytes:
        raise RuntimeError("fixed Git object read exceeded its output bound") from None
    return completed.stdout


def _git_line(*arguments: str) -> str:
    raw = _run_git(*arguments)
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise RuntimeError("Git metadata was not ASCII") from error
    lines = text.splitlines()
    if len(lines) != 1 or lines[0] == "" or lines[0].strip() != lines[0]:
        raise RuntimeError("Git metadata was not one canonical line") from None
    return lines[0]


def _load_committed_source() -> _CommittedSourceSnapshot:
    if _git_line("cat-file", "-t", _M220_COMMIT) != "commit":
        raise RuntimeError("M220 object was not a commit") from None
    commit = _git_line("rev-parse", "--verify", f"{_M220_COMMIT}^{{commit}}")
    if commit != _M220_COMMIT:
        raise RuntimeError("M220 commit identity did not match") from None
    tree = _git_line("rev-parse", "--verify", f"{_M220_COMMIT}^{{tree}}")
    if tree != _M220_TREE:
        raise RuntimeError("M220 tree identity did not match") from None
    parent = _git_line("rev-parse", "--verify", f"{_M220_COMMIT}^")
    if parent != _M220_PARENT:
        raise RuntimeError("M220 parent identity did not match") from None
    blob_oid = _git_line("rev-parse", "--verify", f"{_M220_COMMIT}:{_M220_SOURCE_PATH}")
    if blob_oid != _M220_SOURCE_BLOB:
        raise RuntimeError("M220 source path did not resolve to the expected blob") from None
    if _git_line("cat-file", "-t", _M220_SOURCE_BLOB) != "blob":
        raise RuntimeError("M220 source object was not a blob") from None
    size_text = _git_line("cat-file", "-s", _M220_SOURCE_BLOB)
    if not size_text.isascii() or not size_text.isdecimal():
        raise RuntimeError("M220 source blob size was invalid") from None
    size = int(size_text)
    if size != _M220_SOURCE_BYTES:
        raise RuntimeError("M220 source blob size did not match") from None
    blob = _run_git("cat-file", "blob", _M220_SOURCE_BLOB, max_output_bytes=_MAX_GIT_BLOB_BYTES)
    digest = hashlib.sha256(blob).digest()
    if len(blob) != _M220_SOURCE_BYTES or digest != _M220_SOURCE_SHA256:
        raise RuntimeError("M220 source blob content did not match") from None
    return _CommittedSourceSnapshot(
        commit=commit,
        tree=tree,
        parent=parent,
        path=_M220_SOURCE_PATH,
        blob_oid=blob_oid,
        size=size,
        sha256=digest,
    )


def _verify_committed_source(
    retained: _ImageSnapshot,
    committed: _CommittedSourceSnapshot,
) -> None:
    if retained.size != committed.size:
        raise RuntimeError("retained source size did not match committed blob") from None
    if retained.sha256 != committed.sha256:
        raise RuntimeError("retained source digest did not match committed blob") from None


def _require_committed_source_bound_access_refused(*, phase: str) -> None:
    with (
        _InheritedLaunchSource(_SOURCE_BOUND_CONTENDER) as source_file,
        _InheritedNullHandle() as output_handle,
        _InheritedNullHandle() as error_handle,
    ):
        committed_before = _load_committed_source()
        source_before = source_file.snapshot()
        _verify_committed_source(source_before, committed_before)
        source_file.rewind()
        probe = _ContainedSourceBoundAccessProbe()
        try:
            with probe:
                probe.run_source_bound_contender(
                    source_file,
                    output_handle,
                    error_handle,
                    phase=phase,
                )
        except _NativeFailure as error:
            if error.operation == "AssignProcessToJobObject" and error.code == _ERROR_ACCESS_DENIED:
                pytest.skip("current host does not permit the required nested Job Object")
            raise
        committed_after = _load_committed_source()
        assert committed_after == committed_before
        source_after = source_file.snapshot()
        _verify_committed_source(source_after, committed_after)
        _verify_source_stable(source_before, source_after)
        assert probe.owned_count == 0
    _require_source_access_allowed(_SOURCE_BOUND_CONTENDER)


def test_committed_source_binding_preserves_m220_boundary() -> None:
    with patch.object(
        _source_module,
        "_require_source_bound_source_access_refused",
        _require_committed_source_bound_access_refused,
    ):
        _source_module.test_contained_source_access_source_binding_preserves_boundary()


def test_committed_source_descriptor_is_exact() -> None:
    assert _load_committed_source() == _CommittedSourceSnapshot(
        commit=_M220_COMMIT,
        tree=_M220_TREE,
        parent=_M220_PARENT,
        path=_M220_SOURCE_PATH,
        blob_oid=_M220_SOURCE_BLOB,
        size=_M220_SOURCE_BYTES,
        sha256=_M220_SOURCE_SHA256,
    )


def test_committed_source_verifier_rejects_size_drift() -> None:
    with _InheritedLaunchSource(_SOURCE_BOUND_CONTENDER) as source_file:
        retained = source_file.snapshot()
    committed = _load_committed_source()
    drifted = _CommittedSourceSnapshot(
        commit=committed.commit,
        tree=committed.tree,
        parent=committed.parent,
        path=committed.path,
        blob_oid=committed.blob_oid,
        size=committed.size + 1,
        sha256=committed.sha256,
    )
    with pytest.raises(RuntimeError, match="retained source size"):
        _verify_committed_source(retained, drifted)


def test_committed_source_verifier_rejects_digest_drift() -> None:
    with _InheritedLaunchSource(_SOURCE_BOUND_CONTENDER) as source_file:
        retained = source_file.snapshot()
    committed = _load_committed_source()
    drifted = _CommittedSourceSnapshot(
        commit=committed.commit,
        tree=committed.tree,
        parent=committed.parent,
        path=committed.path,
        blob_oid=committed.blob_oid,
        size=committed.size,
        sha256=b"\x00" * len(committed.sha256),
    )
    with pytest.raises(RuntimeError, match="retained source digest"):
        _verify_committed_source(retained, drifted)
