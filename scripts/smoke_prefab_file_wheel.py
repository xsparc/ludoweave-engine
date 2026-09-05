"""Install one built wheel and verify project-confined prefab-file loading."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import textwrap
from collections.abc import Sequence
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
        raise RuntimeError("uv is required for the isolated prefab-file wheel smoke test")
    project_root = Path(__file__).resolve().parents[1]
    local_temp = project_root / ".tmp"
    local_temp.mkdir(exist_ok=True)

    probe = textwrap.dedent(
        """
        import json
        import tempfile
        from dataclasses import dataclass
        from hashlib import sha256
        from pathlib import Path
        from uuid import UUID

        from ludoweave.ecs import (
            ComponentRegistry,
            EntityId,
            ResourceRegistry,
            ResourceStore,
            World,
            component,
        )
        from ludoweave.scene import PrefabNode, SceneNode, compile_prefab
        from ludoweave.tools.headless_project import PROJECT_PROTOCOL, HeadlessProject
        from ludoweave.world import (
            AuthorityResourceRegistry,
            CommandActor,
            ReceiptStatus,
            TransactionService,
            WorldSession,
            canonical_dumps,
        )

        @component(type_id=UUID("cccccccc-0000-0000-0000-000000000008"))
        @dataclass(frozen=True, slots=True)
        class InstalledPrefabFileValue:
            amount: int

        registry = ComponentRegistry((PrefabNode, SceneNode, InstalledPrefabFileValue))
        component_name = (
            f"{InstalledPrefabFileValue.__module__}.{InstalledPrefabFileValue.__qualname__}"
        )
        with tempfile.TemporaryDirectory(prefix="ludoweave-installed-prefab-file-") as name:
            root = Path(name)
            (root / "prefabs").mkdir()
            (root / "ludoweave.project.json").write_bytes(canonical_dumps({
                "protocol": PROJECT_PROTOCOL,
                "world_id": "installed-prefab-file",
                "seed": "0000000000000001",
                "platform_profile": "cpython-portable-empty-v1",
                "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
            }))
            (root / "prefabs" / "source.json").write_bytes(canonical_dumps({
                "$schema": "ludoweave.prefab/1",
                "prefab_id": "installed-prefab-file",
                "entities": [{
                    "local_id": "root",
                    "name": "Root",
                    "parent": None,
                    "components": {
                        component_name: {"version": 1, "values": {"amount": 4}},
                    },
                }],
                "dependencies": ["asset://installed/prefab-file.json"],
            }))
            (root / "prefabs" / "instance.json").write_bytes(canonical_dumps({
                "$schema": "ludoweave.prefab-instance/1",
                "prefab_id": "installed-prefab-file",
                "instance_id": "installed-file-instance",
                "overrides": [{
                    "local_id": "root",
                    "component": component_name,
                    "version": 1,
                    "changes": {"amount": 9},
                }],
            }))
            project = HeadlessProject.load(root)
            prefab = project.load_prefab("prefabs/source.json")
            instance = project.load_prefab_instance("prefabs/instance.json")

        session = WorldSession(
            "installed-prefab-file",
            World(registry),
            ResourceStore(ResourceRegistry()),
            authority_resources=AuthorityResourceRegistry(),
        )
        plan = compile_prefab(
            prefab,
            instance,
            registry=registry,
            world_id=session.world_id,
            transaction_id="installed-prefab-file-transaction",
            actor=CommandActor("smoke", "wheel"),
        )
        receipt = TransactionService(session).apply(plan.transaction)
        assert receipt.status is ReceiptStatus.COMMITTED
        aliases = dict(receipt.aliases)
        index, generation = aliases["root"].split(":")
        entity = EntityId(int(index), int(generation))
        assert session.world.get(entity, InstalledPrefabFileValue) == InstalledPrefabFileValue(9)
        assert session.world.get(entity, PrefabNode).prefab_id == prefab.prefab_id
        assert session.world.get(entity, SceneNode).instance_id == instance.instance_id
        print(json.dumps({
            "schema": "ludoweave.prefab-file-wheel-smoke/1",
            "status": "pass",
            "source_id": prefab.prefab_id,
            "instance_id": instance.instance_id,
            "commands": len(plan.transaction.commands),
            "aliases": sorted(aliases),
            "entities": len(session.world.entities()),
        }, sort_keys=True))
        """
    )
    with tempfile.TemporaryDirectory(
        prefix="ludoweave-prefab-file-wheel-smoke-", dir=local_temp
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

    summary = cast(dict[str, object], json.loads(result.stdout))
    expected: dict[str, object] = {
        "schema": "ludoweave.prefab-file-wheel-smoke/1",
        "status": "pass",
        "source_id": "installed-prefab-file",
        "instance_id": "installed-file-instance",
        "commands": 1,
        "aliases": ["root"],
        "entities": 1,
    }
    if summary != expected:
        raise RuntimeError(f"installed prefab-file summary was invalid: {summary!r}")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
