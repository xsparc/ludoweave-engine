"""Source-integrity lock CLI integration tests."""

from __future__ import annotations

import json
import subprocess
import sys
from hashlib import sha256
from pathlib import Path
from typing import cast

from ludoweave.scene import SourceLock, SourceManifest
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
                "world_id": "source-lock-world",
                "seed": "0000000000000001",
                "platform_profile": "cpython-portable-empty-v1",
                "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
            }
        )
    )


def _scene_bytes(*, scene_id: str = "locked-scene") -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.scene/1",
            "scene_id": scene_id,
            "entities": [],
            "dependencies": ["asset://locked/scene.png"],
        }
    )


def _prefab_bytes() -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.prefab/1",
            "prefab_id": "locked-prefab",
            "entities": [],
            "dependencies": [],
        }
    )


def _instance_bytes() -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.prefab-instance/1",
            "prefab_id": "locked-prefab",
            "instance_id": "locked-instance",
            "overrides": [],
        }
    )


def _manifest_bytes() -> bytes:
    return canonical_dumps(
        {
            "$schema": "ludoweave.source-manifest/1",
            "manifest_id": "locked-sources",
            "entries": [
                {"entry_id": "scene", "kind": "scene", "source": "scene.json"},
                {
                    "entry_id": "prefab",
                    "kind": "prefab",
                    "source": "prefab.json",
                    "instance": "instance.json",
                },
            ],
        }
    )


def _write_sources(root: Path) -> None:
    (root / "scene.json").write_bytes(_scene_bytes())
    (root / "prefab.json").write_bytes(_prefab_bytes())
    (root / "instance.json").write_bytes(_instance_bytes())
    (root / "sources.json").write_bytes(_manifest_bytes())


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_source_lock_emits_canonical_path_silent_document_without_mutation(
    tmp_path: Path,
) -> None:
    _project(tmp_path)
    _write_sources(tmp_path)
    before = _files(tmp_path)

    result = _run_module("source", "lock", str(tmp_path), "--manifest", "sources.json")

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    lock = SourceLock.from_json(result.stdout)
    assert report == lock.as_dict()
    assert report["$schema"] == "ludoweave.source-lock/1"
    assert report["manifest_id"] == "locked-sources"
    entries = cast(list[object], report["entries"])
    assert [cast(dict[str, object], item)["entry_id"] for item in entries] == [
        "prefab",
        "scene",
    ]
    assert "scene.json" not in result.stdout
    assert str(tmp_path) not in result.stdout
    assert result.stdout.encode() == lock.canonical_bytes() + b"\n"
    assert _files(tmp_path) == before


def test_source_verify_accepts_exact_lock_without_mutation(tmp_path: Path) -> None:
    _project(tmp_path)
    _write_sources(tmp_path)
    generated = _run_module("source", "lock", str(tmp_path), "--manifest", "sources.json")
    assert generated.returncode == 0
    (tmp_path / "sources.lock.json").write_text(generated.stdout, encoding="utf-8")
    before = _files(tmp_path)

    result = _run_module(
        "source",
        "verify",
        str(tmp_path),
        "--manifest",
        "sources.json",
        "--lock",
        "sources.lock.json",
    )

    assert result.returncode == 0
    assert result.stderr == ""
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report == {
        "protocol": "ludoweave.cli.source-lock-verify/1",
        "status": "verified",
        "manifest_id": "locked-sources",
        "manifest_sha256": (
            f"sha256:{sha256(SourceManifest.from_json(_manifest_bytes()).canonical_bytes()).hexdigest()}"
        ),
        "entry_count": 2,
    }
    assert result.stdout.encode() == canonical_dumps(report) + b"\n"
    assert _files(tmp_path) == before


def test_source_verify_rejects_drift_without_hash_or_path_disclosure(tmp_path: Path) -> None:
    _project(tmp_path)
    _write_sources(tmp_path)
    generated = _run_module("source", "lock", str(tmp_path), "--manifest", "sources.json")
    assert generated.returncode == 0
    (tmp_path / "sources.lock.json").write_text(generated.stdout, encoding="utf-8")
    (tmp_path / "scene.json").write_bytes(_scene_bytes(scene_id="changed-scene"))
    before = _files(tmp_path)

    result = _run_module(
        "source",
        "verify",
        str(tmp_path),
        "--manifest",
        "sources.json",
        "--lock",
        "sources.lock.json",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "source_lock.mismatch"
    assert error["details"] == {"entry_id": "scene", "field": "source_id"}
    assert "scene.json" not in result.stderr
    assert "sha256:" not in result.stderr
    assert str(tmp_path) not in result.stderr
    assert _files(tmp_path) == before


def test_source_verify_rejects_manifest_identity_drift_before_entries(tmp_path: Path) -> None:
    _project(tmp_path)
    _write_sources(tmp_path)
    generated = _run_module("source", "lock", str(tmp_path), "--manifest", "sources.json")
    assert generated.returncode == 0
    (tmp_path / "sources.lock.json").write_text(generated.stdout, encoding="utf-8")
    changed = cast(dict[str, object], json.loads(_manifest_bytes()))
    changed["manifest_id"] = "other-sources"
    (tmp_path / "sources.json").write_bytes(canonical_dumps(changed))
    before = _files(tmp_path)

    result = _run_module(
        "source",
        "verify",
        str(tmp_path),
        "--manifest",
        "sources.json",
        "--lock",
        "sources.lock.json",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "source_lock.mismatch"
    assert error["details"] == {"field": "manifest_id"}
    assert "sha256:" not in result.stderr
    assert str(tmp_path) not in result.stderr
    assert _files(tmp_path) == before


def test_source_verify_confines_the_lock_file(tmp_path: Path) -> None:
    _project(tmp_path)
    _write_sources(tmp_path)
    outside = tmp_path.parent / "outside-source.lock.json"
    outside.write_bytes(canonical_dumps({}))

    result = _run_module(
        "source",
        "verify",
        str(tmp_path),
        "--manifest",
        "sources.json",
        "--lock",
        "../outside-source.lock.json",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    report = cast(dict[str, object], json.loads(result.stderr))
    error = cast(dict[str, object], report["error"])
    assert error["code"] == "tools.unsafe_path"
    assert str(outside) not in result.stderr


def test_source_lock_addition_retains_m124_check_output(tmp_path: Path) -> None:
    _project(tmp_path)
    _write_sources(tmp_path)

    result = _run_module("source", "check", str(tmp_path), "--manifest", "sources.json")

    assert result.returncode == 0
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["protocol"] == "ludoweave.cli.source-manifest-check/1"
    assert report["manifest_id"] == "locked-sources"
    assert report["entry_count"] == 2
