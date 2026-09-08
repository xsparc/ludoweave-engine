"""Replay-owned input remains exact, bounded and independent of caller state."""

import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.app import InputAction, InputSnapshot, RecordedInputSource
from ludoweave.app.errors import InputError
from ludoweave.app.input import InputSource
from ludoweave.app.replay import InputReplay
from ludoweave.samples import clockwork_input, create_clockwork_arena
from ludoweave.samples.clockwork_arena import (
    ARENA_LOCK_HASH,
    ARENA_PLATFORM_PROFILE,
    ARENA_PROJECT_SCHEMA,
    ArenaTickExecutor,
    arena_tick_transaction,
)
from ludoweave.world import (
    IncompatibleReplayError,
    ReplayDivergenceError,
    ReplayRecorder,
    ReplayRunner,
)
from ludoweave.world.canonical import JsonValue, canonical_dumps, canonical_loads
from ludoweave.world.state import TickExecutor


def _artifact(ticks: int = 12) -> InputReplay:
    source = clockwork_input(ticks)
    arena = create_clockwork_arena(source)
    recorder = ReplayRecorder(
        arena.session,
        arena.codec,
        timeline_id="owned-input-test",
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )
    for _ in range(ticks):
        recorder.record(arena_tick_transaction(recorder.session))
    timeline = recorder.timeline()
    return InputReplay(timeline, tuple(source.snapshot_for_tick(tick) for tick in range(ticks)))


def _runner() -> ReplayRunner:
    arena = create_clockwork_arena(RecordedInputSource())
    return ReplayRunner(
        arena.codec,
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )


def test_replay_owns_input_and_preserves_legacy_bytes() -> None:
    artifact = _artifact()
    timeline = artifact.timeline
    original = timeline.canonical_bytes()
    restored = InputReplay.from_json(artifact.canonical_bytes())
    result = restored.replay(_runner(), ArenaTickExecutor)
    assert result.session.state_hash == timeline.final_state_hash
    assert restored.timeline.canonical_bytes() == original
    assert restored.canonical_bytes() == artifact.canonical_bytes()
    assert result.verified_checkpoints == timeline.checkpoints
    with pytest.raises(InputError, match="tick"):
        restored.snapshot_for_tick(12)


@given(st.floats(allow_nan=False, allow_infinity=False), st.booleans())
def test_input_value_identity(value: float, digital: bool) -> None:
    artifact = _artifact(1)
    snapshot = InputSnapshot(
        0,
        (InputAction("analog", value), InputAction("fire", digital), InputAction("zero", -0.0)),
        just_pressed=("fire",),
        just_released=("jump",),
    )
    original = replace(artifact, snapshots=(snapshot,))
    restored = InputReplay.from_json(original.canonical_bytes())
    assert restored.snapshots == original.snapshots
    assert cast(float, restored.snapshots[0].value("analog")).hex() == value.hex()
    assert cast(float, restored.snapshots[0].value("zero")).hex() == "-0x0.0p+0"
    assert type(restored.snapshots[0].value("fire")) is bool
    assert restored.artifact_hash() == original.artifact_hash()


@pytest.mark.parametrize("mode", ["missing", "duplicate", "reversed", "extra", "shifted"])
def test_complete_tick_coverage(mode: str) -> None:
    artifact = _artifact(2)
    snapshots = artifact.snapshots
    changed = {
        "missing": snapshots[:1],
        "duplicate": (snapshots[0], snapshots[0]),
        "reversed": snapshots[::-1],
        "extra": (*snapshots, InputSnapshot(2)),
        "shifted": (InputSnapshot(1), InputSnapshot(2)),
    }[mode]
    with pytest.raises(InputError):
        replace(artifact, snapshots=changed)


@pytest.mark.parametrize(
    "document",
    [b"\xff", b"{", b"[]", b"null", b'{"protocol":1,"protocol":2}', b'"\\ud800"'],
)
def test_malformed_json(document: bytes) -> None:
    with pytest.raises(InputError):
        InputReplay.from_json(document)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("tick", True),
        ("tick", -1),
        ("actions", []),
        ("actions", {"fire": 1}),
        ("actions", {"a" * 129: True}),
        ("just_pressed", ["fire", "fire"]),
        ("just_released", [False]),
        ("just_pressed", "fire"),
        ("unknown", None),
    ],
)
def test_invalid_snapshot_fields(field: str, value: JsonValue) -> None:
    document = cast(dict[str, JsonValue], canonical_loads(_artifact(1).canonical_bytes()))
    inputs = cast(list[JsonValue], document["inputs"])
    cast(dict[str, JsonValue], inputs[0])[field] = value
    with pytest.raises(InputError):
        InputReplay.from_json(canonical_dumps(document))


@pytest.mark.parametrize("count", [256, 257])
def test_action_limit_direct_and_decoded(count: int) -> None:
    artifact = _artifact(1)
    snapshot = InputSnapshot(0, tuple(InputAction(f"a{index}", True) for index in range(count)))
    if count == 256:
        value = replace(artifact, snapshots=(snapshot,))
        assert InputReplay.from_json(value.canonical_bytes()).snapshots == (snapshot,)
    else:
        with pytest.raises(InputError, match="limit"):
            replace(artifact, snapshots=(snapshot,))
        document = cast(dict[str, JsonValue], canonical_loads(artifact.canonical_bytes()))
        inputs = cast(list[JsonValue], document["inputs"])
        cast(dict[str, JsonValue], inputs[0])["actions"] = {
            action.name: action.value for action in snapshot.actions
        }
        with pytest.raises(InputError):
            InputReplay.from_json(canonical_dumps(document))


def test_zero_tick_artifact() -> None:
    artifact = _artifact(0)
    restored = InputReplay.from_json(artifact.canonical_bytes())
    assert restored.replay(_runner(), ArenaTickExecutor).batches_applied == 0
    with pytest.raises(InputError):
        restored.snapshot_for_tick(0)


def test_branch_owns_only_its_future_and_parent_is_unchanged() -> None:
    parent = _artifact(12)
    original = parent.canonical_bytes()
    runner = _runner()
    future = tuple(InputSnapshot(tick) for tick in range(6, 12))
    source = RecordedInputSource((*parent.snapshots[:6], *future))
    recorder = runner.branch(
        parent.timeline,
        at_tick=6,
        timeline_id="input-child",
        tick_executor=ArenaTickExecutor(source),
    )
    for _ in future:
        recorder.record(arena_tick_transaction(recorder.session))
    child = InputReplay(recorder.timeline(), future)
    result = InputReplay.from_json(child.canonical_bytes()).replay(runner, ArenaTickExecutor)
    assert result.session.state_hash == child.timeline.final_state_hash
    assert parent.canonical_bytes() == original
    with pytest.raises(InputError):
        child.snapshot_for_tick(5)


def test_fresh_process_uses_no_input_generator(tmp_path: Path) -> None:
    artifact = _artifact()
    program = """
import sys
from ludoweave.app import RecordedInputSource
from ludoweave.app.replay import InputReplay
from ludoweave.samples import create_clockwork_arena
from ludoweave.samples.clockwork_arena import (
    ARENA_LOCK_HASH, ARENA_PLATFORM_PROFILE, ARENA_PROJECT_SCHEMA, ArenaTickExecutor)
from ludoweave.world import ReplayRunner
artifact = InputReplay.from_json(sys.stdin.buffer.read())
arena = create_clockwork_arena(RecordedInputSource())
runner = ReplayRunner(arena.codec, project_schema=ARENA_PROJECT_SCHEMA,
    dependency_lock_hash=ARENA_LOCK_HASH, platform_profile=ARENA_PLATFORM_PROFILE)
print(artifact.replay(runner, ArenaTickExecutor).session.state_hash)
"""
    result = subprocess.run(
        [sys.executable, "-I", "-c", program],
        input=artifact.canonical_bytes(),
        cwd=tmp_path,
        capture_output=True,
        check=True,
        timeout=30,
    )
    assert result.stdout.decode().strip() == artifact.timeline.final_state_hash


def test_composition_failure_precedes_factory() -> None:
    artifact = _artifact(1)
    arena = create_clockwork_arena(RecordedInputSource())
    runner = ReplayRunner(
        arena.codec,
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash="sha256:" + "0" * 64,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )
    called = False

    def factory(source: InputSource) -> TickExecutor:
        nonlocal called
        called = True
        return ArenaTickExecutor(source)

    with pytest.raises(IncompatibleReplayError):
        artifact.replay(runner, factory)
    assert not called


def test_tampered_inputs_change_artifact_hash_and_diverge() -> None:
    artifact = _artifact(12)
    changed = replace(artifact, snapshots=tuple(InputSnapshot(tick) for tick in range(12)))
    assert changed.artifact_hash() != artifact.artifact_hash()
    assert changed.timeline.timeline_hash() == artifact.timeline.timeline_hash()
    with pytest.raises(ReplayDivergenceError):
        changed.replay(_runner(), ArenaTickExecutor)


@given(st.integers(max_value=-1))
def test_invalid_tick_lookup(tick: int) -> None:
    with pytest.raises(InputError):
        _artifact(0).snapshot_for_tick(tick)


@pytest.mark.parametrize("field", ["max_bytes", "max_nodes", "max_depth"])
def test_whole_document_budgets_apply_to_constructor_and_decoder(
    monkeypatch: pytest.MonkeyPatch,
    field: str,
) -> None:
    import ludoweave.app.replay as module

    artifact = _artifact(1)
    encoded = artifact.canonical_bytes()
    from ludoweave.world.canonical import JsonLimits

    limits = (
        JsonLimits(max_bytes=1)
        if field == "max_bytes"
        else (JsonLimits(max_nodes=1) if field == "max_nodes" else JsonLimits(max_depth=1))
    )
    monkeypatch.setattr(module, "_LIMITS", limits)
    with pytest.raises(InputError):
        replace(artifact)
    with pytest.raises(InputError):
        InputReplay.from_json(encoded)


def test_aggregate_limit_precedes_artifact_materialization(monkeypatch: pytest.MonkeyPatch) -> None:
    import ludoweave.app.replay as module

    artifact = _artifact(2)
    encoded = artifact.canonical_bytes()
    monkeypatch.setattr(module, "_MAX_ENTRIES", 1)
    with pytest.raises(InputError, match="limit"):
        replace(artifact)
    with pytest.raises(InputError, match="limit"):
        InputReplay.from_json(encoded)


@pytest.mark.parametrize("count", [1, 2])
def test_tick_limit_direct_and_decoder(monkeypatch: pytest.MonkeyPatch, count: int) -> None:
    import ludoweave.app.replay as module

    artifact = _artifact(count)
    encoded = artifact.canonical_bytes()
    monkeypatch.setattr(module, "_MAX_TICKS", 1)
    if count == 1:
        assert InputReplay.from_json(encoded).canonical_bytes() == encoded
    else:
        with pytest.raises(InputError, match="tick"):
            replace(artifact)
        with pytest.raises(InputError, match="tick"):
            InputReplay.from_json(encoded)
