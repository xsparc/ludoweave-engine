# LudoWeave Engine

**Build worlds humans can play and agents can operate.**

LudoWeave is a pre-alpha, deterministic, headless-first Python engine for 2D and layered-2D worlds. M0 established the repository contract and lifecycle skeleton. M1 added the deterministic world/application core. M2 added typed persistent commands, atomic transactions and receipts, canonical authority snapshots and hashes, deterministic random streams, verified replay/checkpoints, immutable branches, and a data-only headless CLI workflow. M3 adds isolated Null and wgpu 2D rendering. This is not yet a complete game runtime.

## Current capabilities

- Explicit engine initialization, fixed-tick run, shutdown, and close behavior.
- Monotonic real time and deterministic virtual time behind one protocol.
- A backend-neutral rendering boundary with a null validation backend.
- Structured errors, JSON diagnostics, and a headless example.
- Tested architecture rules and a pure-Python wheel.
- Deterministic generational entity allocation with checked stale-handle failures.
- Explicit immutable component schemas and forward migration paths without global registration.
- Canonical dense/sparse world storage checked against an independent dictionary model.
- Storage-neutral queries with stable-order, changed-epoch, and explicit writeback contracts.
- Atomic local command buffers whose deferred entity tokens are exact buffer identities.
- Copy-owned typed resource singletons and input-order-independent conflict-aware schedule planning.
- Exact fixed-step application pumping with immutable input and declaration-enforcing system contexts.
- Canonical versioned commands, atomic staged application, semantic diffs, and machine receipts.
- Complete snapshots and engine-owned deterministic named random streams.
- Self-contained verified replay/checkpoint files and immutable parent-referenced branches.
- Project-confined `apply`, `snapshot`, `replay`, and `diff` command workflows.
- Backend-neutral render resources, immutable extraction, explicit render graphs, and deferred generational-handle destruction.
- An optional wgpu/rendercanvas/GLFW adapter with instanced atlas sprites, tiles, orthographic cameras, debug fixtures, resize, and offscreen capture.

Read the [architecture overview](architecture.md), [runtime contract](runtime-contract.md), [entity identity contract](ecs.md), [headless command workflow](cli-workflows.md), [rendering contract](rendering.md), and [accepted decisions](adr/index.md) before building on the experimental API.

## Quick check

```console
uv sync --frozen --all-groups
uv run ludoweave doctor
uv run python examples/hello_headless.py --ticks 120
```

Neither command needs a display, GPU, native compiler, or network listener.

The optional GPU slice has a separate locked install and smoke:

```console
uv sync --frozen --all-groups --extra graphics
uv run --frozen --extra graphics python examples/hello_sprite.py
```
