"""Run the installed WorldStore baseline against an explicit built-in adapter."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence

from ludoweave.ecs import (
    ComponentRegistry,
    ReferenceWorld,
    World,
    WorldStore,
    run_world_store_conformance,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=("world", "reference"), default="world")
    args = parser.parse_args(argv)
    backend = str(args.backend)
    factory: Callable[[ComponentRegistry], WorldStore] = (
        World if backend == "world" else ReferenceWorld
    )

    report = run_world_store_conformance(f"ludoweave.{backend}", factory)
    print(report.to_json(), end="")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
