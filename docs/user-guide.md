# Community-alpha user guide

LudoWeave Engine builds deterministic, headless-first 2D worlds whose mutations
can be validated, receipted, replayed, and operated through the same typed
protocol. Version `0.1.0a1` is useful for evaluation and contribution; most
Python exports remain experimental and the M12 plugin contract is preview.

## Install and verify

Use a normal CPython 3.12, 3.13, or 3.14 environment on Windows, macOS, or
Linux. The baseline wheel has no dependencies and requires no compiler or GPU:

```console
python -m pip install ./ludoweave-0.1.0a1-py3-none-any.whl
ludoweave --version
ludoweave doctor
```

For a downloaded release candidate, verify its `SHA256SUMS` before installing.
For an official GitHub tag, also verify provenance with the GitHub CLI as shown
in the [release process](release-process.md). PyPI publication and name
reservation remain maintainer follow-ups until an official release says
otherwise.

## Run headlessly first

Download the version-matched `ludoweave-samples-0.1.0a1.zip`, extract it, and
run:

```console
python hello_headless.py --ticks 120
python fixed_step_world.py --ticks 6
python clockwork_arena.py --ticks 600
python rich_2d_showcase.py --ticks 6
python render_device_conformance.py
python alpha_acceptance.py
ludoweave plugin check example.plugin.json
```

Every command exits on its own and prints one JSON summary. The rich 2D
showcase exercises animation, bitmap text, tilemaps, particles, and Null-audio
mixing without a device. The alpha acceptance
spans engine lifecycle, generational entities, fixed world ticks, Clockwork
Arena, typed agent transactions, replay, tests, and owned capture cleanup.
The render-device profile produces deterministic installed evidence for the
explicit Null factory; it does not discover or certify executable providers.

The foundational application surface is deliberately small:

```python
from ludoweave import Engine, EngineConfig
from ludoweave.core import VirtualClock
from ludoweave.render import NullRenderBackend

clock = VirtualClock()
renderer = NullRenderBackend()
with Engine(EngineConfig(fixed_hz=60), renderer, clock=clock) as engine:
    summary = engine.run(ticks=10)

assert summary.ticks == 10
assert renderer.frame_count == 10
```

The engine owns and closes the injected renderer. The clock is borrowed.
Lifecycle calls are single-thread-owned. Virtual time and authoritative world
state are deterministic control inputs; frame timing and diagnostics are not.

## Build a canonical world

Use registered immutable components and `World` for local simulation. Use
`WorldSession` plus persistent transactions when work must be validated,
attributed, hashed, snapshotted, or replayed. Local `Commands` buffers are only
for trusted in-process deferred structural work and do not produce persistent
receipts.

Read the [ECS/world guide](ecs.md), [fixed-step application guide](fixed-step-application.md),
and [persistent command contract](commands.md) before choosing a layer. The
canonical state rule is simple: presentation objects, GPU handles, input
providers, clocks, paths, and audio handles never enter the authority image.

## Check plugin metadata without loading code

The sample bundle includes one inert `example.plugin.json`. Check it against
the current engine, CPython minor, and desktop platform:

```console
ludoweave plugin check example.plugin.json
```

The checker reads only the explicitly named bounded JSON file. It does not
discover installed packages, import a module, execute a hook, install a
dependency, contact a network, or compose runtime state. Exit 0 is compatible,
1 is valid but incompatible, and 2 is invalid input. Read the
[plugin guide](plugins.md) before relying on this preview format.

## Optional presentation

For this release candidate, install the exact optional packages and the
downloaded wheel. They are not required for any headless workflow:

```console
python -m pip install glfw==2.10.2 "rendercanvas[glfw]==2.7.2" wgpu==0.32.0
python hello_sprite.py
python clockwork_arena.py --ticks 600 --renderer wgpu
python render_device_conformance.py --backend wgpu
```

The locked adapter uses wgpu-py/rendercanvas/GLFW behind engine-owned
descriptors. Headless/offscreen use remains the reference acceptance path. A
windowed interactive run is:

```console
python clockwork_arena.py --ticks 36000 --renderer wgpu --window --interactive
```

Use WASD/arrows to move, the pointer and primary button to aim/fire, and R to
restart. Provider/native objects are not public API and must not be saved in
world state. The [conformance guide](render-device-conformance.md) explains
what the baseline does and does not prove.

## Typed local agent control

The [agent control guide](agent-control.md) documents all 12 tools. Read calls
are available by default; mutation requires the composition root's explicit
write capability. MCP is local stdio only:

```console
ludoweave mcp --sample agent-world-builder
ludoweave mcp --sample agent-world-builder --write
```

There is no HTTP listener, remote authentication claim, arbitrary Python
evaluation, shell tool, or dynamic project-module loader.

## Failure and compatibility expectations

Expected engine failures are structured `LudoWeaveError` subclasses with stable
codes and bounded context. A rejected transaction preserves its pre-hash and
returns a rejected receipt. Resource-owning objects provide explicit close
semantics and should be used as context managers where supported.

Most exports are experimental; `ludoweave.plugins` is preview under RFC-0002.
Inspect a package's `__all__` and `__stability__`, then read the
[API status](api-status.md). Persistent protocol revision and Python symbol
stability are separate contracts.

If installation, doctor, headless samples, or a recorded replay fails, file a
bug using the repository form with the exact version, OS, CPython version,
command, sanitized output, and smallest reproduction. Report vulnerabilities
privately under the repository's `SECURITY.md` policy.
