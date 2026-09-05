"""Test-only Windows post-admission hard-link creation probe."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from test_windows_cache_cleanup_capability_probe import (
    _WindowsCapabilityProbe,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_cooperative_lock_probe import (
    _close_participant,  # pyright: ignore[reportPrivateUsage]
    _CoordinationLockProbe,  # pyright: ignore[reportPrivateUsage]
    _create_fixture,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_expected_identity_guardian_admission_probe import (
    _read_identity_guardian_event,  # pyright: ignore[reportPrivateUsage]
    _release_identity_guardian,  # pyright: ignore[reportPrivateUsage]
    _start_identity_guardian,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_protected_guardian_handoff_probe import (
    _assert_exclusive_available,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M183 probes Windows post-admission hard-link creation",
)

_ERROR_SHARING_VIOLATION = 32


def test_matching_guardian_does_not_exclude_post_admission_hard_link_creation(
    tmp_path: Path,
) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    peer_path = tmp_path / "peer"
    peer_path.mkdir()
    alias_path = peer_path / "coordination.alias"
    displaced_path = coordination_path.with_name("coordination.displaced")

    guardian: subprocess.Popen[bytes] | None = None
    identity_probe = _WindowsCapabilityProbe()
    lock_probe = _CoordinationLockProbe()
    try:
        with identity_probe, lock_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            peer = identity_probe.open_directory(root, "peer")
            original = identity_probe.open_file(live, "coordination.lock", delete_access=False)
            original_identity = identity_probe.identity(original)
            assert identity_probe.link_count(original) == 1

            guardian = _start_identity_guardian(tmp_path, original_identity)
            assert _read_identity_guardian_event(guardian) == "ready"
            assert guardian.poll() is None

            with pytest.raises(OSError) as blocked_coordination:
                coordination_path.rename(displaced_path)
            assert blocked_coordination.value.winerror == _ERROR_SHARING_VIOLATION

            os.link(coordination_path, alias_path)
            assert guardian.poll() is None
            alias = identity_probe.open_file(peer, "coordination.alias", delete_access=False)
            assert identity_probe.identity(alias) == original_identity
            assert identity_probe.link_count(original) == 2
            assert identity_probe.link_count(alias) == 2
            assert coordination_path.read_bytes() == payload
            assert alias_path.read_bytes() == payload
            _assert_exclusive_available(lock_probe, coordination_path)
            _assert_exclusive_available(lock_probe, alias_path)

            with pytest.raises(OSError) as still_blocked_coordination:
                coordination_path.rename(displaced_path)
            assert still_blocked_coordination.value.winerror == _ERROR_SHARING_VIOLATION

            assert _release_identity_guardian(guardian) == "closed"
            assert guardian.returncode == 0
            coordination_path.rename(displaced_path)
            displaced = identity_probe.open_file(
                live,
                "coordination.displaced",
                delete_access=False,
            )
            assert identity_probe.identity(displaced) == original_identity
            assert identity_probe.identity(alias) == original_identity
            assert identity_probe.link_count(displaced) == 2
            assert identity_probe.link_count(alias) == 2
            assert displaced_path.read_bytes() == payload
            assert alias_path.read_bytes() == payload
    finally:
        if guardian is not None:
            _close_participant(guardian)

    assert guardian is not None and guardian.returncode == 0
    for stream in (guardian.stdin, guardian.stdout, guardian.stderr):
        assert stream is not None and stream.closed
    assert identity_probe.owned_count == 0
    assert lock_probe.owned_count == 0
    assert displaced_path.read_bytes() == payload
    assert alias_path.read_bytes() == payload
    assert not coordination_path.exists()
