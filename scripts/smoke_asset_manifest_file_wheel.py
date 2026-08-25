"""Install one wheel and verify bounded project-confined asset-manifest loading."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import textwrap
from collections.abc import Sequence
from hashlib import sha256
from pathlib import Path
from typing import cast


def _run(command: Sequence[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed with exit {result.returncode}: "
            f"{subprocess.list2cmdline(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def _python_in(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def _canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist", type=Path, help="directory containing exactly one wheel")
    args = parser.parse_args(argv)
    dist: object = getattr(args, "dist", None)
    if not isinstance(dist, Path) or not dist.is_dir():
        parser.error("dist must be an existing directory")
    wheels = sorted(dist.resolve().glob("ludoweave-*.whl"))
    if len(wheels) != 1:
        parser.error(f"expected exactly one LudoWeave wheel in {dist}, found {len(wheels)}")

    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("uv is required for the isolated asset-manifest wheel smoke test")
    project_root = Path(__file__).resolve().parents[1]
    local_temp = project_root / ".tmp"
    local_temp.mkdir(exist_ok=True)
    probe = textwrap.dedent(
        """
        import json
        import tempfile
        from hashlib import sha256
        from pathlib import Path

        import ludoweave.assets as assets
        from ludoweave.tools.headless_project import HeadlessProject, PROJECT_PROTOCOL

        names = {"ASSET_MANIFEST_PROTOCOL", "AssetManifestLimits"}
        assert names <= set(assets.__all__)
        assert all(assets.__stability__[name] == "experimental" for name in names)
        with tempfile.TemporaryDirectory(prefix="ludoweave-installed-assets-") as name:
            root = Path(name)
            project = {
                "protocol": PROJECT_PROTOCOL,
                "world_id": "installed-asset-manifest",
                "seed": "0000000000000001",
                "platform_profile": "cpython-portable-empty-v1",
                "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
            }
            manifest = {
                "protocol": assets.ASSET_MANIFEST_PROTOCOL,
                "assets": [
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
                ],
            }
            encode = lambda value: json.dumps(
                value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
            ).encode("utf-8")
            (root / "ludoweave.project.json").write_bytes(encode(project))
            (root / "assets.json").write_bytes(encode(manifest))
            loaded = HeadlessProject.load(root).load_asset_manifest("assets.json")
            summary = {
                "schema": "ludoweave.asset-manifest-file-wheel-smoke/1",
                "status": "pass",
                "protocol": loaded.protocol,
                "assets": len(loaded.entries),
                "uris": [entry.uri.value for entry in loaded.entries],
                "canonical_sha256": f"sha256:{sha256(loaded.canonical_bytes()).hexdigest()}",
                "sources_absent": not (root / "assets").exists(),
            }
            print(json.dumps(summary, sort_keys=True))
        """
    )
    with tempfile.TemporaryDirectory(
        prefix="ludoweave-asset-manifest-wheel-smoke-", dir=local_temp
    ) as temp_name:
        temp_root = Path(temp_name)
        environment = temp_root / "venv"
        _run([uv, "venv", "--python", "3.12", str(environment)], cwd=temp_root)
        python = _python_in(environment)
        _run(
            [uv, "pip", "install", "--python", str(python), "--no-deps", str(wheels[0])],
            cwd=temp_root,
        )
        result = _run([str(python), "-I", "-c", probe], cwd=temp_root)

    normalized: dict[str, object] = {
        "protocol": "ludoweave.assets/1",
        "assets": [
            {
                "uri": "asset://data/level.json",
                "kind": "json",
                "source": "assets/level.json",
                "settings": {},
                "dependencies": ["asset://textures/player.png"],
            },
            {
                "uri": "asset://textures/player.png",
                "kind": "png",
                "source": "assets/player.png",
                "settings": {"srgb": True},
                "dependencies": [],
            },
        ],
    }
    expected: dict[str, object] = {
        "schema": "ludoweave.asset-manifest-file-wheel-smoke/1",
        "status": "pass",
        "protocol": "ludoweave.assets/1",
        "assets": 2,
        "uris": ["asset://data/level.json", "asset://textures/player.png"],
        "canonical_sha256": f"sha256:{sha256(_canonical(normalized)).hexdigest()}",
        "sources_absent": True,
    }
    summary = cast(dict[str, object], json.loads(result.stdout))
    if summary != expected:
        raise RuntimeError(f"installed asset-manifest summary was invalid: {summary!r}")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
