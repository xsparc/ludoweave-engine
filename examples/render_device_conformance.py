"""Run the installed render-device baseline against an explicit adapter."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence

from ludoweave.render import (
    NullRenderDevice,
    RenderDevice,
    run_render_device_conformance,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=("null", "wgpu"), default="null")
    args = parser.parse_args(argv)
    backend = str(args.backend)
    factory: Callable[[], RenderDevice]
    if backend == "null":
        factory = NullRenderDevice
    else:
        from ludoweave.render.backends.wgpu import WgpuRenderDevice

        factory = WgpuRenderDevice

    report = run_render_device_conformance(f"org.ludoweave.{backend}", factory)
    print(report.to_json(), end="")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
