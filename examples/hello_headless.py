"""Run the M0 engine for deterministic virtual ticks with no display."""

import argparse
import json
from collections.abc import Sequence

from ludoweave import Engine, EngineConfig, LifecycleState, __version__
from ludoweave.app import RunSummary
from ludoweave.core.clock import VirtualClock
from ludoweave.render import NullRenderBackend, RenderDescriptor


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticks", type=int, default=120, help="non-negative virtual tick count")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    ticks: object = getattr(args, "ticks", None)
    if isinstance(ticks, bool) or not isinstance(ticks, int) or ticks < 0:
        _build_parser().error("--ticks must be a non-negative integer")

    clock = VirtualClock()
    backend = NullRenderBackend()
    engine = Engine(
        EngineConfig(fixed_hz=60),
        backend,
        clock=clock,
        descriptor=RenderDescriptor(label="hello_headless"),
    )
    summary: RunSummary | None = None
    with engine:
        summary = engine.run(ticks=ticks)
    assert summary is not None

    payload: dict[str, object] = {
        "schema": "ludoweave.example.headless/1",
        "ludoweave_version": __version__,
        "ticks": summary.ticks,
        "frames": summary.frames,
        "fixed_hz": summary.fixed_hz,
        "elapsed_ns": summary.elapsed_ns,
        "renderer": summary.renderer,
        "final_state": engine.state.value,
    }
    assert engine.state is LifecycleState.CLOSED
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
