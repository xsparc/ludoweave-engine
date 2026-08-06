"""Release staging determinism, completeness, and tamper regressions."""

import json
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import cast

_ROOT = Path(__file__).resolve().parents[2]
_STAGE = _ROOT / "scripts" / "release_artifacts.py"
_SMOKE = _ROOT / "scripts" / "smoke_release.py"


def _fake_dist(root: Path) -> Path:
    dist = root / "dist"
    dist.mkdir()
    (dist / "ludoweave-0.1.0a1-py3-none-any.whl").write_bytes(b"pure-wheel-fixture")
    (dist / "ludoweave-0.1.0a1.tar.gz").write_bytes(b"sdist-fixture")
    return dist


def _stage(dist: Path, output: Path, *, tag: str | None = None) -> None:
    command = [sys.executable, str(_STAGE), str(dist), str(output)]
    if tag is not None:
        command.extend(("--tag", tag))
    result = subprocess.run(command, cwd=_ROOT, check=False, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_release_stage_is_reproducible_and_complete(tmp_path: Path) -> None:
    dist = _fake_dist(tmp_path)
    first = tmp_path / "first"
    second = tmp_path / "second"

    _stage(dist, first, tag="v0.1.0a1")
    _stage(dist, second)

    assert {path.name: path.read_bytes() for path in first.iterdir()} == {
        path.name: path.read_bytes() for path in second.iterdir()
    }
    manifest_value: object = json.loads(
        (first / "RELEASE_MANIFEST.json").read_text(encoding="utf-8")
    )
    assert isinstance(manifest_value, dict)
    manifest = cast(dict[str, object], manifest_value)
    assert manifest["protocol"] == "ludoweave.release-manifest/1"
    assert manifest["version"] == "0.1.0a1"

    bundle = first / "ludoweave-samples-0.1.0a1.zip"
    with zipfile.ZipFile(bundle) as archive:
        names = set(archive.namelist())
    prefix = "ludoweave-samples-0.1.0a1/"
    assert prefix + "README.md" in names
    assert prefix + "agent_tool_conformance.py" in names
    assert prefix + "alpha_acceptance.py" in names
    assert prefix + "render_device_conformance.py" in names
    assert prefix + "receipt_reader.py" in names
    assert prefix + "receipt_semantic_compatibility.py" in names
    assert prefix + "command_receipt_stability_decision.py" in names
    assert prefix + "operation_argument_compatibility.py" in names
    assert prefix + "constrained_3d_decision.py" in names
    assert prefix + "rich_2d_showcase.py" in names
    assert prefix + "rollback_readiness.py" in names
    assert prefix + "visual_editor_decision.py" in names
    assert prefix + "wasm_mod_security_decision.py" in names
    assert prefix + "world_store_conformance.py" in names
    assert prefix + "example.plugin.json" in names
    assert prefix + "assets/clockwork_arena.scene.json" in names
    assert all(name.startswith(prefix) and ".." not in name.split("/") for name in names)


def test_release_smoke_rejects_tampered_staged_file_before_install(tmp_path: Path) -> None:
    dist = _fake_dist(tmp_path)
    release = tmp_path / "release"
    _stage(dist, release)
    (release / "NOTICE").write_text("tampered", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(_SMOKE), str(release)],
        cwd=_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "release checksum mismatch for NOTICE" in result.stderr
