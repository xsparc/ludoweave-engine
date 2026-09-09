"""Record or verify Clockwork Arena with replay-owned inputs, without a device."""

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from ludoweave.app import RecordedInputSource
from ludoweave.app.replay import InputReplay
from ludoweave.samples import clockwork_input, create_clockwork_arena
from ludoweave.samples.clockwork_arena import (
    ARENA_LOCK_HASH,
    ARENA_PLATFORM_PROFILE,
    ARENA_PROJECT_SCHEMA,
    ArenaTickExecutor,
    arena_tick_transaction,
)
from ludoweave.world import ReceiptStatus, ReplayRecorder, ReplayRunner


def record(ticks: int) -> InputReplay:
    """Record a bounded sample; input generation is used only during recording."""

    if type(ticks) is not int or not 0 <= ticks <= 3600:
        raise ValueError("ticks must be between 0 and 3600")
    source = clockwork_input(ticks)
    snapshots = tuple(source.snapshot_for_tick(tick) for tick in range(ticks))
    arena = create_clockwork_arena(RecordedInputSource(snapshots))
    recorder = ReplayRecorder(
        arena.session,
        arena.codec,
        timeline_id="clockwork-owned-input",
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )
    for _ in range(ticks):
        receipt = recorder.record(arena_tick_transaction(recorder.session))
        if receipt.status is not ReceiptStatus.COMMITTED:
            raise RuntimeError("sample recording transaction was rejected")
    return InputReplay(recorder.timeline(), snapshots)


def verify(artifact: InputReplay) -> dict[str, str | int]:
    """Replay from embedded inputs with an otherwise empty composition source."""

    arena = create_clockwork_arena(RecordedInputSource())
    runner = ReplayRunner(
        arena.codec,
        project_schema=ARENA_PROJECT_SCHEMA,
        dependency_lock_hash=ARENA_LOCK_HASH,
        platform_profile=ARENA_PLATFORM_PROFILE,
    )
    result = artifact.replay(runner, ArenaTickExecutor)
    return {
        "schema": "ludoweave.input-replay-example/1",
        "status": "pass",
        "ticks": result.session.completed_ticks,
        "state_hash": result.session.state_hash,
        "artifact_hash": artifact.artifact_hash(),
        "checkpoints": len(result.verified_checkpoints),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    recording = commands.add_parser("record")
    recording.add_argument("artifact", type=Path)
    recording.add_argument("--ticks", type=int, default=120)
    playback = commands.add_parser("replay")
    playback.add_argument("artifact", type=Path)
    args = parser.parse_args(argv)
    path = Path(args.artifact)
    if args.command == "record":
        if not 0 <= args.ticks <= 3600:
            parser.error("ticks must be between 0 and 3600")
        artifact = record(args.ticks)
        # Refuse accidental replacement of an existing recording.
        with path.open("xb") as output:
            output.write(artifact.canonical_bytes())
    else:
        with path.open("rb") as source:
            artifact = InputReplay.from_json(source.read(67_108_865))
    print(json.dumps(verify(artifact), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
