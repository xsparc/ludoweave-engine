"""Bounded project-confined loading for existing asset manifests."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from hashlib import sha256
from pathlib import Path
from typing import cast

import pytest

from ludoweave.assets import (
    ASSET_MANIFEST_PROTOCOL,
    AssetError,
    AssetManifest,
    AssetManifestLimits,
)
from ludoweave.core.errors import LudoWeaveError
from ludoweave.tools.headless_project import PROJECT_PROTOCOL, HeadlessProject
from ludoweave.world import canonical_dumps


def _project(root: Path) -> HeadlessProject:
    (root / "ludoweave.project.json").write_bytes(
        canonical_dumps(
            {
                "protocol": PROJECT_PROTOCOL,
                "world_id": "asset-manifest-world",
                "seed": "0000000000000001",
                "platform_profile": "cpython-portable-empty-v1",
                "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
            }
        )
    )
    return HeadlessProject.load(root)


def _manifest(*, reverse: bool = False) -> dict[str, object]:
    assets: list[dict[str, object]] = [
        {
            "uri": "asset://textures/player.png",
            "kind": "png",
            "source": "assets/player.png",
            "settings": {"srgb": True},
            "dependencies": [],
        },
        {
            "uri": "asset://data/level.json",
            "kind": "json",
            "source": "assets/level.json",
            "settings": {},
            "dependencies": ["asset://textures/player.png"],
        },
    ]
    if reverse:
        assets.reverse()
    return {"protocol": ASSET_MANIFEST_PROTOCOL, "assets": assets}


def test_project_loads_bounded_asset_manifest_without_reading_asset_sources(
    tmp_path: Path,
) -> None:
    project = _project(tmp_path)
    document = canonical_dumps(_manifest())
    (tmp_path / "assets.json").write_bytes(document)

    manifest = project.load_asset_manifest("assets.json")

    assert manifest.protocol == ASSET_MANIFEST_PROTOCOL
    assert manifest.project_root == tmp_path.resolve()
    assert tuple(entry.uri.value for entry in manifest.entries) == (
        "asset://data/level.json",
        "asset://textures/player.png",
    )
    assert (
        manifest.canonical_bytes()
        == AssetManifest.from_json(
            canonical_dumps(_manifest(reverse=True)), project_root=tmp_path
        ).canonical_bytes()
    )
    assert not (tmp_path / "assets").exists()


def test_existing_path_loader_delegates_to_the_bounded_canonical_contract(
    tmp_path: Path,
) -> None:
    document = _manifest()
    path = tmp_path / "assets.json"
    path.write_text(json.dumps(document, indent=2), encoding="utf-8")

    manifest = AssetManifest.load(path, project_root=tmp_path)

    decoded = cast(dict[str, object], json.loads(manifest.canonical_bytes()))
    assert decoded["protocol"] == ASSET_MANIFEST_PROTOCOL
    assert len(cast(list[object], decoded["assets"])) == 2
    path.replace(tmp_path / "renamed-assets.json")


def test_asset_manifest_limits_may_tighten_only() -> None:
    limits = AssetManifestLimits(max_assets=1)
    assert limits.max_assets == 1
    assert not hasattr(limits, "__dict__")
    with pytest.raises(FrozenInstanceError):
        limits.max_assets = 2  # type: ignore[misc]

    for invalid in (True, 0, -1):
        with pytest.raises(AssetError) as raised:
            AssetManifestLimits(max_assets=invalid)  # type: ignore[arg-type]
        assert raised.value.code == "asset.invalid_manifest_limits"
    with pytest.raises(AssetError) as above_maximum:
        AssetManifestLimits(max_assets=4_097)
    assert above_maximum.value.details == (
        ("actual", 4_097),
        ("field", "max_assets"),
        ("maximum", 4_096),
    )


def test_project_loader_enforces_byte_and_entry_limits(tmp_path: Path) -> None:
    project = _project(tmp_path)
    document = canonical_dumps(_manifest())
    (tmp_path / "assets.json").write_bytes(document)

    with pytest.raises(LudoWeaveError) as oversized:
        project.load_asset_manifest(
            "assets.json", limits=AssetManifestLimits(max_bytes=len(document) - 1)
        )
    assert oversized.value.code == "tools.input_oversized"
    assert oversized.value.details == (
        ("limit", len(document) - 1),
        ("role", "asset_manifest"),
    )

    with pytest.raises(AssetError) as too_many:
        project.load_asset_manifest("assets.json", limits=AssetManifestLimits(max_assets=1))
    assert too_many.value.code == "asset.manifest_limit_exceeded"
    assert too_many.value.details == (("actual", 2), ("field", "assets"), ("limit", 1))


def test_project_loader_requires_exact_limits_and_confined_path(tmp_path: Path) -> None:
    project = _project(tmp_path)

    with pytest.raises(LudoWeaveError) as wrong_limits:
        project.load_asset_manifest("assets.json", limits=cast(AssetManifestLimits, object()))
    assert wrong_limits.value.code == "tools.invalid_asset_manifest_limits"

    with pytest.raises(LudoWeaveError) as escaped:
        project.load_asset_manifest("../outside-assets.json")
    assert escaped.value.code == "tools.unsafe_path"
    assert str(tmp_path) not in str(escaped.value.as_dict())


def test_asset_manifest_decoder_rejects_nonexact_or_overbounded_shapes(tmp_path: Path) -> None:
    unexpected = _manifest()
    unexpected["extra"] = True
    with pytest.raises(AssetError) as root_fields:
        AssetManifest.from_json(canonical_dumps(unexpected), project_root=tmp_path)
    assert root_fields.value.code == "asset.invalid_manifest"

    document = _manifest()
    assets = cast(list[dict[str, object]], document["assets"])
    assets[0]["dependencies"] = ["asset://data/level.json", "asset://data/other.json"]
    with pytest.raises(AssetError) as dependencies:
        AssetManifest.from_json(
            canonical_dumps(document),
            project_root=tmp_path,
            limits=AssetManifestLimits(max_dependencies=1),
        )
    assert dependencies.value.code == "asset.manifest_limit_exceeded"
    assert dependencies.value.details == (
        ("actual", 2),
        ("field", "dependencies"),
        ("limit", 1),
    )

    document = _manifest()
    assets = cast(list[dict[str, object]], document["assets"])
    assets[0]["settings"] = {"one": 1, "two": 2}
    with pytest.raises(AssetError) as settings:
        AssetManifest.from_json(
            canonical_dumps(document),
            project_root=tmp_path,
            limits=AssetManifestLimits(max_settings=1),
        )
    assert settings.value.code == "asset.manifest_limit_exceeded"
    assert settings.value.details == (
        ("actual", 2),
        ("field", "settings"),
        ("limit", 1),
    )


def test_asset_manifest_decode_failures_are_structured_and_chained(tmp_path: Path) -> None:
    with pytest.raises(AssetError) as raised:
        AssetManifest.from_json(b'{"protocol":', project_root=tmp_path)

    assert raised.value.code == "asset.invalid_manifest_json"
    assert raised.value.details == (("cause_type", "JSONDecodeError"),)
    assert raised.value.__cause__ is not None


@pytest.mark.parametrize(
    "document",
    (
        b"\xff",
        b'{"protocol":"ludoweave.assets/1","protocol":"duplicate","assets":[]}',
        b'{"protocol":"ludoweave.assets/1","assets":[],"number":NaN}',
        b'{"protocol":"ludoweave.assets/1","assets":[],"number":1e400}',
    ),
)
def test_asset_manifest_requires_unique_utf8_finite_json(tmp_path: Path, document: bytes) -> None:
    with pytest.raises(AssetError) as raised:
        AssetManifest.from_json(document, project_root=tmp_path)

    assert raised.value.code == "asset.invalid_manifest_json"


def test_asset_manifest_rejects_unsafe_decoded_text_before_path_or_encoding(
    tmp_path: Path,
) -> None:
    document = _manifest()
    assets = cast(list[dict[str, object]], document["assets"])
    assets[0]["settings"] = {"label": "\ud800"}

    with pytest.raises(AssetError) as raised:
        AssetManifest.from_json(
            json.dumps(document, ensure_ascii=True),
            project_root=tmp_path,
        )

    assert raised.value.code == "asset.invalid_value"
    assert raised.value.details == (("field", "settings"),)

    assets[0]["settings"] = {"\ud800": "label"}
    with pytest.raises(AssetError) as surrogate_key:
        AssetManifest.from_json(
            json.dumps(document, ensure_ascii=True),
            project_root=tmp_path,
        )
    assert surrogate_key.value.code == "asset.invalid_value"
    assert surrogate_key.value.details == (("field", "settings"),)

    assets[0]["settings"] = {}
    assets[0]["source"] = "assets/\x00.png"
    with pytest.raises(AssetError) as nul_path:
        AssetManifest.from_json(
            json.dumps(document, ensure_ascii=True),
            project_root=tmp_path,
        )
    assert nul_path.value.code == "asset.invalid_value"
    assert nul_path.value.details == (("field", "source"),)
