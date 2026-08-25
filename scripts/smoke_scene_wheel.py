"""Install one built wheel and verify the public scene transaction surface."""

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
        raise RuntimeError("uv is required for the isolated scene wheel smoke test")
    project_root = Path(__file__).resolve().parents[1]
    local_temp = project_root / ".tmp"
    local_temp.mkdir(exist_ok=True)

    probe = textwrap.dedent(
        """
        import json
        from dataclasses import dataclass
        from uuid import UUID

        from ludoweave.ecs import (
            ComponentRegistry,
            EntityId,
            ResourceRegistry,
            ResourceStore,
            World,
            component,
        )
        from ludoweave.scene import SceneDocument, SceneNode, compile_scene
        from ludoweave.world import (
            AuthorityResourceRegistry,
            CommandActor,
            ReceiptStatus,
            TransactionService,
            WorldSession,
        )

        @component(type_id=UUID("cccccccc-0000-0000-0000-000000000005"))
        @dataclass(frozen=True, slots=True)
        class InstalledTransform:
            x: int

        registry = ComponentRegistry((SceneNode, InstalledTransform))
        session = WorldSession(
            "installed-scene",
            World(registry),
            ResourceStore(ResourceRegistry()),
            authority_resources=AuthorityResourceRegistry(),
        )
        component_name = (
            f"{InstalledTransform.__module__}.{InstalledTransform.__qualname__}"
        )
        scene = SceneDocument.from_mapping({
            "$schema": "ludoweave.scene/1",
            "scene_id": "installed-scene",
            "entities": [{
                "local_id": "root",
                "name": "Root",
                "parent": None,
                "components": {
                    component_name: {"version": 1, "values": {"x": 4}},
                },
            }],
            "dependencies": ["asset://installed/scene.json"],
        })
        plan = compile_scene(
            scene,
            registry=registry,
            world_id=session.world_id,
            transaction_id="installed-scene-transaction",
            actor=CommandActor("smoke", "wheel"),
            instance_id="installed-instance",
        )
        receipt = TransactionService(session).apply(plan.transaction)
        assert receipt.status is ReceiptStatus.COMMITTED
        aliases = dict(receipt.aliases)
        index, generation = aliases["root"].split(":")
        entity = EntityId(int(index), int(generation))
        assert session.world.get(entity, InstalledTransform) == InstalledTransform(4)
        assert session.world.get(entity, SceneNode).local_id == "root"
        assert tuple(item.value for item in plan.dependencies) == (
            "asset://installed/scene.json",
        )
        print(json.dumps({
            "schema": "ludoweave.scene-wheel-smoke/1",
            "status": "pass",
            "commands": len(plan.transaction.commands),
            "aliases": sorted(aliases),
            "entities": len(session.world.entities()),
        }, sort_keys=True))
        """
    )
    with tempfile.TemporaryDirectory(
        prefix="ludoweave-scene-wheel-smoke-", dir=local_temp
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
        "schema": "ludoweave.scene-wheel-smoke/1",
        "status": "pass",
        "commands": 1,
        "aliases": ["root"],
        "entities": 1,
    }
    if summary != expected:
        raise RuntimeError(f"installed scene summary was invalid: {summary!r}")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
