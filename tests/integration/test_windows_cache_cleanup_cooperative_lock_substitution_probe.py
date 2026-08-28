"""Test-only Windows coordination-lock pathname-substitution probe for M174."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _NativeFailure,  # pyright: ignore[reportPrivateUsage]
    _WindowsCapabilityProbe,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_probe import (
    _ERROR_LOCK_VIOLATION,  # pyright: ignore[reportPrivateUsage]
    _close_participant,  # pyright: ignore[reportPrivateUsage]
    _CoordinationLockProbe,  # pyright: ignore[reportPrivateUsage]
    _create_fixture,  # pyright: ignore[reportPrivateUsage]
    _read_event,  # pyright: ignore[reportPrivateUsage]
    _release_and_read_closed,  # pyright: ignore[reportPrivateUsage]
    _start_participant,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M174 probes Windows coordination-lock pathname substitution",
)

_CHILD = Path(__file__).parents[1] / "fixtures/windows_coordination_lock_substitution_child.py"
_SCHEMA = "ludoweave.test.windows-coordination-lock-substitution/1"
_MAX_CHILD_OUTPUT_BYTES = 256
_TIMEOUT_SECONDS = 15.0


@dataclass(frozen=True, slots=True)
class _SubstitutionResult:
    phase: str
    error_code: int


def _attempt_substitution(working_directory: Path) -> _SubstitutionResult:
    completed = subprocess.run(
        (sys.executable, "-I", "-B", str(_CHILD)),
        check=False,
        capture_output=True,
        close_fds=True,
        cwd=working_directory,
        shell=False,
        stdin=subprocess.DEVNULL,
        timeout=_TIMEOUT_SECONDS,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"substitution child exited with code {completed.returncode}") from None
    if completed.stderr or len(completed.stdout) > _MAX_CHILD_OUTPUT_BYTES:
        raise RuntimeError("substitution child returned invalid structured output") from None
    try:
        payload: object = json.loads(completed.stdout)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("substitution child returned invalid structured output") from None
    if not isinstance(payload, dict):
        raise RuntimeError("substitution child returned invalid structured output") from None
    document = cast(dict[object, object], payload)
    if set(document) != {"error_code", "phase", "schema"}:
        raise RuntimeError("substitution child returned invalid structured output") from None
    phase = document["phase"]
    error_code = document["error_code"]
    if (
        document["schema"] != _SCHEMA
        or type(phase) is not str
        or phase
        not in {
            "substituted",
            "rename_failed",
            "create_failed",
            "inheritable_handle",
            "write_failed",
            "short_write",
            "close_failed",
        }
        or type(error_code) is not int
        or error_code < 0
    ):
        raise RuntimeError("substitution child returned invalid structured output") from None
    return _SubstitutionResult(phase=phase, error_code=error_code)


def test_path_substitution_splits_cooperative_lock_generations(tmp_path: Path) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    displaced_path = coordination_path.with_name("coordination.displaced")
    original_participant = _start_participant(tmp_path)
    replacement_participant: subprocess.Popen[bytes] | None = None

    try:
        identity_probe = _WindowsCapabilityProbe()
        lock_probe = _CoordinationLockProbe()
        with identity_probe, lock_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            original = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            original_identity = identity_probe.identity(original)

            assert _read_event(original_participant) == ("ready", 0)
            assert original_participant.poll() is None
            assert _attempt_substitution(tmp_path) == _SubstitutionResult(
                phase="substituted",
                error_code=0,
            )

            displaced = identity_probe.open_file(
                live,
                "coordination.displaced",
                delete_access=False,
            )
            replacement = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            displaced_identity = identity_probe.identity(displaced)
            replacement_identity = identity_probe.identity(replacement)
            assert original_identity == displaced_identity
            assert replacement_identity != original_identity
            assert displaced_path.read_bytes() == payload
            assert coordination_path.read_bytes() == payload

            replacement_participant = _start_participant(tmp_path)
            assert _read_event(replacement_participant) == ("ready", 0)
            assert replacement_participant.poll() is None
            assert original_participant.poll() is None

            with pytest.raises(_NativeFailure) as old_generation_active:
                lock_probe.acquire_exclusive(displaced_path)
            assert old_generation_active.value.code == _ERROR_LOCK_VIOLATION
            with pytest.raises(_NativeFailure) as new_generation_active:
                lock_probe.acquire_exclusive(coordination_path)
            assert new_generation_active.value.code == _ERROR_LOCK_VIOLATION
            assert lock_probe.owned_count == 0

            assert _release_and_read_closed(replacement_participant) == ("closed", 0)
            assert replacement_participant.returncode == 0
            assert original_participant.poll() is None
            replacement_exclusive = lock_probe.acquire_exclusive(coordination_path)
            assert os.get_handle_inheritable(replacement_exclusive) is False
            lock_probe.release_exclusive(replacement_exclusive)
            with pytest.raises(_NativeFailure) as old_still_active:
                lock_probe.acquire_exclusive(displaced_path)
            assert old_still_active.value.code == _ERROR_LOCK_VIOLATION

            assert _release_and_read_closed(original_participant) == ("closed", 0)
            assert original_participant.returncode == 0
            displaced_exclusive = lock_probe.acquire_exclusive(displaced_path)
            assert os.get_handle_inheritable(displaced_exclusive) is False
            lock_probe.release_exclusive(displaced_exclusive)
            assert lock_probe.owned_count == 0
    finally:
        _close_participant(original_participant)
        if replacement_participant is not None:
            _close_participant(replacement_participant)

    assert displaced_path.read_bytes() == payload
    assert coordination_path.read_bytes() == payload
