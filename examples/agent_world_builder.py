"""Run the Agent World Builder acceptance loop with a real offscreen wgpu capture."""

from __future__ import annotations

import json
from collections.abc import Sequence

from ludoweave.render.backends.wgpu import WgpuRenderDevice
from ludoweave.samples import create_agent_world_builder, run_agent_world_builder_acceptance


def main(argv: Sequence[str] | None = None) -> int:
    if argv:
        raise SystemExit("agent_world_builder accepts no arguments")
    builder = create_agent_world_builder(write=True, device=WgpuRenderDevice())
    try:
        result = run_agent_world_builder_acceptance(builder.service)
    finally:
        builder.close()
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
