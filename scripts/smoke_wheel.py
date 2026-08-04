"""Install the built wheel into a temporary environment and run public smoke checks."""

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
        rendered = subprocess.list2cmdline(command)
        raise RuntimeError(
            f"command failed with exit {result.returncode}: {rendered}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def _python_in(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def _ludoweave_in(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "ludoweave.exe"
    return environment / "bin" / "ludoweave"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist", type=Path, help="directory containing exactly one wheel")
    args = parser.parse_args(argv)
    dist: object = getattr(args, "dist", None)
    if not isinstance(dist, Path):
        parser.error("dist must be a directory path")
    wheels = sorted(dist.resolve().glob("ludoweave-*.whl"))
    if len(wheels) != 1:
        parser.error(f"expected exactly one LudoWeave wheel in {dist}, found {len(wheels)}")

    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("uv is required for the isolated wheel smoke test")

    project_root = Path(__file__).resolve().parents[1]
    local_temp = project_root / ".tmp"
    local_temp.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ludoweave-wheel-smoke-", dir=local_temp) as temp_name:
        temp_root = Path(temp_name)
        environment = temp_root / "venv"
        _run([uv, "venv", "--python", "3.12", str(environment)], cwd=temp_root)
        python = _python_in(environment)
        _run(
            [uv, "pip", "install", "--python", str(python), "--no-deps", str(wheels[0])],
            cwd=temp_root,
        )

        ludoweave = _ludoweave_in(environment)
        version_result = _run([str(ludoweave), "--version"], cwd=temp_root)
        if version_result.stdout.strip() != "ludoweave 0.1.0.dev0":
            raise RuntimeError(f"unexpected version output: {version_result.stdout!r}")

        doctor_result = _run([str(ludoweave), "doctor"], cwd=temp_root)
        doctor = cast(dict[str, object], json.loads(doctor_result.stdout))
        if doctor.get("status") != "ok":
            raise RuntimeError(f"doctor did not report success: {doctor!r}")

        _run(
            [
                str(python),
                "-I",
                "-c",
                (
                    "from ludoweave.ecs import EntityAllocator; "
                    "allocator = EntityAllocator(); stale = allocator.create(); "
                    "allocator.destroy(stale); current = allocator.create(); "
                    "assert not allocator.is_alive(stale); "
                    "assert current.index == stale.index; "
                    "assert current.generation == stale.generation + 1"
                ),
            ],
            cwd=temp_root,
        )

        render_boundary_smoke = textwrap.dedent(
            """
            import sys

            import ludoweave.render
            from ludoweave.core.errors import RenderError
            from ludoweave.render.backends.wgpu import WgpuRenderDevice

            assert not ({"wgpu", "rendercanvas", "glfw", "numpy"} & set(sys.modules))
            try:
                WgpuRenderDevice()
            except RenderError as error:
                assert error.code == "render.backend_dependency_missing"
            else:
                raise AssertionError("no-dependency wheel unexpectedly initialized wgpu")
            """
        )
        _run([str(python), "-I", "-c", render_boundary_smoke], cwd=temp_root)

        schema_smoke = textwrap.dedent(
            """
            from collections.abc import Mapping
            from dataclasses import dataclass
            from uuid import UUID

            from ludoweave.ecs import ComponentMigration, ComponentRegistry, component

            def migrate(values: Mapping[str, object]) -> Mapping[str, object]:
                return {"value": int(values["value"]) + 1}

            @component(
                type_id=UUID("cccccccc-0000-0000-0000-000000000001"),
                version=2,
                migrations=(ComponentMigration(1, 2, migrate),),
            )
            @dataclass(slots=True)
            class InstalledComponent:
                value: int

            registry = ComponentRegistry((InstalledComponent,))
            source = {"value": 4}
            migrated = registry.migrate(
                UUID("cccccccc-0000-0000-0000-000000000001"),
                from_version=1,
                values=source,
            )
            assert migrated == {"value": 5}
            assert source == {"value": 4}
            """
        )
        _run([str(python), "-I", "-c", schema_smoke], cwd=temp_root)

        world_smoke = textwrap.dedent(
            """
            from dataclasses import dataclass
            from uuid import UUID

            from ludoweave.ecs import (
                ComponentRegistry,
                StaleEntityError,
                World,
                component,
            )

            @component(type_id=UUID("cccccccc-0000-0000-0000-000000000002"))
            @dataclass(slots=True)
            class InstalledPosition:
                x: int = 0

            @component(type_id=UUID("cccccccc-0000-0000-0000-000000000003"))
            @dataclass(slots=True)
            class InstalledVelocity:
                x: int = 0

            @component(type_id=UUID("cccccccc-0000-0000-0000-000000000004"))
            @dataclass(slots=True)
            class InstalledHidden:
                pass

            registry = ComponentRegistry(
                (InstalledPosition, InstalledVelocity, InstalledHidden)
            )
            world = World(registry)
            source = InstalledPosition(1)
            entity_id = world.spawn()
            world.add(entity_id, source)
            source.x = 99
            assert world.get(entity_id, InstalledPosition) == InstalledPosition(1)
            world.patch(entity_id, InstalledPosition, x=2)
            returned = world.get(entity_id, InstalledPosition)
            returned.x = 88
            assert world.get(entity_id, InstalledPosition) == InstalledPosition(2)
            assert world.remove(entity_id, InstalledPosition) == InstalledPosition(2)
            world.destroy(entity_id)
            replacement = world.spawn()
            assert replacement.index == entity_id.index
            assert replacement.generation == entity_id.generation + 1
            try:
                world.has(entity_id, InstalledPosition)
            except StaleEntityError:
                pass
            else:
                raise AssertionError("stale installed-wheel entity became valid")

            world.add(replacement, InstalledPosition(3))
            with world.query(InstalledPosition).writes(InstalledPosition).rows() as rows:
                queried_id, position = next(rows)
                assert queried_id == replacement
                position.x = 4
            assert world.get(replacement, InstalledPosition) == InstalledPosition(4)

            world.spawn(InstalledPosition(9), InstalledVelocity(9), InstalledHidden())
            changed_baseline = world.epoch
            commands = world.commands()
            pending = commands.spawn(InstalledPosition(5))
            commands.add(pending, InstalledVelocity(6))
            before_flush = world.entities()
            assert list(
                world.query(InstalledPosition, InstalledVelocity)
                .without(InstalledHidden)
                .changed_since(changed_baseline)
                .stable()
                .rows()
            ) == []
            assert world.entities() == before_flush
            result = world.flush(commands)
            spawned = result.resolve(pending)
            assert result.command_count == 2
            assert world.get(spawned, InstalledPosition) == InstalledPosition(5)
            assert list(
                world.query(InstalledPosition, InstalledVelocity)
                .without(InstalledHidden)
                .changed_since(changed_baseline)
                .stable()
                .rows()
            ) == [(spawned, InstalledPosition(5), InstalledVelocity(6))]
            """
        )
        _run([str(python), "-I", "-c", world_smoke], cwd=temp_root)

        schedule_smoke = textwrap.dedent(
            """
            from dataclasses import dataclass

            from ludoweave.ecs import (
                ComponentRegistry,
                ResourceRegistry,
                ResourceSpec,
                ResourceStore,
                Scheduler,
                SystemContext,
                system,
            )

            @dataclass(slots=True)
            class InstalledSettings:
                fixed_hz: int

            settings = ResourceSpec(
                "simulation.settings",
                InstalledSettings,
                lambda value: InstalledSettings(value.fixed_hz),
            )
            resources = ResourceRegistry((settings,))
            store = ResourceStore(resources, ((settings, InstalledSettings(60)),))
            detached = store.require(settings)
            detached.fixed_hz = 1
            assert store.require(settings).fixed_hz == 60

            @system(
                name="installed.writer",
                resource_writes=(settings,),
                before=("installed.reader",),
            )
            def writer(context: SystemContext, delta: float) -> None:
                del context, delta

            @system(name="installed.reader", resource_reads=(settings,))
            def reader(context: SystemContext, delta: float) -> None:
                del context, delta

            plan = Scheduler(ComponentRegistry(), resources).build((reader, writer))
            assert [spec.name for spec in plan.systems] == [
                "installed.writer",
                "installed.reader",
            ]
            assert len(plan.conflicts) == 1
            """
        )
        _run([str(python), "-I", "-c", schedule_smoke], cwd=temp_root)

        example_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "hello_headless.py"),
                "--ticks",
                "3",
            ],
            cwd=temp_root,
        )
        summary = cast(dict[str, object], json.loads(example_result.stdout))
        expected = {"ticks": 3, "frames": 3, "renderer": "null", "final_state": "closed"}
        if any(summary.get(key) != value for key, value in expected.items()):
            raise RuntimeError(f"headless example summary was invalid: {summary!r}")

        fixed_step_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "fixed_step_world.py"),
                "--ticks",
                "6",
            ],
            cwd=temp_root,
        )
        fixed_step = cast(dict[str, object], json.loads(fixed_step_result.stdout))
        fixed_expected = {
            "ticks": 6,
            "frames": 6,
            "entities": 6,
            "active": 3,
            "elapsed_ns": 100_000_000,
            "renderer": "null",
            "final_state": "closed",
        }
        if any(fixed_step.get(key) != value for key, value in fixed_expected.items()):
            raise RuntimeError(f"fixed-step example summary was invalid: {fixed_step!r}")

        cli_project = temp_root / "cli-project"
        cli_project.mkdir()
        manifest = {
            "protocol": "ludoweave.headless-project/1",
            "world_id": "wheel-world",
            "seed": "000000000000002a",
            "platform_profile": "cpython-portable-empty-v1",
            "dependency_lock_hash": "sha256:" + "0" * 64,
        }
        (cli_project / "ludoweave.project.json").write_text(
            json.dumps(manifest, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
        actor: dict[str, object] = {"kind": "test", "id": "wheel-smoke"}
        transaction: dict[str, object] = {
            "protocol": "ludoweave.transaction/1",
            "world_id": "wheel-world",
            "dry_run": False,
            "commands": [
                {
                    "protocol": "ludoweave.command/1",
                    "command_id": "wheel-spawn",
                    "transaction_id": "wheel-transaction",
                    "actor": actor,
                    "operation": "entity.spawn",
                    "operation_version": 1,
                    "arguments": {"alias": "subject", "components": []},
                },
                {
                    "protocol": "ludoweave.command/1",
                    "command_id": "wheel-tick",
                    "transaction_id": "wheel-transaction",
                    "actor": actor,
                    "operation": "world.tick",
                    "operation_version": 1,
                    "arguments": {"count": 1},
                },
            ],
        }
        (cli_project / "transaction.json").write_text(
            json.dumps(transaction, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
        apply_result = _run(
            [
                str(ludoweave),
                "apply",
                str(cli_project),
                "transaction.json",
                "--snapshot-out",
                "after.lws",
                "--receipt-out",
                "receipt.json",
                "--replay-out",
                "run.lwr",
                "--timeline-id",
                "wheel-smoke",
            ],
            cwd=temp_root,
        )
        receipt = cast(dict[str, object], json.loads(apply_result.stdout))
        if receipt.get("status") != "committed" or receipt.get("completed_ticks_after") != 1:
            raise RuntimeError(f"installed CLI apply receipt was invalid: {receipt!r}")

        _run(
            [
                str(ludoweave),
                "snapshot",
                str(cli_project),
                "run.lwr",
                "--tick",
                "0",
                "--out",
                "before.lws",
            ],
            cwd=temp_root,
        )
        replay_result = _run(
            [
                str(ludoweave),
                "replay",
                str(cli_project),
                "run.lwr",
                "--verify-hashes",
                "--snapshot-out",
                "replayed.lws",
            ],
            cwd=temp_root,
        )
        replay_report = cast(dict[str, object], json.loads(replay_result.stdout))
        if replay_report.get("status") != "verified" or replay_report.get("tick") != 1:
            raise RuntimeError(f"installed CLI replay report was invalid: {replay_report!r}")
        _run(
            [
                str(ludoweave),
                "snapshot",
                str(cli_project),
                "run.lwr",
                "--tick",
                "1",
                "--out",
                "tick-1.lws",
            ],
            cwd=temp_root,
        )
        diff_result = _run(
            [
                str(ludoweave),
                "diff",
                str(cli_project),
                "before.lws",
                "after.lws",
            ],
            cwd=temp_root,
        )
        diff_report = cast(dict[str, object], json.loads(diff_result.stdout))
        changes = cast(dict[str, object], diff_report.get("changes"))
        if changes.get("created_entities") != ["0:0"]:
            raise RuntimeError(f"installed CLI diff was invalid: {diff_report!r}")
        if (cli_project / "after.lws").read_bytes() != (cli_project / "replayed.lws").read_bytes():
            raise RuntimeError("installed CLI replay snapshot differs from apply snapshot")
        if (cli_project / "after.lws").read_bytes() != (cli_project / "tick-1.lws").read_bytes():
            raise RuntimeError("installed CLI extracted snapshot differs from apply snapshot")

    print(f"wheel smoke passed: {wheels[0].name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
