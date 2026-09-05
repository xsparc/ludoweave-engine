"""Test-only Windows zero-owner guardian restart-boundary probe."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _WindowsCapabilityProbe,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_abrupt_settlement_probe import (
    _terminate_and_assert_abrupt,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_probe import (
    _close_participant,  # pyright: ignore[reportPrivateUsage]
    _CoordinationLockProbe,  # pyright: ignore[reportPrivateUsage]
    _create_fixture,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_substitution_probe import (
    _attempt_substitution,  # pyright: ignore[reportPrivateUsage]
    _SubstitutionResult,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_guardian_abrupt_handoff_probe import (
    _read_guardian_event,  # pyright: ignore[reportPrivateUsage]
    _release_guardian,  # pyright: ignore[reportPrivateUsage]
    _start_guardian,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_protected_guardian_handoff_probe import (
    _assert_exclusive_available,  # pyright: ignore[reportPrivateUsage]
    _assert_substitution_refused,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M180 probes the Windows zero-owner guardian restart boundary",
)


def test_benign_zero_owner_guardian_restart_reacquires_unchanged_identity(
    tmp_path: Path,
) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    displaced_path = coordination_path.with_name("coordination.displaced")
    first_guardian: subprocess.Popen[bytes] | None = None
    second_guardian: subprocess.Popen[bytes] | None = None

    identity_probe = _WindowsCapabilityProbe()
    lock_probe = _CoordinationLockProbe()
    try:
        with identity_probe, lock_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            original = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            original_identity = identity_probe.identity(original)

            first_guardian = _start_guardian(tmp_path)
            assert _read_guardian_event(first_guardian) == "ready"
            assert first_guardian.poll() is None
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_available(lock_probe, coordination_path)

            first_return_code = _terminate_and_assert_abrupt(first_guardian)
            assert first_guardian.poll() == first_return_code
            exposed = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            assert identity_probe.identity(exposed) == original_identity
            _assert_exclusive_available(lock_probe, coordination_path)

            second_guardian = _start_guardian(tmp_path)
            assert _read_guardian_event(second_guardian) == "ready"
            assert second_guardian.poll() is None
            restarted = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            assert identity_probe.identity(restarted) == original_identity
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_available(lock_probe, coordination_path)

            assert _release_guardian(second_guardian) == "closed"
            assert second_guardian.returncode == 0
            _assert_exclusive_available(lock_probe, coordination_path)
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
            assert identity_probe.identity(displaced) == original_identity
            assert identity_probe.identity(replacement) != original_identity
            assert displaced_path.read_bytes() == payload
            assert coordination_path.read_bytes() == payload
    finally:
        for process in (first_guardian, second_guardian):
            if process is not None:
                _close_participant(process)

    assert first_guardian is not None and first_guardian.returncode is not None
    assert first_guardian.returncode != 0
    assert second_guardian is not None and second_guardian.returncode == 0
    for process in (first_guardian, second_guardian):
        for stream in (process.stdin, process.stdout, process.stderr):
            assert stream is not None and stream.closed
    assert lock_probe.owned_count == 0
    assert displaced_path.read_bytes() == payload
    assert coordination_path.read_bytes() == payload


def test_zero_owner_substitution_redirects_later_guardian_to_replacement_identity(
    tmp_path: Path,
) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    displaced_path = coordination_path.with_name("coordination.displaced")
    second_displaced_path = coordination_path.with_name("coordination.second-displaced")
    first_guardian: subprocess.Popen[bytes] | None = None
    second_guardian: subprocess.Popen[bytes] | None = None

    identity_probe = _WindowsCapabilityProbe()
    lock_probe = _CoordinationLockProbe()
    try:
        with identity_probe, lock_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            original = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            original_identity = identity_probe.identity(original)

            first_guardian = _start_guardian(tmp_path)
            assert _read_guardian_event(first_guardian) == "ready"
            assert first_guardian.poll() is None
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_available(lock_probe, coordination_path)

            first_return_code = _terminate_and_assert_abrupt(first_guardian)
            assert first_guardian.poll() == first_return_code
            _assert_exclusive_available(lock_probe, coordination_path)

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
            replacement_identity = identity_probe.identity(replacement)
            assert identity_probe.identity(displaced) == original_identity
            assert replacement_identity != original_identity
            assert displaced_path.read_bytes() == payload
            assert coordination_path.read_bytes() == payload

            second_guardian = _start_guardian(tmp_path)
            assert _read_guardian_event(second_guardian) == "ready"
            assert second_guardian.poll() is None
            restarted = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            assert identity_probe.identity(restarted) == replacement_identity
            assert identity_probe.identity(restarted) != original_identity
            with pytest.raises(OSError) as blocked:
                coordination_path.rename(second_displaced_path)
            assert blocked.value.winerror == 32
            _assert_exclusive_available(lock_probe, coordination_path)

            assert _release_guardian(second_guardian) == "closed"
            assert second_guardian.returncode == 0
            coordination_path.rename(second_displaced_path)
            moved_replacement = identity_probe.open_file(
                live,
                "coordination.second-displaced",
                delete_access=False,
            )
            assert identity_probe.identity(moved_replacement) == replacement_identity
            assert identity_probe.identity(displaced) == original_identity
            assert displaced_path.read_bytes() == payload
            assert second_displaced_path.read_bytes() == payload
    finally:
        for process in (first_guardian, second_guardian):
            if process is not None:
                _close_participant(process)

    assert first_guardian is not None and first_guardian.returncode is not None
    assert first_guardian.returncode != 0
    assert second_guardian is not None and second_guardian.returncode == 0
    for process in (first_guardian, second_guardian):
        for stream in (process.stdin, process.stdout, process.stderr):
            assert stream is not None and stream.closed
    assert lock_probe.owned_count == 0
    assert not coordination_path.exists()
    assert displaced_path.read_bytes() == payload
    assert second_displaced_path.read_bytes() == payload
