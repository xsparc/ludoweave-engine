"""Run one dependency-free acceptance summary spanning the alpha milestones."""

from __future__ import annotations

import json
from collections.abc import Sequence

from ludoweave import Engine, EngineConfig, LifecycleState, __version__
from ludoweave.agent import AgentCapture
from ludoweave.core.clock import VirtualClock
from ludoweave.ecs import EntityAllocator
from ludoweave.render import NullRenderBackend
from ludoweave.samples import (
    clockwork_input,
    create_agent_world_builder,
    create_clockwork_arena,
    run_agent_world_builder_acceptance,
)


class _Capture:
    """Provider-neutral deterministic capture used by the baseline bundle."""

    __slots__ = ("closed",)

    def __init__(self) -> None:
        self.closed = False

    def capture(self, width: int, height: int) -> AgentCapture:
        return AgentCapture(width, height, b"\x10\x20\x30\xff" * (width * height))

    def close(self) -> None:
        self.closed = True


def main(argv: Sequence[str] | None = None) -> int:
    if argv:
        raise SystemExit("alpha_acceptance accepts no arguments")

    clock = VirtualClock()
    backend = NullRenderBackend()
    engine_ticks = 0
    with Engine(EngineConfig(), backend, clock=clock) as engine:
        engine_ticks = engine.run(ticks=4).ticks
    if engine.state is not LifecycleState.CLOSED:
        raise AssertionError("engine acceptance did not close")

    allocator = EntityAllocator()
    stale = allocator.create()
    allocator.destroy(stale)
    current = allocator.create()
    if current.index != stale.index or current.generation != stale.generation + 1:
        raise AssertionError("entity generation acceptance failed")

    arena = create_clockwork_arena(clockwork_input(120))
    arena_summary = arena.run(120)

    capture = _Capture()
    builder = create_agent_world_builder(write=True, capture_provider=capture)
    try:
        builder_summary = run_agent_world_builder_acceptance(builder.service)
    finally:
        builder.close()
    if not capture.closed:
        raise AssertionError("owned agent capture provider did not close")

    result: dict[str, object] = {
        "protocol": "ludoweave.sample.alpha_acceptance/1",
        "status": "ok",
        "ludoweave_version": __version__,
        "engine_ticks": engine_ticks,
        "engine_frames": backend.frame_count,
        "entity_generation": current.generation,
        "arena_ticks": arena_summary.ticks,
        "arena_state_hash": arena_summary.state_hash,
        "agent_ticks": _integer(builder_summary["ticks"], "ticks"),
        "agent_replay_batches": _integer(builder_summary["replay_batches"], "replay_batches"),
        "agent_tests_passed": _boolean(builder_summary["tests_passed"], "tests_passed"),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


def _integer(value: object, field: str) -> int:
    if type(value) is not int:
        raise AssertionError(f"agent builder {field} is not an integer")
    return value


def _boolean(value: object, field: str) -> bool:
    if type(value) is not bool:
        raise AssertionError(f"agent builder {field} is not a boolean")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
