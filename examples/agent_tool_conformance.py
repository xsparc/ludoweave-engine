"""Run the installed agent-tool baseline against the explicit direct service."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from ludoweave.agent import (
    AgentCapture,
    AgentToolAdapter,
    run_agent_tool_conformance,
)
from ludoweave.samples import create_agent_world_builder


class _Capture:
    """Deterministic provider-neutral capture used only by this composition root."""

    __slots__ = ()

    def capture(self, width: int, height: int) -> AgentCapture:
        return AgentCapture(width, height, b"\x12\x34\x56\xff" * (width * height))

    def close(self) -> None:
        pass


def _factory() -> AgentToolAdapter:
    return create_agent_world_builder(write=True, capture_provider=_Capture()).service


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    report = run_agent_tool_conformance("org.ludoweave.agent-service", _factory)
    print(report.to_json(), end="")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
