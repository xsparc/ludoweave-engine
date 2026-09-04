"""Real Git proof and fail-closed fixture handling, independent of repository ancestry."""

from __future__ import annotations

import hashlib
import zlib
from pathlib import Path

import pytest

from tests.integration import (
    test_windows_contained_source_access_source_commit_binding_probe as probe,
)
from tests.tools.git_source_fixture import materialize_m220_objects, read_m220_objects

_ROOT = Path(__file__).parents[2]
_MANIFEST = _ROOT / "tests/fixtures/m220_git_objects.json"


def test_pinned_objects_include_exact_real_source_bytes() -> None:
    objects = read_m220_objects()
    assert len(objects) == 5
    assert len({item.oid for item in objects}) == 5
    payload = objects[-1].content.split(b"\0", 1)[1]
    assert len(payload) == 3252
    assert (
        payload
        == (
            _ROOT / "tests/fixtures/windows_contained_source_access_bound_contender.py"
        ).read_bytes()
    )
    assert hashlib.sha256(payload).hexdigest() == (
        "fa01dae3119f817c62d0b27b0f575642c9837ad5259d79507bd2a1c09c41d2dd"
    )


def test_real_git_checks_all_historical_identities_in_isolated_store(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = materialize_m220_objects(tmp_path / "objects.git")
    monkeypatch.setattr(probe, "_ROOT", store)
    snapshot = probe._load_committed_source()  # pyright: ignore[reportPrivateUsage]
    assert snapshot.commit == "734d4eb943c3da7a1a8357ef3e180cac4353cb6b"
    assert snapshot.tree == "5575eeeb8123a0eaed9028a6281227b64fdfb73d"
    assert snapshot.parent == "09e6d3390040498371912d7d47bff5b75be03c35"
    assert snapshot.blob_oid == "10b71fc7d2d555160bf4a2869190a0b3e66d3330"
    assert snapshot.path == "tests/fixtures/windows_contained_source_access_bound_contender.py"
    assert snapshot.size == 3252
    assert (
        snapshot.sha256.hex() == "fa01dae3119f817c62d0b27b0f575642c9837ad5259d79507bd2a1c09c41d2dd"
    )
    assert not (store / "objects/info/alternates").exists()
    assert not (store / "hooks").exists()
    assert b"remote" not in (store / "config").read_bytes()


@pytest.mark.parametrize(
    "payload",
    [b"{}", b"x" * 16_385, _MANIFEST.read_bytes() + b"\n"],
    ids=["invalid-json", "oversized", "changed-bytes"],
)
def test_changed_manifest_refuses_before_creating_store(tmp_path: Path, payload: bytes) -> None:
    manifest = tmp_path / "changed.json"
    manifest.write_bytes(payload)
    destination = tmp_path / "objects.git"
    with pytest.raises(ValueError, match="manifest identity mismatch"):
        materialize_m220_objects(destination, manifest=manifest)
    assert not destination.exists()


def test_existing_destination_is_preserved(tmp_path: Path) -> None:
    destination = tmp_path / "objects.git"
    destination.mkdir()
    sentinel = destination / "sentinel"
    sentinel.write_bytes(b"preserved")
    with pytest.raises(FileExistsError):
        materialize_m220_objects(destination)
    assert list(destination.iterdir()) == [sentinel]
    assert sentinel.read_bytes() == b"preserved"


@pytest.mark.parametrize("missing_index", range(5))
def test_missing_object_still_fails_real_git_binding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, missing_index: int
) -> None:
    store = materialize_m220_objects(tmp_path / "objects.git")
    oid = read_m220_objects()[missing_index].oid
    (store / "objects" / oid[:2] / oid[2:]).unlink()
    monkeypatch.setattr(probe, "_ROOT", store)
    with pytest.raises(RuntimeError, match="fixed Git object read returned nonzero"):
        probe._load_committed_source()  # pyright: ignore[reportPrivateUsage]


def test_tampered_source_object_still_fails_real_git_binding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = materialize_m220_objects(tmp_path / "objects.git")
    oid = read_m220_objects()[-1].oid
    (store / "objects" / oid[:2] / oid[2:]).write_bytes(b"not a Git object")
    monkeypatch.setattr(probe, "_ROOT", store)
    with pytest.raises(RuntimeError, match="fixed Git object read returned nonzero"):
        probe._load_committed_source()  # pyright: ignore[reportPrivateUsage]


@pytest.mark.parametrize("field", ["parent", "tree", "blob"])
def test_validly_encoded_object_drift_does_not_pass_binding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, field: str
) -> None:
    store = materialize_m220_objects(tmp_path / "objects.git")
    objects = read_m220_objects()
    item = objects[-1] if field == "blob" else objects[0]
    if field == "blob":
        content = item.content[:-1] + b"!"
        expected = "source blob content did not match"
    else:
        original = (
            b"09e6d3390040498371912d7d47bff5b75be03c35"
            if field == "parent"
            else b"5575eeeb8123a0eaed9028a6281227b64fdfb73d"
        )
        content = item.content.replace(original, b"0" * 40)
        expected = "fixed Git object read returned nonzero"
    (store / "objects" / item.oid[:2] / item.oid[2:]).write_bytes(zlib.compress(content))
    monkeypatch.setattr(probe, "_ROOT", store)
    with pytest.raises(RuntimeError, match=expected):
        probe._load_committed_source()  # pyright: ignore[reportPrivateUsage]
