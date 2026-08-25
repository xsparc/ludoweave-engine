"""Unit tests for bounded explicit source-integrity locks."""

from __future__ import annotations

from collections.abc import Callable
from typing import cast

import pytest

from ludoweave.scene import (
    SOURCE_LOCK_PROTOCOL,
    SourceLock,
    SourceLockEntry,
    SourceLockLimits,
)
from ludoweave.scene.errors import SceneError
from ludoweave.world import canonical_dumps

_HASH_A = f"sha256:{'a' * 64}"
_HASH_B = f"sha256:{'b' * 64}"
_HASH_C = f"sha256:{'c' * 64}"


def _scene(entry_id: str = "main") -> dict[str, object]:
    return {
        "entry_id": entry_id,
        "kind": "scene",
        "source_protocol": "ludoweave.scene/1",
        "source_id": "main-scene",
        "source_sha256": _HASH_B,
    }


def _prefab(entry_id: str = "enemy") -> dict[str, object]:
    return {
        "entry_id": entry_id,
        "kind": "prefab",
        "source_protocol": "ludoweave.prefab/1",
        "instance_protocol": "ludoweave.prefab-instance/1",
        "source_id": "enemy-prefab",
        "instance_id": "enemy-one",
        "source_sha256": _HASH_B,
        "instance_sha256": _HASH_C,
    }


def _lock(*entries: dict[str, object]) -> bytes:
    return canonical_dumps(
        {
            "$schema": SOURCE_LOCK_PROTOCOL,
            "manifest_id": "project-sources",
            "manifest_sha256": _HASH_A,
            "entries": list(entries),
        }
    )


def test_source_lock_normalizes_entries_and_canonical_bytes() -> None:
    lock = SourceLock.from_json(_lock(_scene("z-scene"), _prefab("a-prefab")))

    assert lock.protocol == SOURCE_LOCK_PROTOCOL
    assert lock.manifest_id == "project-sources"
    assert lock.manifest_sha256 == _HASH_A
    assert tuple(entry.entry_id for entry in lock.entries) == ("a-prefab", "z-scene")
    assert lock.canonical_bytes() == canonical_dumps(lock.as_dict())
    assert lock.as_dict()["entries"] == [_prefab("a-prefab"), _scene("z-scene")]


@pytest.mark.parametrize(
    ("document", "code"),
    [
        (
            canonical_dumps(
                {
                    "$schema": "other/1",
                    "manifest_id": "sources",
                    "manifest_sha256": _HASH_A,
                    "entries": [_scene()],
                }
            ),
            "source_lock.incompatible_protocol",
        ),
        (_lock(), "source_lock.limit_exceeded"),
        (_lock(_scene("same"), _prefab("same")), "source_lock.duplicate_entry_id"),
        (
            canonical_dumps(
                {
                    "$schema": SOURCE_LOCK_PROTOCOL,
                    "manifest_id": "sources",
                    "manifest_sha256": "sha256:not-a-hash",
                    "entries": [_scene()],
                }
            ),
            "source_lock.invalid_hash",
        ),
        (
            _lock(
                {
                    **_scene(),
                    "instance_protocol": "ludoweave.prefab-instance/1",
                    "instance_id": "not-allowed",
                    "instance_sha256": _HASH_C,
                }
            ),
            "source_lock.invalid_document",
        ),
        (
            _lock(
                {
                    "entry_id": "prefab",
                    "kind": "prefab",
                    "source_protocol": "ludoweave.prefab/1",
                    "source_id": "prefab",
                    "source_sha256": _HASH_B,
                }
            ),
            "source_lock.invalid_document",
        ),
    ],
)
def test_source_lock_rejects_invalid_documents(document: bytes, code: str) -> None:
    with pytest.raises(SceneError) as caught:
        SourceLock.from_json(document)

    assert caught.value.code == code
    assert "not-a-hash" not in str(caught.value.as_dict())


def test_source_lock_applies_tightened_entry_limit() -> None:
    with pytest.raises(SceneError) as caught:
        SourceLock.from_json(
            _lock(_scene(), _prefab()),
            limits=SourceLockLimits(max_entries=1),
        )

    assert caught.value.code == "source_lock.limit_exceeded"
    assert dict(caught.value.details)["limit"] == 1


def test_source_lock_verifies_exact_identity_and_reports_first_field_only() -> None:
    expected = SourceLock.from_json(_lock(_scene(), _prefab()))
    expected.verify(SourceLock.from_json(_lock(_scene(), _prefab())))
    changed = SourceLock.from_json(
        _lock({**_scene(), "source_sha256": f"sha256:{'d' * 64}"}, _prefab())
    )

    with pytest.raises(SceneError) as caught:
        expected.verify(changed)

    assert caught.value.code == "source_lock.mismatch"
    assert dict(caught.value.details) == {"entry_id": "main", "field": "source_sha256"}
    assert _HASH_B not in str(caught.value.as_dict())


@pytest.mark.parametrize(
    ("actual", "details"),
    [
        (
            SourceLock.from_json(
                canonical_dumps(
                    {
                        "$schema": SOURCE_LOCK_PROTOCOL,
                        "manifest_id": "other-sources",
                        "manifest_sha256": _HASH_A,
                        "entries": [_scene()],
                    }
                )
            ),
            {"field": "manifest_id"},
        ),
        (
            SourceLock.from_json(
                canonical_dumps(
                    {
                        "$schema": SOURCE_LOCK_PROTOCOL,
                        "manifest_id": "project-sources",
                        "manifest_sha256": _HASH_C,
                        "entries": [_scene()],
                    }
                )
            ),
            {"field": "manifest_sha256"},
        ),
        (
            SourceLock.from_json(_lock(_scene("other-entry"))),
            {"field": "entries"},
        ),
    ],
)
def test_source_lock_verification_uses_stable_root_then_entry_precedence(
    actual: SourceLock,
    details: dict[str, str],
) -> None:
    expected = SourceLock.from_json(_lock(_scene()))

    with pytest.raises(SceneError) as caught:
        expected.verify(actual)

    assert caught.value.code == "source_lock.mismatch"
    assert dict(caught.value.details) == details


def test_source_lock_verification_requires_an_exact_current_value() -> None:
    expected = SourceLock.from_json(_lock(_scene()))

    with pytest.raises(SceneError) as caught:
        expected.verify(cast(SourceLock, object()))

    assert caught.value.code == "source_lock.invalid_verify"
    assert dict(caught.value.details) == {"actual_type": "object"}


@pytest.mark.parametrize(
    "factory",
    [
        lambda: SourceLockLimits(max_bytes=0),
        lambda: SourceLockLimits(max_entries=True),
        lambda: SourceLockLimits(max_entries=257),
        lambda: SourceLock.from_json(_lock(_scene()), limits=cast(SourceLockLimits, object())),
        lambda: SourceLockEntry(
            "scene",
            "scene",
            "ludoweave.scene/1",
            "main",
            _HASH_B,
            instance_protocol="ludoweave.prefab-instance/1",
        ),
    ],
)
def test_source_lock_rejects_invalid_limits_or_direct_entries(
    factory: Callable[[], object],
) -> None:
    with pytest.raises(SceneError):
        factory()
