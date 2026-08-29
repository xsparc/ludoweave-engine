"""Test-only Windows overlapping coordination-guardian rotation probe."""

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
from test_windows_cache_cleanup_cooperative_lock_live_substitution_exclusion_probe import (
    _start_protected_participant,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_probe import (
    _close_participant,  # pyright: ignore[reportPrivateUsage]
    _CoordinationLockProbe,  # pyright: ignore[reportPrivateUsage]
    _create_fixture,  # pyright: ignore[reportPrivateUsage]
    _read_event,  # pyright: ignore[reportPrivateUsage]
    _release_and_read_closed,  # pyright: ignore[reportPrivateUsage]
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
    _assert_exclusive_refused,  # pyright: ignore[reportPrivateUsage]
    _assert_substitution_refused,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M179 probes overlapping Windows coordination-guardian rotation",
)


def test_overlapping_guardian_rotation_preserves_each_surviving_owner(
    tmp_path: Path,
) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    displaced_path = coordination_path.with_name("coordination.displaced")
    first_guardian: subprocess.Popen[bytes] | None = None
    second_guardian: subprocess.Popen[bytes] | None = None
    participant: subprocess.Popen[bytes] | None = None

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
            after_first = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            assert identity_probe.identity(after_first) == original_identity
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_available(lock_probe, coordination_path)

            participant = _start_protected_participant(tmp_path)
            assert _read_event(participant) == ("ready", 0)
            assert participant.poll() is None
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_refused(lock_probe, coordination_path)

            second_guardian = _start_guardian(tmp_path)
            assert _read_guardian_event(second_guardian) == "ready"
            assert first_guardian.poll() is None
            assert second_guardian.poll() is None
            assert participant.poll() is None
            after_second = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            assert identity_probe.identity(after_second) == original_identity
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_refused(lock_probe, coordination_path)

            first_return_code = _terminate_and_assert_abrupt(first_guardian)
            assert first_guardian.poll() == first_return_code
            assert second_guardian.poll() is None
            assert participant.poll() is None
            after_first_loss = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            assert identity_probe.identity(after_first_loss) == original_identity
            _assert_substitution_refused(tmp_path)
            _assert_exclusive_refused(lock_probe, coordination_path)

            assert _release_and_read_closed(participant) == ("closed", 0)
            assert participant.returncode == 0
            assert second_guardian.poll() is None
            guardian_only = identity_probe.open_file(
                live,
                "coordination.lock",
                delete_access=False,
            )
            assert identity_probe.identity(guardian_only) == original_identity
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
        for process in (first_guardian, second_guardian, participant):
            if process is not None:
                _close_participant(process)

    assert first_guardian is not None and first_guardian.returncode is not None
    assert first_guardian.returncode != 0
    assert second_guardian is not None and second_guardian.returncode == 0
    assert participant is not None and participant.returncode == 0
    for process in (first_guardian, second_guardian, participant):
        for stream in (process.stdin, process.stdout, process.stderr):
            assert stream is not None and stream.closed
    assert lock_probe.owned_count == 0
    assert displaced_path.read_bytes() == payload
    assert coordination_path.read_bytes() == payload
