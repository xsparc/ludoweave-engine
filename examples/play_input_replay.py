"""Verify a Clockwork Arena recording, then display its recorded world transactions."""

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from ludoweave.app import RecordedInputSource
from ludoweave.app.replay import InputReplay
from ludoweave.core.clock import MonotonicClock
from ludoweave.platform import CloseEvent, KeyEvent, ResizeEvent
from ludoweave.render import (
    NullRenderDevice,
    PipelineDescriptor,
    RenderDevice,
    RenderExtractor,
    SurfaceDescriptor,
    SurfaceHandle,
    SurfaceKind,
    TextureData,
    TextureDescriptor,
    TextureFormat,
    TextureUsage,
)
from ludoweave.samples import create_clockwork_arena
from ludoweave.samples.clockwork_arena import (
    ARENA_LOCK_HASH,
    ARENA_PLATFORM_PROFILE,
    ARENA_PROJECT_SCHEMA,
    ArenaTickExecutor,
    ClockworkArena,
)
from ludoweave.world import ReceiptStatus, ReplayRunner, TransactionService


def _device(name: str) -> RenderDevice:
    if name == "null":
        return NullRenderDevice()
    from ludoweave.render.backends.wgpu import WgpuRenderDevice

    return WgpuRenderDevice()


class _PlaybackControls:
    """Presentation-only key edges; never an input source for the world."""

    __slots__ = ("held", "paused", "rebase", "step")

    def __init__(self, *, paused: bool) -> None:
        self.paused = paused
        self.step = False
        self.rebase = False
        self.held: set[str] = set()

    def key(self, event: KeyEvent) -> None:
        key = event.key.lower()
        if key == " ":
            key = "space"
        if key not in ("space", "arrowright"):
            return
        if not event.pressed:
            self.held.discard(key)
            return
        if key in self.held:
            return
        self.held.add(key)
        if key == "space":
            self.paused = not self.paused
            self.step = False
            self.rebase = True
        elif self.paused:
            self.step = True


def _events(
    device: RenderDevice, surface: SurfaceHandle, controls: _PlaybackControls | None = None
) -> bool:
    """Only presentation management is live; recorded inputs remain authoritative."""
    closed = False
    for event in device.drain_surface_events(surface):
        if type(event) is CloseEvent:
            closed = True
        elif type(event) is ResizeEvent:
            device.resize_surface(surface, event.width, event.height)
        elif type(event) is KeyEvent and controls is not None:
            controls.key(event)
    return closed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--renderer", choices=("null", "wgpu"), default="null")
    parser.add_argument("--window", action="store_true", help="display at recorded 60-Hz tick pace")
    parser.add_argument(
        "--controls", action="store_true", help="Space: pause/resume; Right: one paused tick"
    )
    parser.add_argument("--paused", action="store_true", help="start controlled playback paused")
    args = parser.parse_args(argv)
    if args.window and args.renderer != "wgpu":
        parser.error("--window requires --renderer wgpu")
    if args.controls and not args.window:
        parser.error("--controls requires --window")
    if args.paused and not args.controls:
        parser.error("--paused requires --controls")
    with Path(args.artifact).open("rb") as source:
        artifact = InputReplay.from_json(source.read(67_108_865))
    timeline = artifact.timeline
    if len(timeline.batches) > 3600 or len(artifact.snapshots) > 3600:
        parser.error("visible playback supports at most 3600 batches and ticks")
    if args.controls and any(batch.end_tick != batch.start_tick + 1 for batch in timeline.batches):
        parser.error("controlled playback requires exactly one tick per recorded batch")
    controls = _PlaybackControls(paused=bool(args.paused)) if args.controls else None

    composition = create_clockwork_arena(RecordedInputSource())
    runner = ReplayRunner(
        composition.codec,
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )
    # Complete verification precedes optional provider construction. No unverified
    # recording is shown, and no renderer participates in the authoritative pass.
    verified = artifact.replay(runner, ArenaTickExecutor)
    kernel = ArenaTickExecutor(artifact)
    initial = runner.replay(timeline, tick_executor=kernel, max_batches=0)
    arena = ClockworkArena(initial.session, composition.codec, kernel)
    service = TransactionService(arena.session)
    checkpoints = {item.after_batch: item for item in timeline.checkpoints}
    frames = 0
    completed = 0
    interrupted = False
    device = _device(args.renderer)
    try:
        surface = device.create_surface(
            SurfaceDescriptor(
                960,
                540,
                TextureFormat.RGBA8_UNORM,
                SurfaceKind.WINDOW if args.window else SurfaceKind.OFFSCREEN,
                "LudoWeave recorded Clockwork Arena",
            )
        )
        texture = device.create_texture(
            TextureDescriptor(
                1,
                1,
                TextureFormat.RGBA8_UNORM,
                TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
                label="replay-white",
            ),
            TextureData(b"\xff\xff\xff\xff", 4),
        )
        pipeline = device.create_pipeline(PipelineDescriptor(TextureFormat.RGBA8_UNORM))
        extractor = RenderExtractor()
        clock = MonotonicClock()
        start = clock.now_ns()

        def draw() -> None:
            nonlocal frames
            commands = extractor.build_command_list(
                arena.presentation(texture),
                target=surface,
                pipeline=pipeline,
                label=f"replay-frame-{frames}",
            )
            device.submit((commands,))
            device.poll()
            frames += 1

        interrupted = bool(args.window and _events(device, surface, controls))
        if not interrupted:
            draw()
        for batch in timeline.batches:
            if interrupted or (args.window and _events(device, surface, controls)):
                interrupted = True
                break
            if controls is not None:
                while controls.paused and not controls.step:
                    # Keep the window responsive without advancing canonical time
                    # or busy-spinning. Redraw permits resize while paused.
                    draw()
                    clock.wait_until_ns(clock.now_ns() + 1_000_000_000 // 60)
                    if _events(device, surface, controls):
                        interrupted = True
                        break
                if interrupted:
                    break
                if controls.rebase:
                    start = (
                        clock.now_ns()
                        - (batch.start_tick - timeline.header.initial_tick) * 1_000_000_000 // 60
                    )
                    controls.rebase = False
                controls.step = False
            receipt = service.apply(batch.transaction)
            if (
                receipt.status is not ReceiptStatus.COMMITTED
                or receipt.completed_ticks_before != batch.start_tick
                or receipt.completed_ticks_after != batch.end_tick
                or receipt.pre_hash != batch.pre_hash
                or receipt.post_hash != batch.post_hash
            ):
                raise RuntimeError("visible playback diverged from verified recording")
            completed += 1
            checkpoint = checkpoints.get(completed)
            if checkpoint is not None and (
                checkpoint.tick != arena.session.completed_ticks
                or checkpoint.state_hash != arena.session.state_hash
            ):
                raise RuntimeError("visible playback checkpoint diverged")
            if args.window and (controls is None or not controls.paused):
                clock.wait_until_ns(
                    start + (batch.end_tick - timeline.header.initial_tick) * 1_000_000_000 // 60
                )
            draw()
        if not interrupted and arena.session.state_hash != verified.session.state_hash:
            raise RuntimeError("visible playback final state diverged")
    finally:
        device.close()
    print(
        json.dumps(
            {
                "schema": "ludoweave.input-replay-playback/1",
                "verification": "pass",
                "playback": "interrupted" if interrupted else "complete",
                "artifact_hash": artifact.artifact_hash(),
                "verified_state_hash": verified.session.state_hash,
                "verified_checkpoints": len(verified.verified_checkpoints),
                "played_batches": completed,
                "frames": frames,
                "arena": arena.summary().as_dict(),
                "renderer": args.renderer,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
