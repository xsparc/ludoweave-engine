"""Verified recorded gameplay drives presentation without live input authority."""

import json
from collections.abc import Callable, Sequence
from dataclasses import replace
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import cast

import pytest

from ludoweave.app import InputAction, InputSnapshot, RecordedInputSource
from ludoweave.app.replay import InputReplay
from ludoweave.core.clock import VirtualClock
from ludoweave.platform import CloseEvent, KeyEvent, PlatformEvent, ResizeEvent
from ludoweave.render import NullRenderDevice, RenderDevice, SurfaceDescriptor, SurfaceHandle
from ludoweave.samples import create_clockwork_arena
from ludoweave.samples.clockwork_arena import (
    ARENA_LOCK_HASH,
    ARENA_PLATFORM_PROFILE,
    ARENA_PROJECT_SCHEMA,
    ArenaTickExecutor,
    arena_tick_transaction,
)
from ludoweave.world import (
    CommandTransaction,
    ReplayBatch,
    ReplayCheckpoint,
    ReplayDivergenceError,
    ReplayResult,
    ReplayRunner,
    ReplayTimeline,
    TransactionReceipt,
    TransactionService,
)
from ludoweave.world.state import TickExecutor

_ROOT = Path(__file__).resolve().parents[2]


def _module(name: str) -> ModuleType:
    spec = spec_from_file_location(name, _ROOT / "examples" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _record(path: Path, ticks: int) -> InputReplay:
    record = cast(Callable[[int], InputReplay], _module("input_replay").record)
    artifact = record(ticks)
    path.write_bytes(artifact.canonical_bytes())
    return artifact


def _main(module: ModuleType, args: Sequence[str]) -> int:
    return cast(Callable[[Sequence[str]], int], module.main)(args)


def _provider(device: RenderDevice) -> Callable[[str], RenderDevice]:
    def create(name: str) -> RenderDevice:
        return device

    return create


class _Device(NullRenderDevice):
    def __init__(self, close_at: int = -1, *, fail: bool = False) -> None:
        super().__init__()
        self.closes = 0
        self.polls = 0
        self.close_at = close_at
        self.fail = fail

    def create_surface(self, descriptor: SurfaceDescriptor) -> SurfaceHandle:
        if self.fail:
            raise RuntimeError("injected renderer failure")
        return super().create_surface(descriptor)

    def drain_surface_events(self, handle: SurfaceHandle) -> tuple[PlatformEvent, ...]:
        super().drain_surface_events(handle)
        self.polls += 1
        if self.polls == self.close_at:
            return (CloseEvent(),)
        return (KeyEvent("r", True), ResizeEvent(800, 600))

    def close(self) -> None:
        self.closes += 1
        super().close()


@pytest.mark.parametrize("ticks", [0, 1, 12])
def test_null_playback_matches_verified_final_state_and_initial_frame(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], ticks: int
) -> None:
    path = tmp_path / "recording.json"
    artifact = _record(path, ticks)
    assert _main(_module("play_input_replay"), [str(path)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["schema"] == "ludoweave.input-replay-playback/1"
    assert result["verification"] == "pass"
    assert result["playback"] == "complete"
    assert result["frames"] == ticks + 1
    assert result["played_batches"] == ticks
    assert result["arena"]["state_hash"] == artifact.timeline.final_state_hash
    assert result["verified_state_hash"] == artifact.timeline.final_state_hash
    assert result["verified_checkpoints"] == ticks + 1


@pytest.mark.parametrize("close_at,played,frames", [(1, 0, 0), (3, 1, 2), (-1, 3, 4)])
def test_window_pacing_close_and_live_input_isolation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    close_at: int,
    played: int,
    frames: int,
) -> None:
    path = tmp_path / "window.json"
    artifact = _record(path, 3)
    module = _module("play_input_replay")
    device = _Device(close_at)
    clock = VirtualClock()
    monkeypatch.setattr(module, "_device", _provider(device))
    monkeypatch.setattr(module, "MonotonicClock", lambda: clock)
    assert _main(module, [str(path), "--renderer", "wgpu", "--window"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["played_batches"] == played
    assert result["frames"] == frames
    assert result["playback"] == ("complete" if played == 3 else "interrupted")
    assert result["verification"] == "pass"
    assert result["verified_state_hash"] == artifact.timeline.final_state_hash
    assert clock.now_ns() == played * 1_000_000_000 // 60
    assert device.closes == 1
    if played == 3:
        assert result["arena"]["state_hash"] == artifact.timeline.final_state_hash


def test_divergent_input_is_rejected_before_renderer_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "corrupt.json"
    artifact = _record(path, 1)
    altered = replace(artifact, snapshots=(InputSnapshot(0, (InputAction("move.x", -1.0),)),))
    path.write_bytes(altered.canonical_bytes())
    module = _module("play_input_replay")

    def forbidden(name: str) -> RenderDevice:
        pytest.fail("renderer constructed before complete verification")

    monkeypatch.setattr(module, "_device", forbidden)
    with pytest.raises(ReplayDivergenceError):
        _main(module, [str(path), "--renderer", "wgpu", "--window"])


def test_renderer_failure_closes_owned_device(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "valid.json"
    _record(path, 1)
    module = _module("play_input_replay")
    device = _Device(fail=True)
    monkeypatch.setattr(module, "_device", _provider(device))
    with pytest.raises(RuntimeError, match="injected"):
        _main(module, [str(path)])
    assert device.closes == 1


def test_playback_uses_two_replay_passes_not_a_prefix_replay_per_frame(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "linear.json"
    _record(path, 120)
    calls: list[int | None] = []
    original = ReplayRunner.replay

    def observe(
        self: ReplayRunner,
        timeline: ReplayTimeline | str | bytes,
        *,
        tick_executor: TickExecutor | None = None,
        verify_hashes: bool = True,
        max_batches: int | None = None,
    ) -> ReplayResult:
        calls.append(max_batches)
        assert verify_hashes
        return original(
            self,
            timeline,
            tick_executor=tick_executor,
            verify_hashes=verify_hashes,
            max_batches=max_batches,
        )

    monkeypatch.setattr(ReplayRunner, "replay", observe)
    assert _main(_module("play_input_replay"), [str(path)]) == 0
    assert calls == [None, 0]


def test_nonzero_branch_plays_from_its_own_initial_snapshot(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "branch.json"
    parent = _record(path, 6)
    composition = create_clockwork_arena(RecordedInputSource())
    runner = ReplayRunner(
        composition.codec,
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )
    recorder = runner.branch(
        parent.timeline,
        at_tick=3,
        timeline_id="visible-branch",
        tick_executor=ArenaTickExecutor(parent),
    )
    for _ in range(3):
        recorder.record(arena_tick_transaction(recorder.session))
    child = InputReplay(recorder.timeline(), parent.snapshots[3:])
    path.write_bytes(child.canonical_bytes())
    assert _main(_module("play_input_replay"), [str(path)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["arena"]["ticks"] == 6
    assert result["played_batches"] == 3
    assert result["frames"] == 4
    assert result["arena"]["state_hash"] == child.timeline.final_state_hash


def test_tick_budget_is_admitted_before_replay_or_renderer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "oversized.json"
    initial = _record(path, 0).timeline
    arena = create_clockwork_arena(RecordedInputSource())
    digest = initial.header.initial_state_hash
    timeline = ReplayTimeline(
        initial.header,
        initial.initial_snapshot,
        (ReplayBatch(0, 0, 3601, digest, digest, arena_tick_transaction(arena.session)),),
        (*initial.checkpoints, ReplayCheckpoint(1, 3601, digest)),
    )
    artifact = InputReplay(timeline, tuple(InputSnapshot(tick) for tick in range(3601)))
    path.write_bytes(artifact.canonical_bytes())
    module = _module("play_input_replay")

    def forbidden(name: str) -> RenderDevice:
        pytest.fail("renderer constructed for oversized playback")

    monkeypatch.setattr(module, "_device", forbidden)
    with pytest.raises(SystemExit) as error:
        _main(module, [str(path)])
    assert error.value.code == 2


def test_second_pass_divergence_closes_without_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "second-pass.json"
    _record(path, 1)
    module = _module("play_input_replay")
    device = _Device()

    class DivergingService(TransactionService):
        def apply(self, transaction: CommandTransaction) -> TransactionReceipt:
            receipt = super().apply(transaction)
            return replace(receipt, post_hash="sha256:" + "0" * 64)

    monkeypatch.setattr(module, "TransactionService", DivergingService)
    monkeypatch.setattr(module, "_device", _provider(device))
    with pytest.raises(RuntimeError, match="visible playback diverged"):
        _main(module, [str(path)])
    assert device.closes == 1
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("mode", ["step_resume", "close", "resume", "zero", "pause_running"])
def test_controls_pause_step_repeat_resume_and_close_preserve_recorded_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    mode: str,
) -> None:
    path = tmp_path / "controlled.json"
    artifact = _record(path, 0 if mode == "zero" else 3)
    module = _module("play_input_replay")
    applied: list[int] = []
    observed: list[tuple[int, int, int]] = []
    clock = VirtualClock()

    class Service(TransactionService):
        def apply(self, transaction: CommandTransaction) -> TransactionReceipt:
            receipt = super().apply(transaction)
            applied.append(receipt.completed_ticks_after)
            return receipt

    class Device(_Device):
        def drain_surface_events(self, handle: SurfaceHandle) -> tuple[PlatformEvent, ...]:
            super().drain_surface_events(handle)
            observed.append((self.polls, len(applied), clock.now_ns()))
            assert self.polls < 20, "paused event loop did not consume the scheduled control"
            if mode == "close" and self.polls == 5:
                return (KeyEvent("ArrowRight", True), CloseEvent())
            if mode == "resume" and self.polls == 10:
                return (KeyEvent(" ", True),)
            if mode == "pause_running":
                if self.polls in (3, 4):
                    return (KeyEvent("Space", True),)
                if self.polls == 6:
                    return (KeyEvent("Space", False), KeyEvent("Space", True))
                if self.polls == 7:
                    return (KeyEvent("ArrowRight", True),)
            if mode == "step_resume":
                if self.polls in (3, 4):
                    return (KeyEvent("ArrowRight", True),)
                if self.polls == 5:
                    return (KeyEvent("ArrowRight", False), KeyEvent("ArrowRight", True))
                if self.polls == 6:
                    return (KeyEvent("Space", True),)
            return (KeyEvent("r", True), ResizeEvent(800, 600))

    device = Device()
    monkeypatch.setattr(module, "TransactionService", Service)
    monkeypatch.setattr(module, "_device", _provider(device))
    monkeypatch.setattr(module, "MonotonicClock", lambda: clock)
    arguments = [str(path), "--renderer", "wgpu", "--window", "--controls"]
    if mode != "pause_running":
        arguments.append("--paused")
    assert _main(module, arguments) == 0
    result = json.loads(capsys.readouterr().out)
    assert device.closes == 1
    assert result["verification"] == "pass"
    assert result["verified_state_hash"] == artifact.timeline.final_state_hash
    assert path.read_bytes() == artifact.canonical_bytes()
    if mode == "close":
        assert applied == []
        assert result["playback"] == "interrupted"
        assert result["arena"]["ticks"] == 0
    else:
        assert result["playback"] == "complete"
        assert result["arena"]["state_hash"] == artifact.timeline.final_state_hash
        assert applied == ([] if mode == "zero" else [1, 2, 3])
    if mode == "step_resume":
        assert [(poll, ticks) for poll, ticks, _ in observed] == [
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 1),
            (5, 1),
            (6, 2),
        ]
        # A held/repeated Right press did not step twice; resuming after steps
        # schedules a fresh deadline instead of catching up on paused time.
        assert clock.now_ns() - observed[-1][2] == 16_666_667
    if mode == "resume":
        assert all(ticks == 0 for poll, ticks, _ in observed if poll <= 10)
        assert clock.now_ns() - observed[9][2] == 50_000_000
    if mode == "pause_running":
        assert [(poll, ticks) for poll, ticks, _ in observed] == [
            (1, 0),
            (2, 0),
            (3, 1),
            (4, 1),
            (5, 1),
            (6, 1),
            (7, 2),
        ]
        assert clock.now_ns() - observed[5][2] == 33_333_334


@pytest.mark.parametrize("args", [["--controls"], ["--paused"]])
def test_control_flags_require_window_before_artifact_io(args: list[str]) -> None:
    with pytest.raises(SystemExit) as error:
        _main(_module("play_input_replay"), ["does-not-exist.json", *args])
    assert error.value.code == 2


def test_controls_refuse_multitick_batch_before_renderer(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "multi.json"
    artifact = _record(path, 2)
    first, last = artifact.timeline.batches
    grouped = replace(
        first,
        end_tick=2,
        post_hash=last.post_hash,
    )
    timeline = replace(
        artifact.timeline,
        batches=(grouped,),
        checkpoints=(
            artifact.timeline.checkpoints[0],
            replace(artifact.timeline.checkpoints[-1], after_batch=1),
        ),
    )
    path.write_bytes(replace(artifact, timeline=timeline).canonical_bytes())
    module = _module("play_input_replay")

    def forbidden(name: str) -> RenderDevice:
        pytest.fail("device created before single-tick admission")

    monkeypatch.setattr(module, "_device", forbidden)
    with pytest.raises(SystemExit) as error:
        _main(module, [str(path), "--renderer", "wgpu", "--window", "--controls"])
    assert error.value.code == 2


def test_paused_render_failure_closes_without_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "paused-failure.json"
    _record(path, 1)
    module = _module("play_input_replay")

    class Device(_Device):
        def poll(self) -> None:
            super().poll()
            if self.polls >= 2:
                raise RuntimeError("injected paused redraw failure")

    device = Device()
    monkeypatch.setattr(module, "_device", _provider(device))
    with pytest.raises(RuntimeError, match="paused redraw failure"):
        _main(module, [str(path), "--renderer", "wgpu", "--window", "--controls", "--paused"])
    assert device.closes == 1
    assert capsys.readouterr().out == ""
