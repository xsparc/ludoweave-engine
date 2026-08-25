"""Read-only source-check CLI integration tests."""

from __future__ import annotations

import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from typing import cast

import pytest

from ludoweave.tools.headless_project import PROJECT_PROTOCOL
from ludoweave.world import canonical_dumps


def _run_module(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "ludoweave", *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def _project(root: Path) -> None:
    (root / "ludoweave.project.json").write_bytes(
        canonical_dumps(
            {
                "protocol": PROJECT_PROTOCOL,
                "world_id": "source-check-world",
                "seed": "0000000000000001",
                "platform_profile": "cpython-portable-empty-v1",
                "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
            }
        )
    )


def _scene_bytes() -> bytes:
    value: dict[str, object] = {
        "$schema": "ludoweave.scene/1",
        "scene_id": "checked-scene",
        "entities": [{"local_id": "root", "name": "Root", "parent": None, "components": {}}],
        "dependencies": ["asset://checked/scene.png"],
    }
    return canonical_dumps(value)


def _prefab_bytes(*, prefab_id: str = "checked-prefab") -> bytes:
    value: dict[str, object] = {
        "$schema": "ludoweave.prefab/1",
        "prefab_id": prefab_id,
        "entities": [{"local_id": "root", "name": "Root", "parent": None, "components": {}}],
        "dependencies": ["asset://checked/prefab.png"],
    }
    return canonical_dumps(value)


def _instance_bytes(*, prefab_id: str = "checked-prefab") -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.prefab-instance/1",
            "prefab_id": prefab_id,
            "instance_id": "checked-instance",
            "overrides": [],
        }
    )


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_source_check_scene_emits_canonical_read_only_summary(tmp_path: Path) -> None:
    _project(tmp_path)
    (tmp_path / "scene.json").write_bytes(_scene_bytes())
    before = _files(tmp_path)

    result = _run_module(
        "source",
        "check",
        str(tmp_path),
        "--scene",
        "scene.json",
    )

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report == {
        "protocol": "ludoweave.cli.source-check/1",
        "status": "valid",
        "kind": "scene",
        "source_protocol": "ludoweave.scene/1",
        "source_id": "checked-scene",
        "source_sha256": f"sha256:{sha256(_scene_bytes()).hexdigest()}",
        "entities": 1,
        "dependencies": 1,
    }
    assert result.stdout.encode() == canonical_dumps(report) + b"\n"
    assert _files(tmp_path) == before


def test_source_check_prefab_validates_two_explicit_files_without_mutation(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    (tmp_path / "prefab.json").write_bytes(_prefab_bytes())
    (tmp_path / "instance.json").write_bytes(_instance_bytes())
    before = _files(tmp_path)

    result = _run_module(
        "source",
        "check",
        str(tmp_path),
        "--prefab",
        "prefab.json",
        "--instance",
        "instance.json",
    )

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report == {
        "protocol": "ludoweave.cli.source-check/1",
        "status": "valid",
        "kind": "prefab",
        "source_protocol": "ludoweave.prefab/1",
        "instance_protocol": "ludoweave.prefab-instance/1",
        "source_id": "checked-prefab",
        "instance_id": "checked-instance",
        "source_sha256": f"sha256:{sha256(_prefab_bytes()).hexdigest()}",
        "instance_sha256": f"sha256:{sha256(_instance_bytes()).hexdigest()}",
        "entities": 1,
        "overrides": 0,
        "dependencies": 1,
    }
    assert result.stdout.encode() == canonical_dumps(report) + b"\n"
    assert _files(tmp_path) == before


def test_source_check_rejects_mismatched_prefab_pair_without_disclosing_paths(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    (tmp_path / "prefab.json").write_bytes(_prefab_bytes())
    (tmp_path / "instance.json").write_bytes(_instance_bytes(prefab_id="other"))
    before = _files(tmp_path)

    result = _run_module(
        "source",
        "check",
        str(tmp_path),
        "--prefab",
        "prefab.json",
        "--instance",
        "instance.json",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert report["protocol"] == "ludoweave.cli.error/1"
    assert error["code"] == "tools.prefab_source_mismatch"
    assert str(tmp_path) not in result.stderr
    assert _files(tmp_path) == before


@pytest.mark.parametrize(
    "arguments",
    [
        ("--prefab", "prefab.json"),
        ("--scene", "scene.json", "--instance", "instance.json"),
    ],
)
def test_source_check_rejects_incomplete_or_mixed_mode(
    tmp_path: Path, arguments: tuple[str, ...]
) -> None:
    _project(tmp_path)

    result = _run_module("source", "check", str(tmp_path), *arguments)

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "tools.invalid_argument"


def test_source_check_inherits_project_path_confinement(tmp_path: Path) -> None:
    _project(tmp_path)
    outside = tmp_path.parent / "outside-source.json"
    outside.write_bytes(_scene_bytes())

    result = _run_module(
        "source",
        "check",
        str(tmp_path),
        "--scene",
        "..\\outside-source.json",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "tools.unsafe_path"
    assert str(tmp_path) not in result.stderr
    assert str(outside) not in result.stderr
