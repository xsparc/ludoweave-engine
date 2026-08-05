# API status

The normative compatibility policy is
[`API_COMPATIBILITY.md`](https://github.com/xsparc/ludoweave-engine/blob/main/API_COMPATIBILITY.md). LudoWeave defines official
Python exports through `__all__`; the adjacent `__stability__` mapping gives
every exported symbol its status.

The `0.1.0a1` surfaces are:

| Module | Role | Status |
| --- | --- | --- |
| `ludoweave` | Deliberately small engine root | Experimental |
| `ludoweave.core` | Clock/error contracts | Experimental |
| `ludoweave.ecs` | Entity, component, query, resource, schedule, and world contracts | Experimental |
| `ludoweave.app` | Lifecycle, fixed-step application, and input contracts | Experimental |
| `ludoweave.world` | Persistent commands, receipts, snapshots, replay, and authority | Experimental |
| `ludoweave.render` | Backend-neutral 2D rendering contracts and installed conformance evidence | Experimental |
| `ludoweave.render.backends` | Null validation adapters | Experimental |
| `ludoweave.render.backends.wgpu` | Optional concrete WebGPU device entry point | Experimental |
| `ludoweave.platform` | Provider-neutral events and gamepad-provider protocol | Experimental |
| `ludoweave.assets` | Project-confined asset contracts | Experimental |
| `ludoweave.audio` | Audio protocol, mix graph, and Null adapter | Experimental |
| `ludoweave.collision` | Deterministic bounded collision | Experimental |
| `ludoweave.presentation` | Tick animation, bitmap text, tilemap, particle, and extraction contracts | Experimental |
| `ludoweave.plugins` | Data-only plugin manifests and compatibility evaluation | Preview |
| `ludoweave.agent` | Typed agent-control service | Experimental |
| `ludoweave.samples` | Exercised reference compositions | Experimental |

Names from `ludoweave.tools` are composition-root internals unless a future
decision exports them. CLI commands and persistent protocols have separately
documented versioned contracts; a Python stability label does not override a
wire-format revision.

Inspect metadata directly when evaluating an alpha dependency:

```python
import ludoweave.ecs as ecs

assert set(ecs.__all__) == set(ecs.__stability__)
assert ecs.__stability__["World"] == "experimental"

import ludoweave.plugins as plugins

assert plugins.__stability__["PluginManifest"] == "preview"
```
