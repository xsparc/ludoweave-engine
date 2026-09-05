"""Exact saved-plan verification and confined loading."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

from ludoweave.assets import (
    AssetBuildPlan,
    AssetEntry,
    AssetError,
    AssetKind,
    AssetManifest,
    AssetSourceLock,
    AssetSourceLockEntry,
    AssetUri,
)
from ludoweave.core.errors import LudoWeaveError
from ludoweave.tools.headless_project import PROJECT_PROTOCOL, HeadlessProject
from ludoweave.world import canonical_dumps


def _uri() -> AssetUri:
    return AssetUri("asset://data/item.json")


def _plan(root: Path, payload: bytes = b'{"value":1}') -> AssetBuildPlan:
    uri = _uri()
    manifest = AssetManifest(
        root,
        (AssetEntry(uri, AssetKind.JSON, "assets/item.json"),),
    )
    lock = AssetSourceLock(
        "sha256:" + "1" * 64,
        f"sha256:{sha256(manifest.canonical_bytes()).hexdigest()}",
        (uri,),
        (
            AssetSourceLockEntry(
                uri,
                AssetKind.JSON,
                f"sha256:{sha256(payload).hexdigest()}",
                len(payload),
            ),
        ),
    )
    return AssetBuildPlan.from_inputs(manifest, lock)


def _project(root: Path) -> HeadlessProject:
    (root / "ludoweave.project.json").write_bytes(
        canonical_dumps(
            {
                "protocol": PROJECT_PROTOCOL,
                "world_id": "asset-plan-verify-world",
                "seed": "0000000000000001",
                "platform_profile": "cpython-portable-empty-v1",
                "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
            }
        )
    )
    return HeadlessProject.load(root)


def test_asset_build_plan_verify_accepts_exact_and_rejects_content_silently(
    tmp_path: Path,
) -> None:
    expected = _plan(tmp_path)
    expected.verify(AssetBuildPlan.from_json(expected.canonical_bytes()))

    changed = _plan(tmp_path, b'{"value":2}')
    changed_with_expected_lock_identity = AssetBuildPlan(
        expected.asset_source_lock_sha256,
        expected.asset_manifest_sha256,
        expected.roots,
        changed.entries,
    )
    with pytest.raises(AssetError) as mismatch:
        expected.verify(changed_with_expected_lock_identity)
    assert mismatch.value.code == "asset_build_plan.mismatch"
    assert mismatch.value.details == (
        ("field", "source_sha256"),
        ("uri", "asset://data/item.json"),
    )
    report = str(mismatch.value.as_dict())
    assert expected.entries[0].source_sha256 not in report
    assert changed.entries[0].source_sha256 not in report
    assert expected.entries[0].cache_key not in report
    assert changed.entries[0].cache_key not in report

    with pytest.raises(AssetError) as invalid:
        expected.verify(object())  # type: ignore[arg-type]
    assert invalid.value.code == "asset_build_plan.invalid_verify"


def test_headless_project_loads_plan_confined_and_closes_descriptor(tmp_path: Path) -> None:
    project = _project(tmp_path)
    expected = _plan(tmp_path)
    source = tmp_path / "assets.plan.json"
    source.write_bytes(expected.canonical_bytes())

    assert project.load_asset_build_plan("assets.plan.json") == expected
    moved = tmp_path / "assets.plan.moved.json"
    source.rename(moved)
    moved.rename(source)

    with pytest.raises(LudoWeaveError) as unsafe:
        project.load_asset_build_plan("../assets.plan.json")
    assert unsafe.value.code == "tools.unsafe_path"
    assert unsafe.value.details == (("role", "asset_build_plan"),)
    assert str(tmp_path) not in str(unsafe.value.as_dict())

    with pytest.raises(LudoWeaveError) as invalid_limits:
        project.load_asset_build_plan(
            "assets.plan.json",
            limits=object(),  # type: ignore[arg-type]
        )
    assert invalid_limits.value.code == "tools.invalid_asset_build_plan_limits"
    assert invalid_limits.value.details == (("actual_type", "object"),)
