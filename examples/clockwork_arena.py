"""Run Clockwork Arena headlessly or render it through the optional wgpu adapter."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from ludoweave import __version__
from ludoweave.app import ActionBinding, ActionMap, InputSnapshot, InputSource, MappedInputSource
from ludoweave.app.replay import InputReplay
from ludoweave.audio import AudioBackend, AudioClipDescriptor, AudioClipHandle, NullAudioBackend
from ludoweave.audio.sounddevice import BlockingAudioBackend
from ludoweave.platform import (
    CloseEvent,
    FocusEvent,
    InputEvent,
    KeyEvent,
    MouseButtonEvent,
    PointerEvent,
    ResizeEvent,
)
from ludoweave.render import (
    NullRenderDevice,
    PipelineDescriptor,
    RenderDevice,
    RenderExtractor,
    SurfaceDescriptor,
    SurfaceKind,
    TextureData,
    TextureDescriptor,
    TextureFormat,
    TextureUsage,
)
from ludoweave.samples import clockwork_input, create_clockwork_arena
from ludoweave.samples.clockwork_arena import (
    ARENA_LOCK_HASH,
    ARENA_PLATFORM_PROFILE,
    ARENA_PROJECT_SCHEMA,
    ARENA_STATE,
    ClockworkArena,
    arena_tick_transaction,
)
from ludoweave.world import (
    ReceiptStatus,
    ReplayBatch,
    ReplayCheckpoint,
    ReplayRecorder,
    ReplayTimeline,
    TransactionService,
)


class _CapturedInput:
    """Capture the exact snapshot consumed once per successful play-loop tick."""

    __slots__ = ("_source", "snapshots")

    def __init__(self, source: InputSource) -> None:
        self._source = source
        self.snapshots: list[InputSnapshot] = []

    def snapshot_for_tick(self, tick: int) -> InputSnapshot:
        if tick != len(self.snapshots) or tick >= 3600:
            raise ValueError("play recording requires sequential ticks below 3600")
        snapshot = self._source.snapshot_for_tick(tick)
        self.snapshots.append(snapshot)
        return snapshot


class _PlayRecorder:
    """Buffer bounded committed batches; validate the complete history at save time."""

    __slots__ = ("_batches", "_checkpoints", "_initial", "_service")

    def __init__(self, arena: ClockworkArena) -> None:
        self._initial = ReplayRecorder(
            arena.session,
            arena.codec,
            timeline_id="clockwork-play-session",
            project_schema=ARENA_PROJECT_SCHEMA,
            dependency_lock_hash=ARENA_LOCK_HASH,
            platform_profile=ARENA_PLATFORM_PROFILE,
        ).timeline()
        self._service = TransactionService(arena.session)
        self._batches: list[ReplayBatch] = []
        self._checkpoints = list(self._initial.checkpoints)

    def record_tick(self) -> None:
        if len(self._batches) >= 3600:
            raise ValueError("play recording supports at most 3600 ticks")
        transaction = arena_tick_transaction(self._service.session)
        receipt = self._service.apply(transaction)
        if receipt.status is not ReceiptStatus.COMMITTED:
            raise RuntimeError("play recording transaction was rejected")
        self._batches.append(
            ReplayBatch(
                len(self._batches),
                receipt.completed_ticks_before,
                receipt.completed_ticks_after,
                receipt.pre_hash,
                receipt.post_hash,
                transaction,
            )
        )
        self._checkpoints.append(
            ReplayCheckpoint(len(self._batches), receipt.completed_ticks_after, receipt.post_hash)
        )

    def finish(self, snapshots: tuple[InputSnapshot, ...]) -> InputReplay:
        timeline = ReplayTimeline(
            self._initial.header,
            self._initial.initial_snapshot,
            tuple(self._batches),
            tuple(self._checkpoints),
        )
        return InputReplay(timeline, snapshots)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticks", type=int, default=600)
    parser.add_argument("--stress", type=int, default=1)
    parser.add_argument("--renderer", choices=("null", "wgpu"), default="null")
    parser.add_argument(
        "--audio",
        choices=("null", "device"),
        default="null",
        help="device enables audible, blocking 60-Hz presentation pacing",
    )
    parser.add_argument("--window", action="store_true")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="use WASD/arrows, mouse aim/fire, and R to restart in a wgpu window",
    )
    parser.add_argument("--render-every", type=int, default=1)
    parser.add_argument("--record", type=Path, help="save consumed inputs; refuses existing files")
    return parser


def _device(name: str) -> RenderDevice:
    if name == "null":
        return NullRenderDevice()
    from ludoweave.render.backends.wgpu import WgpuRenderDevice

    return WgpuRenderDevice()


def _sound_clips(audio: AudioBackend) -> dict[str, AudioClipHandle]:
    clips: dict[str, AudioClipHandle] = {}
    for name, frequency in (
        ("shots_fired", 880),
        ("enemies_destroyed", 440),
        ("damage_taken", 220),
    ):
        # Original synthesized assets: a short, quiet tone with a click-free envelope.
        samples = 2205
        pcm = b"".join(
            struct.pack(
                "<h",
                round(
                    3000
                    * math.sin(2 * math.pi * frequency * index / 44100)
                    * math.sin(math.pi * index / (samples - 1)) ** 2
                ),
            )
            for index in range(samples)
        )
        clips[name] = audio.load_clip(AudioClipDescriptor(name, 0.05), pcm)
    return clips


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.ticks < 0:
        _parser().error("--ticks must be non-negative")
    if not 1 <= arguments.stress <= 16:
        _parser().error("--stress must be between 1 and 16")
    if arguments.render_every <= 0:
        _parser().error("--render-every must be positive")
    if arguments.window and arguments.renderer != "wgpu":
        _parser().error("--window requires --renderer wgpu")
    if arguments.interactive and not arguments.window:
        _parser().error("--interactive requires --window")
    recording_path = None if arguments.record is None else Path(arguments.record)
    if recording_path is not None:
        if arguments.ticks > 3600:
            _parser().error("--record supports at most 3600 ticks")
        if recording_path.exists() or recording_path.is_symlink():
            _parser().error("--record destination already exists")

    mapped = MappedInputSource(
        ActionMap(
            (
                ActionBinding("move.x", "key:a", -1.0),
                ActionBinding("move.x", "key:arrowleft", -1.0),
                ActionBinding("move.x", "key:d", 1.0),
                ActionBinding("move.x", "key:arrowright", 1.0),
                ActionBinding("move.y", "key:s", -1.0),
                ActionBinding("move.y", "key:arrowdown", -1.0),
                ActionBinding("move.y", "key:w", 1.0),
                ActionBinding("move.y", "key:arrowup", 1.0),
                ActionBinding("fire", "mouse:primary"),
                ActionBinding("restart", "key:r"),
                ActionBinding("move.x", "gamepad:0:axis:left_x", 1.0, 0.15),
                ActionBinding("move.y", "gamepad:0:axis:left_y", -1.0, 0.15),
                ActionBinding("aim.x", "gamepad:0:axis:right_x", 1.0, 0.15),
                ActionBinding("aim.y", "gamepad:0:axis:right_y", -1.0, 0.15),
                ActionBinding("fire", "gamepad:0:button:a"),
                ActionBinding("restart", "gamepad:0:button:start"),
            )
        )
    )
    input_source: InputSource = (
        mapped if arguments.interactive else clockwork_input(arguments.ticks)
    )
    captured = None if recording_path is None else _CapturedInput(input_source)
    arena = create_clockwork_arena(
        input_source if captured is None else captured, stress=arguments.stress
    )
    recorder = None if captured is None else _PlayRecorder(arena)
    device = _device(arguments.renderer)
    audio: AudioBackend = (
        BlockingAudioBackend() if arguments.audio == "device" else NullAudioBackend()
    )
    draw_calls = 0
    sprite_instances = 0
    capture_hash: str | None = None
    kind = SurfaceKind.WINDOW if arguments.window else SurfaceKind.OFFSCREEN
    try:
        audio.initialize()
        clips = _sound_clips(audio)
        previous_audio = arena.session.resources.require(ARENA_STATE)
        surface = device.create_surface(
            SurfaceDescriptor(
                960,
                540,
                TextureFormat.RGBA8_UNORM,
                kind,
                "LudoWeave Clockwork Arena",
            )
        )
        texture = device.create_texture(
            TextureDescriptor(
                1,
                1,
                TextureFormat.RGBA8_UNORM,
                TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
                label="clockwork-white",
            ),
            TextureData(b"\xff\xff\xff\xff", 4),
        )
        pipeline = device.create_pipeline(PipelineDescriptor(TextureFormat.RGBA8_UNORM))
        extractor = RenderExtractor()
        for index in range(arguments.ticks):
            should_close = False
            if arguments.interactive:
                for event in device.drain_surface_events(surface):
                    if type(event) in (KeyEvent, MouseButtonEvent, PointerEvent, FocusEvent):
                        mapped.feed(cast(InputEvent, event))
                    elif type(event) is ResizeEvent:
                        device.resize_surface(surface, event.width, event.height)
                    elif type(event) is CloseEvent:
                        should_close = True
                for event in device.poll_gamepads():
                    mapped.feed(event)
                if should_close:
                    break
            if recorder is None:
                arena.tick()
            else:
                recorder.record_tick()
            current_audio = arena.session.resources.require(ARENA_STATE)
            for counter, clip in clips.items():
                if cast(int, getattr(current_audio, counter)) > cast(
                    int, getattr(previous_audio, counter)
                ):
                    playback = audio.play(clip)
                    if isinstance(audio, NullAudioBackend):
                        audio.stop(playback)
            previous_audio = current_audio
            if isinstance(audio, BlockingAudioBackend):
                audio.pump()
            if (index + 1) % arguments.render_every != 0 and index + 1 != arguments.ticks:
                continue
            frame = arena.presentation(texture)
            command_list = extractor.build_command_list(
                frame,
                target=surface,
                pipeline=pipeline,
                label=f"clockwork-frame-{index + 1}",
            )
            submission = device.submit((command_list,))
            draw_calls += submission.draw_calls
            sprite_instances += submission.sprite_instances
            device.poll()
        if arguments.renderer == "wgpu" and kind is SurfaceKind.OFFSCREEN:
            capture = device.capture_surface(surface)
            capture_hash = hashlib.sha256(capture.pixels).hexdigest()
    finally:
        try:
            audio.close()
        finally:
            device.close()

    if recording_path is not None and captured is not None and recorder is not None:
        artifact = recorder.finish(tuple(captured.snapshots))
        encoded = artifact.canonical_bytes()
        # Publish only after a successful loop and resource close. Exclusive creation
        # also refuses a destination created after the initial admission check.
        with recording_path.open("xb") as output:
            output.write(encoded)

    payload = {
        "arena": arena.summary().as_dict(),
        "capture_sha256": capture_hash,
        "draw_calls": draw_calls,
        "ludoweave_version": __version__,
        "renderer": arguments.renderer,
        "schema": "ludoweave.example.clockwork_arena/1",
        "sprite_instances": sprite_instances,
        "surface": kind.value,
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
