"""Clockwork Arena fixed fixture, action replay, and presentation acceptance."""

import json
from pathlib import Path

from ludoweave.app import RecordedInputSource
from ludoweave.render import (
    NullRenderDevice,
    TextureData,
    TextureDescriptor,
    TextureFormat,
    TextureUsage,
)
from ludoweave.samples import ARENA_FIXED_SEED, clockwork_input, create_clockwork_arena
from ludoweave.samples.clockwork_arena import (
    ARENA_LOCK_HASH,
    ARENA_PLATFORM_PROFILE,
    ARENA_PROJECT_SCHEMA,
    ArenaTickExecutor,
    arena_tick_transaction,
)
from ludoweave.world import ReplayRecorder, ReplayRunner

_FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "clockwork_arena_3600.json"


def test_fixed_seed_3600_tick_headless_run_matches_exact_fixture() -> None:
    expected = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    arena = create_clockwork_arena(clockwork_input(3600), seed=ARENA_FIXED_SEED)

    summary = arena.run(3600)

    assert summary.as_dict() == expected


def test_recorded_action_stream_reproduces_3600_tick_hash_without_divergence() -> None:
    virtual = clockwork_input(3600)
    recorded = RecordedInputSource(virtual.snapshot_for_tick(tick) for tick in range(3600))
    arena = create_clockwork_arena(recorded, seed=ARENA_FIXED_SEED)

    summary = arena.run(3600)

    assert (
        summary.state_hash
        == "sha256:4243defe548ba6e36b6bec93b45f266d2ad48e74c24efc2856d3f7c6197a3b6e"
    )
    assert summary.ticks == 3600


def test_world_replay_verifies_clockwork_transactions_and_input_checkpoints() -> None:
    virtual = clockwork_input(120)
    snapshots = tuple(virtual.snapshot_for_tick(tick) for tick in range(120))
    live = create_clockwork_arena(RecordedInputSource(snapshots))
    recorder = ReplayRecorder(
        live.session,
        live.codec,
        timeline_id="clockwork-arena-replay",
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
        checkpoint_interval=30,
    )
    for _ in range(120):
        recorder.record(arena_tick_transaction(live.session))
    timeline = recorder.timeline()
    runner = ReplayRunner(
        live.codec,
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )

    replay = runner.replay(
        timeline,
        tick_executor=ArenaTickExecutor(RecordedInputSource(snapshots)),
    )

    assert replay.session.completed_ticks == 120
    assert replay.session.state_hash == live.session.state_hash == timeline.final_state_hash


def test_arena_extracts_all_active_gameplay_entities_without_mutating_authority() -> None:
    arena = create_clockwork_arena(clockwork_input(30))
    arena.run(30)
    before = arena.session.state_hash
    device = NullRenderDevice()
    texture = device.create_texture(
        TextureDescriptor(
            1,
            1,
            TextureFormat.RGBA8_UNORM,
            TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
            label="arena-fixture",
        ),
        TextureData(b"\xff\xff\xff\xff", 4),
    )
    try:
        frame = arena.presentation(texture)
    finally:
        device.close()

    summary = arena.summary()
    assert frame.visible_sprite_count == (1 + summary.enemies_active + summary.projectiles_active)
    assert frame.normal_sprite_draw_count == 1
    assert arena.session.state_hash == before
