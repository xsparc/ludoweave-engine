"""Explicit project-confined prefab source and instance file loading tests."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import cast

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from ludoweave.core.errors import LudoWeaveError
from ludoweave.ecs import ComponentRegistry
from ludoweave.scene import (
    PrefabDocument,
    PrefabError,
    PrefabInstance,
    PrefabLimits,
    PrefabNode,
    SceneLimits,
    SceneNode,
    compile_prefab,
)
from ludoweave.tools.headless_project import PROJECT_PROTOCOL, HeadlessProject
from ludoweave.world import CommandActor, canonical_dumps


def _project(root: Path) -> HeadlessProject:
    manifest: dict[str, object] = {
        "protocol": PROJECT_PROTOCOL,
        "world_id": "prefab-file-world",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }
    (root / "ludoweave.project.json").write_bytes(canonical_dumps(manifest))
    return HeadlessProject.load(root)


def _prefab_bytes(*, prefab_id: str = "enemy.scout") -> bytes:
    value: dict[str, object] = {
        "$schema": "ludoweave.prefab/1",
        "prefab_id": prefab_id,
        "entities": [{"local_id": "root", "name": "Scout", "parent": None, "components": {}}],
        "dependencies": ["asset://sprites/scout.png"],
    }
    return canonical_dumps(value)


def _instance_bytes(*, prefab_id: str = "enemy.scout") -> bytes:
    value: dict[str, object] = {
        "$schema": "ludoweave.prefab-instance/1",
        "prefab_id": prefab_id,
        "instance_id": "scout-one",
        "overrides": [],
    }
    return canonical_dumps(value)


def test_prefab_file_loads_are_detached_and_do_not_mutate_world(tmp_path: Path) -> None:
    project = _project(tmp_path)
    sources = tmp_path / "prefabs"
    sources.mkdir()
    prefab_path = sources / "scout.prefab.json"
    instance_path = sources / "scout.instance.json"
    prefab_path.write_bytes(_prefab_bytes())
    instance_path.write_bytes(_instance_bytes())
    session = project.new_session()
    before = session.state_hash

    prefab = project.load_prefab("prefabs/scout.prefab.json")
    instance = project.load_prefab_instance("prefabs/scout.instance.json")
    prefab_baseline = prefab.canonical_bytes()
    instance_baseline = instance.canonical_bytes()
    prefab_path.write_bytes(_prefab_bytes(prefab_id="changed"))
    instance_path.write_bytes(_instance_bytes(prefab_id="changed"))
    prefab_path.unlink()
    instance_path.unlink()

    assert prefab == PrefabDocument.from_json(prefab_baseline)
    assert instance == PrefabInstance.from_json(instance_baseline)
    assert session.state_hash == before
    assert session.world.entities() == ()


@pytest.mark.parametrize(
    ("method", "role"),
    [("load_prefab", "prefab"), ("load_prefab_instance", "prefab_instance")],
)
@pytest.mark.parametrize("relative", ["../outside.json", "C:\\outside.json", "NUL"])
def test_prefab_file_paths_remain_project_relative(
    tmp_path: Path, method: str, role: str, relative: str
) -> None:
    project = _project(tmp_path)
    loader = getattr(project, method)

    with pytest.raises(LudoWeaveError) as captured:
        loader(relative)

    assert captured.value.code == "tools.unsafe_path"
    assert captured.value.details == (("role", role),)
    assert str(tmp_path) not in str(captured.value.as_dict())


@pytest.mark.parametrize(
    ("method", "payload", "expected_code"),
    [
        ("load_prefab", b"not-json", "prefab.invalid_json"),
        (
            "load_prefab_instance",
            b'{"$schema":"ludoweave.prefab-instance/2","prefab_id":"x",'
            b'"instance_id":"i","overrides":[]}',
            "prefab.incompatible_protocol",
        ),
    ],
)
def test_prefab_file_loads_preserve_structured_protocol_failures(
    tmp_path: Path, method: str, payload: bytes, expected_code: str
) -> None:
    project = _project(tmp_path)
    (tmp_path / "input.json").write_bytes(payload)
    loader = getattr(project, method)

    with pytest.raises(PrefabError) as captured:
        loader("input.json")

    assert captured.value.code == expected_code


@given(
    st.integers(
        min_value=1,
        max_value=min(len(_prefab_bytes()), len(_instance_bytes())) - 1,
    )
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_prefab_file_loads_enforce_every_tightened_byte_limit(tmp_path: Path, limit: int) -> None:
    project = _project(tmp_path)
    (tmp_path / "prefab.json").write_bytes(_prefab_bytes())
    (tmp_path / "instance.json").write_bytes(_instance_bytes())
    limits = PrefabLimits(scene=SceneLimits(max_bytes=limit))

    for method, relative, role in (
        (project.load_prefab, "prefab.json", "prefab"),
        (project.load_prefab_instance, "instance.json", "prefab_instance"),
    ):
        with pytest.raises(LudoWeaveError) as captured:
            method(relative, limits=limits)
        assert captured.value.code == "tools.input_oversized"
        assert captured.value.details == (("limit", limit), ("role", role))


def test_prefab_file_loads_reject_invalid_limits_before_path_access(tmp_path: Path) -> None:
    project = _project(tmp_path)
    invalid = cast(PrefabLimits, object())

    for method in (project.load_prefab, project.load_prefab_instance):
        with pytest.raises(LudoWeaveError) as captured:
            method("missing.json", limits=invalid)
        assert captured.value.code == "tools.invalid_prefab_limits"


def test_explicit_files_do_not_bypass_prefab_source_matching(tmp_path: Path) -> None:
    project = _project(tmp_path)
    (tmp_path / "prefab.json").write_bytes(_prefab_bytes())
    (tmp_path / "instance.json").write_bytes(_instance_bytes(prefab_id="other"))

    with pytest.raises(PrefabError) as captured:
        compile_prefab(
            project.load_prefab("prefab.json"),
            project.load_prefab_instance("instance.json"),
            registry=ComponentRegistry((PrefabNode, SceneNode)),
            world_id="prefab-file-world",
            transaction_id="prefab-file-transaction",
            actor=CommandActor("test", "prefab-file"),
        )

    assert captured.value.code == "prefab.source_mismatch"
