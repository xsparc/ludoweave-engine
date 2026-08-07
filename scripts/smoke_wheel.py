"""Install the built wheel into a temporary environment and run public smoke checks."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import tomllib
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from command_receipt_stability_evidence import validate_command_receipt_stability_evidence
from constrained_3d_evidence import validate_constrained_3d_evidence
from cross_version_corpus_evidence import validate_cross_version_corpus_evidence
from external_consumer_feedback_evidence import validate_external_consumer_feedback_evidence
from external_contributor_rehearsal_evidence import (
    validate_external_contributor_rehearsal_evidence,
)
from external_sample_game_adoption_evidence import (
    validate_external_sample_game_adoption_evidence,
)
from operation_argument_evidence import validate_operation_argument_evidence
from receipt_reader_evidence import validate_receipt_reader_evidence
from receipt_semantic_evidence import validate_receipt_semantic_evidence
from supported_release_channel_evidence import validate_supported_release_channel_evidence
from visual_editor_evidence import validate_visual_editor_evidence
from wasm_mod_security_evidence import validate_wasm_mod_security_evidence


def _run(
    command: Sequence[str],
    *,
    cwd: Path,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        input=input_text,
    )
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
    project_root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((project_root / "pyproject.toml").read_text(encoding="utf-8"))
    version = cast(dict[str, object], project["project"])["version"]
    if not isinstance(version, str) or not version:
        raise RuntimeError("project.version must be non-empty text")
    wheels = sorted(dist.resolve().glob(f"ludoweave-{version}-*.whl"))
    if len(wheels) != 1:
        parser.error(f"expected exactly one LudoWeave wheel in {dist}, found {len(wheels)}")

    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("uv is required for the isolated wheel smoke test")

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
        if version_result.stdout.strip() != f"ludoweave {version}":
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

        gamepad_smoke = textwrap.dedent(
            """
            from ludoweave.app import ActionBinding, ActionMap, MappedInputSource
            from ludoweave.platform import (
                GamepadAxis,
                GamepadAxisEvent,
                GamepadButton,
                GamepadButtonEvent,
                GamepadConnectionEvent,
            )
            from ludoweave.render import NullRenderDevice

            source = MappedInputSource(ActionMap((
                ActionBinding("move.x", "gamepad:0:axis:left_x", 1.0, 0.2),
                ActionBinding("fire", "gamepad:0:button:a"),
            )))
            source.feed(GamepadConnectionEvent(0, True))
            source.feed(GamepadAxisEvent(0, GamepadAxis.LEFT_X, 0.6))
            source.feed(GamepadButtonEvent(0, GamepadButton.A, True))
            snapshot = source.snapshot_for_tick(0)
            assert abs(snapshot.value("move.x") - 0.5) < 1e-12
            assert snapshot.pressed("fire")
            assert snapshot.just_pressed("fire")
            device = NullRenderDevice()
            assert device.poll_gamepads() == ()
            device.close()
            """
        )
        _run([str(python), "-I", "-c", gamepad_smoke], cwd=temp_root)

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

        rich_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "rich_2d_showcase.py"),
                "--ticks",
                "6",
            ],
            cwd=temp_root,
        )
        rich = cast(dict[str, object], json.loads(rich_result.stdout))
        rich_expected = {
            "schema": "ludoweave.example.rich_2d/1",
            "ticks": 6,
            "animation_frame": 0,
            "audio_gain": 0.2,
            "glyphs": 9,
            "particles": 10,
            "tile_instances": 8,
            "sprite_instances": 20,
            "draw_calls": 2,
            "renderer": "null-device",
        }
        if any(rich.get(key) != value for key, value in rich_expected.items()):
            raise RuntimeError(f"rich 2D example summary was invalid: {rich!r}")

        conformance_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "render_device_conformance.py"),
            ],
            cwd=temp_root,
        )
        conformance = cast(dict[str, object], json.loads(conformance_result.stdout))
        checks = cast(list[dict[str, object]], conformance.get("checks"))
        if (
            conformance.get("protocol") != "ludoweave.render-device-conformance/1"
            or conformance.get("profile") != "render-device-baseline/1"
            or conformance.get("adapter_id") != "org.ludoweave.null"
            or conformance.get("adapter_name") != "null-device"
            or conformance.get("status") != "pass"
            or len(checks) != 9
            or any(check.get("status") != "pass" for check in checks)
        ):
            raise RuntimeError(f"render-device conformance report was invalid: {conformance!r}")

        agent_conformance_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "agent_tool_conformance.py"),
            ],
            cwd=temp_root,
        )
        agent_conformance = cast(dict[str, object], json.loads(agent_conformance_result.stdout))
        agent_checks = cast(list[dict[str, object]], agent_conformance.get("checks"))
        if (
            agent_conformance.get("protocol") != "ludoweave.agent-tool-conformance/1"
            or agent_conformance.get("profile") != "agent-tool-baseline/1"
            or agent_conformance.get("adapter_id") != "org.ludoweave.agent-service"
            or agent_conformance.get("status") != "pass"
            or len(agent_checks) != 12
            or any(check.get("status") != "pass" for check in agent_checks)
        ):
            raise RuntimeError(f"agent-tool conformance report was invalid: {agent_conformance!r}")

        for backend in ("world", "reference"):
            world_conformance_result = _run(
                [
                    str(python),
                    "-I",
                    str(project_root / "examples" / "world_store_conformance.py"),
                    "--backend",
                    backend,
                ],
                cwd=temp_root,
            )
            world_conformance = cast(dict[str, object], json.loads(world_conformance_result.stdout))
            world_checks = cast(list[dict[str, object]], world_conformance.get("checks"))
            if (
                world_conformance.get("protocol") != "ludoweave.world-store-conformance/1"
                or world_conformance.get("profile") != "world-store-baseline/1"
                or world_conformance.get("adapter_id") != f"ludoweave.{backend}"
                or world_conformance.get("status") != "pass"
                or len(world_checks) != 10
                or any(check.get("status") != "pass" for check in world_checks)
            ):
                raise RuntimeError(
                    f"world-store conformance report was invalid: {world_conformance!r}"
                )

        rollback_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "rollback_readiness.py"),
                "--ticks",
                "24",
                "--branch-tick",
                "12",
            ],
            cwd=temp_root,
        )
        rollback = cast(dict[str, object], json.loads(rollback_result.stdout))
        rollback_proof = cast(dict[str, object], rollback.get("proof", {}))
        if (
            rollback.get("schema") != "ludoweave.evaluation.rollback-readiness/1"
            or rollback.get("status") != "deferred"
            or rollback.get("transport_implemented") is not False
            or rollback_proof.get("lineage_verified") is not True
            or rollback_proof.get("input_rehydration_required") is not True
        ):
            raise RuntimeError(f"rollback readiness summary was invalid: {rollback!r}")

        constrained_3d_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "constrained_3d_decision.py"),
            ],
            cwd=temp_root,
        )
        constrained_3d = cast(dict[str, object], json.loads(constrained_3d_result.stdout))
        validate_constrained_3d_evidence(constrained_3d, version=version)

        visual_editor_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "visual_editor_decision.py"),
            ],
            cwd=temp_root,
        )
        visual_editor = cast(dict[str, object], json.loads(visual_editor_result.stdout))
        validate_visual_editor_evidence(visual_editor, version=version)

        wasm_security_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "wasm_mod_security_decision.py"),
            ],
            cwd=temp_root,
        )
        wasm_security = cast(dict[str, object], json.loads(wasm_security_result.stdout))
        validate_wasm_mod_security_evidence(wasm_security, version=version)

        command_receipt_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "command_receipt_stability_decision.py"),
            ],
            cwd=temp_root,
        )
        command_receipt = cast(dict[str, object], json.loads(command_receipt_result.stdout))
        validate_command_receipt_stability_evidence(command_receipt, version=version)

        operation_argument_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "operation_argument_compatibility.py"),
            ],
            cwd=temp_root,
        )
        operation_argument = cast(dict[str, object], json.loads(operation_argument_result.stdout))
        validate_operation_argument_evidence(operation_argument, version=version)

        receipt_reader_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "receipt_reader.py"),
            ],
            cwd=temp_root,
        )
        receipt_reader = cast(dict[str, object], json.loads(receipt_reader_result.stdout))
        validate_receipt_reader_evidence(receipt_reader, version=version)

        receipt_semantic_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "receipt_semantic_compatibility.py"),
            ],
            cwd=temp_root,
        )
        receipt_semantic = cast(dict[str, object], json.loads(receipt_semantic_result.stdout))
        validate_receipt_semantic_evidence(receipt_semantic, version=version)

        cross_version_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "cross_version_corpus_readiness.py"),
                "--corpus",
                str(project_root / "tests" / "fixtures" / "cross_version_receipt_corpus.json"),
            ],
            cwd=temp_root,
        )
        cross_version = cast(dict[str, object], json.loads(cross_version_result.stdout))
        validate_cross_version_corpus_evidence(cross_version, version=version)

        external_feedback_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "external_consumer_feedback_readiness.py"),
                "--corpus",
                str(project_root / "tests" / "fixtures" / "external_consumer_feedback.json"),
            ],
            cwd=temp_root,
        )
        external_feedback = cast(dict[str, object], json.loads(external_feedback_result.stdout))
        validate_external_consumer_feedback_evidence(external_feedback, version=version)

        external_contributor_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "external_contributor_rehearsal_readiness.py"),
                "--rehearsals",
                str(project_root / "tests" / "fixtures" / "external_contributor_rehearsal.json"),
            ],
            cwd=temp_root,
        )
        external_contributor = cast(
            dict[str, object], json.loads(external_contributor_result.stdout)
        )
        validate_external_contributor_rehearsal_evidence(external_contributor, version=version)

        external_sample_game_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "external_sample_game_adoption_readiness.py"),
                "--samples",
                str(project_root / "tests" / "fixtures" / "external_sample_game_adoption.json"),
            ],
            cwd=temp_root,
        )
        external_sample_game = cast(
            dict[str, object], json.loads(external_sample_game_result.stdout)
        )
        validate_external_sample_game_adoption_evidence(external_sample_game, version=version)

        release_channel_result = _run(
            [
                str(python),
                "-I",
                str(project_root / "examples" / "supported_release_channel_readiness.py"),
                "--channel",
                str(project_root / "tests" / "fixtures" / "supported_release_channel.json"),
            ],
            cwd=temp_root,
        )
        release_channel = cast(dict[str, object], json.loads(release_channel_result.stdout))
        validate_supported_release_channel_evidence(release_channel, version=version)

        plugin_manifest = temp_root / "example.plugin.json"
        shutil.copyfile(project_root / "examples" / "example.plugin.json", plugin_manifest)
        plugin_result = _run(
            [str(ludoweave), "plugin", "check", str(plugin_manifest)],
            cwd=temp_root,
        )
        plugin_report = cast(dict[str, object], json.loads(plugin_result.stdout))
        if (
            plugin_report.get("protocol") != "ludoweave.plugin-check/1"
            or plugin_report.get("compatible") is not True
            or plugin_report.get("plugin_count") != 1
            or str(plugin_manifest) in plugin_result.stdout
        ):
            raise RuntimeError(f"plugin manifest smoke was invalid: {plugin_report!r}")

        arena_smoke = textwrap.dedent(
            """
            from ludoweave.audio import AudioClipDescriptor, NullAudioBackend
            from ludoweave.collision import Aabb, Vec2, overlaps
            from ludoweave.samples import clockwork_input, create_clockwork_arena

            arena = create_clockwork_arena(clockwork_input(30))
            summary = arena.run(30)
            assert summary.ticks == 30
            assert summary.enemies_spawned == 3
            assert summary.state_hash.startswith("sha256:")
            assert overlaps(Aabb(Vec2(0.0, 0.0), 1.0, 1.0), Aabb(Vec2(1.0, 0.0), 1.0, 1.0))
            audio = NullAudioBackend()
            audio.initialize()
            clip = audio.load_clip(AudioClipDescriptor("smoke", 0.1), b"pcm")
            playback = audio.play(clip)
            audio.stop(playback)
            audio.close()
            """
        )
        _run([str(python), "-I", "-c", arena_smoke], cwd=temp_root)

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

        agent_request = {"transaction": transaction}
        (cli_project / "agent-request.json").write_text(
            json.dumps(agent_request, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
        agent_validation = _run(
            [
                str(ludoweave),
                "agent",
                str(cli_project),
                "transaction_validate",
                "agent-request.json",
                "--actor-kind",
                "test",
                "--actor-id",
                "wheel-smoke",
            ],
            cwd=temp_root,
        )
        validation = cast(dict[str, object], json.loads(agent_validation.stdout))
        validation_receipt = cast(dict[str, object], validation.get("receipt"))
        if validation_receipt.get("status") != "dry_run":
            raise RuntimeError(f"installed agent validation was invalid: {validation!r}")
        agent_apply = _run(
            [
                str(ludoweave),
                "agent",
                str(cli_project),
                "transaction_apply",
                "agent-request.json",
                "--write",
                "--actor-kind",
                "test",
                "--actor-id",
                "wheel-smoke",
            ],
            cwd=temp_root,
        )
        agent_result = cast(dict[str, object], json.loads(agent_apply.stdout))
        agent_receipt = cast(dict[str, object], agent_result.get("receipt"))
        if agent_receipt.get("status") != "committed":
            raise RuntimeError(f"installed agent apply was invalid: {agent_result!r}")

        mcp_input = "\n".join(
            (
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "initialize",
                        "params": {
                            "protocolVersion": "2025-11-25",
                            "capabilities": {},
                            "clientInfo": {"name": "wheel-smoke", "version": "1"},
                        },
                    }
                ),
                '{"jsonrpc":"2.0","method":"notifications/initialized"}',
                '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}',
                "",
            )
        )
        mcp_result = _run(
            [str(ludoweave), "mcp", str(cli_project)],
            cwd=temp_root,
            input_text=mcp_input,
        )
        mcp_responses = [json.loads(line) for line in mcp_result.stdout.splitlines()]
        if len(mcp_responses) != 2 or len(mcp_responses[1]["result"]["tools"]) != 12:
            raise RuntimeError(f"installed MCP stdio lifecycle was invalid: {mcp_responses!r}")

        shadow_package = temp_root / "ludoweave"
        shadow_package.mkdir()
        (shadow_package / "__init__.py").write_text("", encoding="utf-8")
        (shadow_package / "__main__.py").write_text(
            "from pathlib import Path\n"
            "Path('shadow-ludoweave-executed').write_text('unsafe', encoding='utf-8')\n"
            "raise SystemExit('shadow ludoweave executed')\n",
            encoding="utf-8",
        )
        inspector_result = _run(
            [
                str(ludoweave),
                "inspect",
                "--sample",
                "agent-world-builder",
                "--write",
                "--bootstrap",
                "--ticks",
                "1",
            ],
            cwd=temp_root,
        )
        inspector_events = [
            cast(dict[str, object], json.loads(line))
            for line in inspector_result.stdout.splitlines()
        ]
        if len(inspector_events) != 3:
            raise RuntimeError(
                f"installed inspector emitted an invalid event count: {inspector_events!r}"
            )
        if [event.get("cause") for event in inspector_events] != [
            "initial",
            "bootstrap",
            "tick",
        ]:
            raise RuntimeError(f"installed inspector emitted invalid causes: {inspector_events!r}")
        for sequence, event in enumerate(inspector_events):
            if (
                event.get("protocol") != "ludoweave.inspector.event/1"
                or event.get("sequence") != sequence
            ):
                raise RuntimeError(f"installed inspector emitted an invalid envelope: {event!r}")
        final_world = cast(dict[str, object], inspector_events[-1].get("world"))
        final_transition = cast(dict[str, object], inspector_events[-1].get("transition"))
        if final_world.get("completed_ticks") != 1 or final_transition.get("status") != "committed":
            raise RuntimeError(
                f"installed inspector did not emit a receipted tick: {inspector_events[-1]!r}"
            )
        if (temp_root / "shadow-ludoweave-executed").exists():
            raise RuntimeError("installed inspector child executed a cwd-shadowed package")

        builder_smoke = textwrap.dedent(
            """
            from ludoweave.agent import AgentCapture
            from ludoweave.samples import (
                create_agent_world_builder,
                run_agent_world_builder_acceptance,
            )

            class Capture:
                def capture(self, width: int, height: int) -> AgentCapture:
                    return AgentCapture(width, height, b"\\x00\\x00\\x00\\xff" * (width * height))

                def close(self) -> None:
                    pass

            builder = create_agent_world_builder(write=True, capture_provider=Capture())
            result = run_agent_world_builder_acceptance(builder.service)
            assert result["apply_status"] == "committed"
            assert result["adjust_status"] == "committed"
            assert result["tests_passed"] is True
            assert result["replay_batches"] == 5
            builder.close()
            """
        )
        _run([str(python), "-I", "-c", builder_smoke], cwd=temp_root)

    print(f"wheel smoke passed: {wheels[0].name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
