"""Project-confined, bounded scene-file loading tests."""

from __future__ import annotations

import os
from hashlib import sha256
from pathlib import Path
from typing import cast

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from ludoweave.core.errors import LudoWeaveError
from ludoweave.scene import SceneDocument, SceneError, SceneLimits
from ludoweave.tools.headless_project import PROJECT_PROTOCOL, HeadlessProject
from ludoweave.world import canonical_dumps


def _manifest() -> dict[str, object]:
    return {
        "protocol": PROJECT_PROTOCOL,
        "world_id": "scene-file-world",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }


def _project(root: Path) -> HeadlessProject:
    (root / "ludoweave.project.json").write_bytes(canonical_dumps(_manifest()))
    return HeadlessProject.load(root)


def _scene_bytes(*, scene_id: str = "loaded-scene") -> bytes:
    scene: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": scene_id,
        "entities": [
            {
                "local_id": "root",
                "name": "Root",
                "parent": None,
                "components": {},
            }
        ],
        "dependencies": ["asset://scenes/loaded.png"],
    }
    return canonical_dumps(scene)


def test_scene_file_load_is_detached_and_does_not_mutate_world(tmp_path: Path) -> None:
    project = _project(tmp_path)
    scenes = tmp_path / "scenes"
    scenes.mkdir()
    path = scenes / "main.json"
    path.write_bytes(_scene_bytes())
    session = project.new_session()
    before = session.state_hash

    document = project.load_scene("scenes/main.json")
    baseline = document.canonical_bytes()
    path.write_bytes(_scene_bytes(scene_id="changed-on-disk"))
    path.unlink()

    assert document == SceneDocument.from_json(baseline)
    assert document.scene_id == "loaded-scene"
    assert session.state_hash == before
    assert session.world.entities() == ()


@pytest.mark.parametrize(
    "relative",
    [
        "../outside.json",
        "..\\outside.json",
        "/absolute.json",
        "\\rooted.json",
        "C:\\absolute.json",
        "C:drive-relative.json",
        "scene.json:alternate",
        "NUL",
    ],
)
def test_scene_file_path_must_remain_project_relative(tmp_path: Path, relative: str) -> None:
    project = _project(tmp_path)

    with pytest.raises(LudoWeaveError) as captured:
        project.load_scene(relative)

    assert captured.value.code == "tools.unsafe_path"
    assert captured.value.details == (("role", "scene"),)
    assert str(tmp_path) not in str(captured.value.as_dict())


@pytest.mark.parametrize(
    ("payload", "expected_code"),
    [
        (b"not-json", "scene.invalid_json"),
        (
            b'{"$schema":"ludoweave.scene/2","scene_id":"x","entities":[],"dependencies":[]}',
            "scene.incompatible_protocol",
        ),
    ],
)
def test_scene_file_preserves_structured_document_failures(
    tmp_path: Path, payload: bytes, expected_code: str
) -> None:
    project = _project(tmp_path)
    (tmp_path / "scene.json").write_bytes(payload)

    with pytest.raises(SceneError) as captured:
        project.load_scene("scene.json")

    assert captured.value.code == expected_code


@given(st.integers(min_value=1, max_value=128))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_scene_file_enforces_every_tightened_byte_limit(tmp_path: Path, limit: int) -> None:
    project = _project(tmp_path)
    (tmp_path / "scene.json").write_bytes(_scene_bytes())

    with pytest.raises(LudoWeaveError) as captured:
        project.load_scene("scene.json", limits=SceneLimits(max_bytes=limit))

    assert captured.value.code == "tools.input_oversized"
    assert captured.value.details == (("limit", limit), ("role", "scene"))


def test_scene_file_caps_the_open_handle_when_size_metadata_is_stale(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _project(tmp_path)
    (tmp_path / "scene.json").write_bytes(_scene_bytes())
    real_fstat = os.fstat

    def stale_size(descriptor: int) -> os.stat_result:
        status = real_fstat(descriptor)
        values = list(status)
        values[6] = 0
        return os.stat_result(values)

    monkeypatch.setattr(os, "fstat", stale_size)
    with pytest.raises(LudoWeaveError) as captured:
        project.load_scene("scene.json", limits=SceneLimits(max_bytes=32))

    assert captured.value.code == "tools.input_oversized"


def test_scene_file_rejects_non_regular_input_and_invalid_limits(tmp_path: Path) -> None:
    project = _project(tmp_path)
    (tmp_path / "scenes").mkdir()

    with pytest.raises(LudoWeaveError) as unavailable:
        project.load_scene("scenes")
    assert unavailable.value.code == "tools.input_unavailable"

    with pytest.raises(LudoWeaveError) as invalid_limits:
        project.load_scene("missing.json", limits=cast(SceneLimits, object()))
    assert invalid_limits.value.code == "tools.invalid_scene_limits"


def test_scene_file_symlink_escape_is_rejected_when_supported(tmp_path: Path) -> None:
    project = _project(tmp_path)
    outside = tmp_path.parent / f"{tmp_path.name}-outside-scene.json"
    outside.write_bytes(_scene_bytes())
    link = tmp_path / "linked-scene.json"
    try:
        link.symlink_to(outside)
    except OSError:
        outside.unlink(missing_ok=True)
        pytest.skip("file symlinks are unavailable for this test account")
    try:
        with pytest.raises(LudoWeaveError) as captured:
            project.load_scene("linked-scene.json")
        assert captured.value.code == "tools.unsafe_path"
    finally:
        outside.unlink(missing_ok=True)
