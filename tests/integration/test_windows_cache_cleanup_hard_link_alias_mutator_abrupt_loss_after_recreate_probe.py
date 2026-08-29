"""Test-only Windows hard-link alias mutator post-recreate abrupt-loss probe."""

from __future__ import annotations

import os
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
from test_windows_cache_cleanup_expected_identity_guardian_admission_probe import (
    _read_identity_guardian_event,  # pyright: ignore[reportPrivateUsage]
    _release_identity_guardian,  # pyright: ignore[reportPrivateUsage]
    _start_identity_guardian,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_independent_hard_link_alias_mutator_aba_probe import (
    _RECREATE_TOKEN,  # pyright: ignore[reportPrivateUsage]
    _read_alias_mutator_event,  # pyright: ignore[reportPrivateUsage]
    _send_alias_mutator_token,  # pyright: ignore[reportPrivateUsage]
    _start_alias_mutator,  # pyright: ignore[reportPrivateUsage]
)
from test_windows_cache_cleanup_protected_guardian_handoff_probe import (
    _assert_exclusive_available,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M188 probes abrupt mutator loss after Windows hard-link alias recreation",
)

_ERROR_SHARING_VIOLATION = 32


def test_abrupt_mutator_loss_after_recreate_leaves_alias_present(
    tmp_path: Path,
) -> None:
    coordination_path, payload = _create_fixture(tmp_path)
    peer_path = tmp_path / "peer"
    peer_path.mkdir()
    alias_path = peer_path / "coordination.alias"
    displaced_path = coordination_path.with_name("coordination.displaced")
    os.link(coordination_path, alias_path)

    guardian: subprocess.Popen[bytes] | None = None
    mutator: subprocess.Popen[bytes] | None = None
    mutator_return_code: int | None = None
    identity_probe = _WindowsCapabilityProbe()
    lock_probe = _CoordinationLockProbe()
    try:
        with identity_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            peer = identity_probe.open_directory(root, "peer")
            original = identity_probe.open_file(live, "coordination.lock", delete_access=False)
            alias = identity_probe.open_file(peer, "coordination.alias", delete_access=False)
            original_identity = identity_probe.identity(original)
            assert identity_probe.identity(alias) == original_identity
            assert identity_probe.link_count(original) == 2
            assert identity_probe.link_count(alias) == 2

        assert identity_probe.owned_count == 0
        guardian = _start_identity_guardian(tmp_path, original_identity)
        assert _read_identity_guardian_event(guardian) == "ready"
        assert guardian.poll() is None

        with identity_probe, lock_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            peer = identity_probe.open_directory(root, "peer")
            original = identity_probe.open_file(live, "coordination.lock", delete_access=False)
            assert identity_probe.identity(original) == original_identity
            assert identity_probe.link_count(original) == 2

            with pytest.raises(OSError) as blocked_before_delete:
                coordination_path.rename(displaced_path)
            assert blocked_before_delete.value.winerror == _ERROR_SHARING_VIOLATION

            mutator = _start_alias_mutator(tmp_path)
            assert mutator.pid != guardian.pid
            assert mutator.pid != os.getpid()
            assert _read_alias_mutator_event(mutator) == "deleted"
            assert mutator.poll() is None
            assert guardian.poll() is None
            assert not alias_path.exists()
            assert identity_probe.identity(original) == original_identity
            assert identity_probe.link_count(original) == 1

            assert _send_alias_mutator_token(mutator, _RECREATE_TOKEN) == "recreated"
            assert mutator.poll() is None
            assert guardian.poll() is None
            alias = identity_probe.open_file(peer, "coordination.alias", delete_access=False)
            assert identity_probe.identity(original) == original_identity
            assert identity_probe.identity(alias) == original_identity
            assert identity_probe.link_count(original) == 2
            assert identity_probe.link_count(alias) == 2
            assert coordination_path.read_bytes() == payload
            assert alias_path.read_bytes() == payload
            _assert_exclusive_available(lock_probe, coordination_path)
            _assert_exclusive_available(lock_probe, alias_path)

            mutator_return_code = _terminate_and_assert_abrupt(mutator)
            assert mutator.poll() == mutator_return_code
            assert guardian.poll() is None
            assert alias_path.exists()
            assert identity_probe.identity(original) == original_identity
            assert identity_probe.identity(alias) == original_identity
            assert identity_probe.link_count(original) == 2
            assert identity_probe.link_count(alias) == 2
            assert coordination_path.read_bytes() == payload
            assert alias_path.read_bytes() == payload
            _assert_exclusive_available(lock_probe, coordination_path)
            _assert_exclusive_available(lock_probe, alias_path)

            with pytest.raises(OSError) as blocked_after_mutator_loss:
                coordination_path.rename(displaced_path)
            assert blocked_after_mutator_loss.value.winerror == _ERROR_SHARING_VIOLATION

            assert _release_identity_guardian(guardian) == "closed"
            assert guardian.returncode == 0

        coordination_path.rename(displaced_path)
        with identity_probe:
            root = identity_probe.open_root(tmp_path)
            live = identity_probe.open_directory(root, "live")
            peer = identity_probe.open_directory(root, "peer")
            displaced = identity_probe.open_file(
                live,
                "coordination.displaced",
                delete_access=False,
            )
            alias = identity_probe.open_file(peer, "coordination.alias", delete_access=False)
            assert identity_probe.identity(displaced) == original_identity
            assert identity_probe.identity(alias) == original_identity
            assert identity_probe.link_count(displaced) == 2
            assert identity_probe.link_count(alias) == 2
            assert displaced_path.read_bytes() == payload
            assert alias_path.read_bytes() == payload
    finally:
        if mutator is not None:
            _close_participant(mutator)
        if guardian is not None:
            _close_participant(guardian)

    assert mutator is not None
    assert mutator_return_code is not None and mutator_return_code != 0
    assert mutator.returncode == mutator_return_code
    assert guardian is not None and guardian.returncode == 0
    for process in (mutator, guardian):
        for stream in (process.stdin, process.stdout, process.stderr):
            assert stream is not None and stream.closed
    assert identity_probe.owned_count == 0
    assert lock_probe.owned_count == 0
    assert displaced_path.read_bytes() == payload
    assert alias_path.read_bytes() == payload
    assert not coordination_path.exists()
