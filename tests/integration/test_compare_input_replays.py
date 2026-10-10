"""Replay comparison preserves verification, exact values and bounded output."""

import json
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import replace
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import cast

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from ludoweave.app import InputAction, InputSnapshot, RecordedInputSource
from ludoweave.app.replay import InputReplay
from ludoweave.render import NullRenderDevice
from ludoweave.samples import create_clockwork_arena
from ludoweave.samples.clockwork_arena import (
    ARENA_LOCK_HASH,
    ARENA_PLATFORM_PROFILE,
    ARENA_PROJECT_SCHEMA,
    ArenaTickExecutor,
    Player,
    arena_tick_transaction,
)
from ludoweave.world import (
    CommandTransaction,
    ReceiptStatus,
    ReplayRecorder,
    ReplayRunner,
    TransactionReceipt,
    TransactionService,
    WorldSession,
)
from ludoweave.world.canonical import JsonValue, canonical_dumps, canonical_loads
from ludoweave.world.random import RandomStreams

_ROOT = Path(__file__).resolve().parents[2]
_SPEC = spec_from_file_location(
    "compare_input_replays", _ROOT / "examples/compare_input_replays.py"
)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)
_compare = cast(Callable[[bytes, bytes], dict[str, JsonValue]], _MODULE.compare_documents)
_main = cast(Callable[[Sequence[str]], int], _MODULE.main)


def _record(
    ticks: int = 3,
    *,
    snapshots: tuple[InputSnapshot, ...] | None = None,
    seed: int = 42,
    stress: int = 1,
    label: str = "comparison-test",
    command_label: str | None = None,
) -> InputReplay:
    inputs = (
        snapshots if snapshots is not None else tuple(InputSnapshot(tick) for tick in range(ticks))
    )
    arena = create_clockwork_arena(RecordedInputSource(inputs), seed=seed, stress=stress)
    recorder = ReplayRecorder(
        arena.session,
        arena.codec,
        timeline_id=label,
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )
    for index in range(ticks):
        transaction = arena_tick_transaction(recorder.session)
        if command_label is not None:
            transaction = replace(
                transaction,
                commands=tuple(
                    replace(command, command_id=f"{command_label}.{index}")
                    for command in transaction.commands
                ),
            )
        assert recorder.record(transaction).status is ReceiptStatus.COMMITTED
    return InputReplay(recorder.timeline(), inputs)


def _report(left: InputReplay, right: InputReplay) -> dict[str, JsonValue]:
    return _compare(left.canonical_bytes(), right.canonical_bytes())


def _patch_health(session: WorldSession, health: int) -> CommandTransaction:
    entity, _ = session.world.components(Player)[0]
    schema = session.component_registry.schema_for_type(Player)
    tick = arena_tick_transaction(session)
    command = replace(
        tick.commands[0],
        operation="component.patch",
        arguments={
            "entity": {"index": entity.index, "generation": entity.generation},
            "type_id": str(schema.type_id),
            "version": schema.version,
            "changes": {"health": health},
        },
    )
    return replace(tick, commands=(command,))


def _difference(report: dict[str, JsonValue]) -> dict[str, JsonValue]:
    assert report["status"] == "different"
    return cast(dict[str, JsonValue], report["difference"])


def _detail(report: dict[str, JsonValue]) -> dict[str, JsonValue]:
    wrapper = cast(dict[str, JsonValue], _difference(report)["detail"])
    return cast(dict[str, JsonValue], wrapper["value"])


@pytest.mark.parametrize("ticks", [0, 1, 8])
def test_identical_history_ignores_timeline_labels(ticks: int) -> None:
    left = _record(ticks, label="first")
    right = _record(ticks, label="second")
    report = _report(left, right)
    assert report["schema"] == "ludoweave.input-replay-comparison/1"
    assert report["status"] == "identical"
    assert report["difference"] is None
    assert left.artifact_hash() != right.artifact_hash()
    assert cast(dict[str, JsonValue], report["left"])["artifact_hash"] == left.artifact_hash()


@pytest.mark.parametrize("reverse", [False, True])
def test_different_lengths(reverse: bool) -> None:
    left, right = _record(2), _record(5)
    if reverse:
        left, right = right, left
    diff = _difference(_report(left, right))
    assert diff["category"] == "length"
    assert diff["after_batch"] == 2
    assert diff["left_tick"] == diff["right_tick"] == 2


@pytest.mark.parametrize(
    "kind", ["digital", "analog", "pressed", "released", "signed_zero", "type"]
)
def test_exact_input_values_and_edges(kind: str) -> None:
    a = InputSnapshot(1, (InputAction("unused", 0.0),))
    b = {
        "digital": InputSnapshot(1, (InputAction("unused", True),)),
        "analog": InputSnapshot(1, (InputAction("unused", 0.5),)),
        "pressed": InputSnapshot(1, a.actions, just_pressed=("unused",)),
        "released": InputSnapshot(1, a.actions, just_released=("unused",)),
        "signed_zero": InputSnapshot(1, (InputAction("unused", -0.0),)),
        "type": InputSnapshot(1, (InputAction("unused", False),)),
    }[kind]
    left = _record(snapshots=(InputSnapshot(0), a, InputSnapshot(2)))
    right = _record(snapshots=(InputSnapshot(0), b, InputSnapshot(2)))
    diff = _difference(_report(left, right))
    assert diff["category"] == "input"
    assert diff["after_batch"] == diff["left_tick"] == 1
    assert _detail(_report(left, right))["input_tick"] == 1


def test_valid_transaction_content_difference() -> None:
    report = _report(_record(), _record(command_label="alternate"))
    assert _difference(report)["category"] == "transaction"
    assert _difference(report)["after_batch"] == 0
    assert _detail(report)["reason"] == "content"


def test_checkpoint_coverage_and_initial_coverage() -> None:
    original = _record()
    for boundary in (0, 2, 3):
        changed = replace(
            original,
            timeline=replace(
                original.timeline,
                checkpoints=tuple(
                    item for item in original.timeline.checkpoints if item.after_batch != boundary
                ),
            ),
        )
        diff = _difference(_report(original, changed))
        assert diff["category"] == "checkpoint"
        assert diff["after_batch"] == diff["left_tick"] == boundary


@pytest.mark.parametrize("kind", ["seed", "stress", "component"])
def test_initial_canonical_state_changes(kind: str) -> None:
    left = _record(0)
    if kind == "component":
        # Use a real engine-owned mutation before recording, not patched hash bytes.
        arena = create_clockwork_arena(RecordedInputSource(), seed=42)
        assert (
            TransactionService(arena.session).apply(_patch_health(arena.session, 19)).status
            is ReceiptStatus.COMMITTED
        )
        recorder = ReplayRecorder(
            arena.session,
            arena.codec,
            timeline_id="changed-component",
            project_schema=ARENA_PROJECT_SCHEMA,
            dependency_lock_hash=ARENA_LOCK_HASH,
            platform_profile=ARENA_PLATFORM_PROFILE,
        )
        right = InputReplay(recorder.timeline(), ())
    else:
        right = _record(0, seed=43) if kind == "seed" else _record(0, stress=2)
    report = _report(left, right)
    assert _difference(report)["category"] == "state"
    assert _difference(report)["after_batch"] == 0
    if kind == "component":
        changes = cast(dict[str, JsonValue], _detail(report)["changes"])
        components = cast(list[dict[str, JsonValue]], changes["components_changed"])
        assert components[0]["fields"] == ["health"]
    if kind == "seed":
        assert _detail(report)["random_changed"] is True


def _branch(parent: InputReplay, tick: int) -> InputReplay:
    arena = create_clockwork_arena(RecordedInputSource())
    runner = ReplayRunner(
        arena.codec,
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )
    recorder = runner.branch(
        parent.timeline, at_tick=tick, timeline_id="child", tick_executor=ArenaTickExecutor(parent)
    )
    for _ in range(tick, parent.timeline.final_tick):
        assert (
            recorder.record(arena_tick_transaction(recorder.session)).status
            is ReceiptStatus.COMMITTED
        )
    return InputReplay(recorder.timeline(), parent.snapshots[tick:])


def test_nonzero_start_and_incompatible_start() -> None:
    parent = _record(6)
    child = _branch(parent, 3)
    other = replace(
        child,
        timeline=replace(
            child.timeline, header=replace(child.timeline.header, timeline_id="other-child")
        ),
    )
    assert _report(child, other)["status"] == "identical"
    assert _report(parent, child)["status"] == "incompatible"
    shorter = replace(
        child,
        timeline=replace(
            child.timeline,
            batches=child.timeline.batches[:1],
            checkpoints=child.timeline.checkpoints[:2],
        ),
        snapshots=child.snapshots[:1],
    )
    diff = _difference(_report(child, shorter))
    assert diff["category"] == "length"
    assert diff["left_tick"] == 4


@pytest.mark.parametrize(
    "field", ["project_schema", "dependency_lock_hash", "platform_profile", "engine_version"]
)
def test_composition_mismatch(field: str) -> None:
    artifact = _record()
    document = cast(dict[str, JsonValue], canonical_loads(artifact.canonical_bytes()))
    timeline = cast(dict[str, JsonValue], document["timeline"])
    header = cast(dict[str, JsonValue], timeline["header"])
    header[field] = (
        "sha256:" + "a" * 64 if "hash" in field or field == "project_schema" else "different"
    )
    report = _compare(artifact.canonical_bytes(), canonical_dumps(document))
    assert report["status"] == "incompatible"
    assert report["difference"] is None


@pytest.mark.parametrize("data", [b"", b"{", b"null", b"\xff", b'"\\ud800"'])
def test_invalid_artifacts_are_separate(data: bytes) -> None:
    report = _compare(_record().canonical_bytes(), data)
    assert report["status"] == "invalid"
    assert report["difference"] is None
    assert cast(dict[str, JsonValue], report["left"])["verification"] == "pass"


def test_full_verification_after_early_input_difference() -> None:
    left = _record(4)
    right = _record(
        4, snapshots=tuple(InputSnapshot(tick, (InputAction("unused", True),)) for tick in range(4))
    )
    document = cast(dict[str, JsonValue], canonical_loads(right.canonical_bytes()))
    timeline = cast(dict[str, JsonValue], document["timeline"])
    batches = cast(list[dict[str, JsonValue]], timeline["batches"])
    batches[-1]["post_hash"] = "sha256:" + "0" * 64
    timeline["checkpoints"] = []
    report = _compare(left.canonical_bytes(), canonical_dumps(document))
    assert report["status"] == "invalid"
    assert report["difference"] is None


def test_corrupted_inputs_that_change_world_are_invalid() -> None:
    artifact = _record(2)
    changed = replace(
        artifact, snapshots=(InputSnapshot(0, (InputAction("move.x", 1.0),)), artifact.snapshots[1])
    )
    assert _report(artifact, changed)["status"] == "invalid"


def test_limits_before_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _MODULE
    monkeypatch.setattr(module, "_MAX_BYTES", 4)
    assert _compare(b"12345", b"12345")["status"] == "invalid"
    monkeypatch.setattr(module, "_MAX_BYTES", 67_108_864)
    monkeypatch.setattr(module, "_MAX_HISTORY", 2)

    def refuse() -> None:
        raise AssertionError("over-limit artifact must not execute")

    monkeypatch.setattr(module, "_runner", refuse)
    data = _record(3).canonical_bytes()
    report = _compare(data, data)
    assert report["status"] == "invalid"
    assert cast(dict[str, JsonValue], report["left"])["error"] == "history_limit"


def test_linear_batch_execution_and_no_renderer(monkeypatch: pytest.MonkeyPatch) -> None:
    artifact = _record(10)
    applies = 0
    original = TransactionService.apply

    def apply(service: TransactionService, transaction: CommandTransaction) -> TransactionReceipt:
        nonlocal applies
        applies += 1
        return original(service, transaction)

    def no_renderer(*args: object, **kwargs: object) -> None:
        raise AssertionError("comparison must be headless")

    monkeypatch.setattr(TransactionService, "apply", apply)
    monkeypatch.setattr(NullRenderDevice, "__init__", no_renderer)
    monkeypatch.setattr(ArenaTickExecutor, "effects", no_renderer, raising=False)
    assert _report(artifact, artifact)["status"] == "identical"
    assert applies == 40  # two complete preflights, two linear boundary walks


def test_detail_is_globally_bounded_and_truncation_explicit() -> None:
    many = InputSnapshot(
        0, tuple(InputAction(f"unused-{index:03}-" + "x" * 110, True) for index in range(256))
    )
    report = _report(_record(1), _record(1, snapshots=(many,)))
    diff = _difference(report)
    wrapper = cast(dict[str, JsonValue], diff["detail"])
    assert wrapper["truncated"] is True
    assert len(json.dumps(report)) < 32_768


@settings(max_examples=12, deadline=None)
@given(st.integers(min_value=0, max_value=6))
def test_report_is_deterministic(ticks: int) -> None:
    a = _record(ticks)
    b = _record(ticks + 1)
    assert canonical_dumps(_report(a, b)) == canonical_dumps(_report(a, b))


def test_cli_exit_codes_bytes_and_content_silent_io(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    left = tmp_path / "left.json"
    right = tmp_path / "right.json"
    original = _record().canonical_bytes()
    left.write_bytes(original)
    right.write_bytes(original)
    assert _main([str(left), str(right)]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "identical"
    right.write_bytes(_record(5).canonical_bytes())
    assert _main([str(left), str(right)]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "different"
    missing = tmp_path / "private-operator-file.json"
    assert _main([str(left), str(missing)]) == 2
    output = capsys.readouterr()
    io_report = json.loads(output.out)
    assert io_report["status"] == "invalid"
    assert io_report["right"]["content_hash"] is None
    assert io_report["right"]["error"] == "read_failure"
    assert "private-operator" not in output.out and not output.err
    assert left.read_bytes() == original
    result = subprocess.run(
        [sys.executable, str(_ROOT / "examples/compare_input_replays.py"), str(left), str(right)],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert result.returncode == 1
    assert json.loads(result.stdout)["status"] == "different"


def test_zero_tick_batch_range_difference() -> None:
    original = _record(1)
    arena = create_clockwork_arena(RecordedInputSource(original.snapshots), seed=42)
    recorder = ReplayRecorder(
        arena.session,
        arena.codec,
        timeline_id="zero-tick",
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )
    assert recorder.record(_patch_health(recorder.session, 20)).status is ReceiptStatus.COMMITTED
    # Only a command batch, so it has no input interval.
    other = InputReplay(recorder.timeline(), ())
    diff = _difference(_report(original, other))
    assert diff["category"] == "transaction"
    assert _detail(_report(original, other))["reason"] == "tick_range"
    assert _report(other, other)["status"] == "identical"


def test_raw_whitespace_is_not_gameplay_identity() -> None:
    original = _record().canonical_bytes()
    report = _compare(original, b" \n" + original + b"\n")
    assert report["status"] == "identical"
    a = cast(dict[str, JsonValue], report["left"])
    b = cast(dict[str, JsonValue], report["right"])
    assert a["content_hash"] != b["content_hash"]
    assert a["artifact_hash"] == b["artifact_hash"]


def test_world_identity_is_incompatible_not_state_divergence() -> None:
    arena = create_clockwork_arena(RecordedInputSource(), seed=42)
    session = WorldSession(
        "another-world",
        arena.session.world,
        arena.session.resources,
        authority_resources=arena.session.authority_resources,
        random_streams=RandomStreams(42),
    )
    recorder = ReplayRecorder(
        session,
        arena.codec,
        timeline_id="other-world",
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )
    other = InputReplay(recorder.timeline(), ())
    report = _report(_record(0), other)
    assert report["status"] == "incompatible"
    assert cast(dict[str, JsonValue], report["left"])["verification"] == "pass"
    assert cast(dict[str, JsonValue], report["right"])["verification"] == "pass"


def test_invalid_left_does_not_skip_right_verification(monkeypatch: pytest.MonkeyPatch) -> None:
    artifact = _record(4)
    applies = 0
    original = TransactionService.apply

    def apply(service: TransactionService, transaction: CommandTransaction) -> TransactionReceipt:
        nonlocal applies
        applies += 1
        return original(service, transaction)

    monkeypatch.setattr(TransactionService, "apply", apply)
    report = _compare(b"{", artifact.canonical_bytes())
    assert report["status"] == "invalid"
    assert cast(dict[str, JsonValue], report["right"])["verification"] == "pass"
    assert applies == 4


def test_invalid_has_precedence_over_incompatibility() -> None:
    artifact = _record()
    incompatible = replace(
        artifact,
        timeline=replace(
            artifact.timeline, header=replace(artifact.timeline.header, platform_profile="other")
        ),
    )
    report = _compare(b"{", incompatible.canonical_bytes())
    assert report["status"] == "invalid"
    assert cast(dict[str, JsonValue], report["right"])["verification"] == "incompatible"
