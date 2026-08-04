# LudoWeave Engine

**Build worlds humans can play and agents can operate.**

LudoWeave is a pre-alpha, deterministic, headless-first Python engine for 2D and layered-2D worlds. M0 established the repository contract and lifecycle skeleton. M1 now includes entity identity, component schemas, canonical world storage, typed queries, local deferred structural commands, typed resources, serial schedule planning, immutable input, and fixed-step application execution, but this is not yet a complete game runtime.

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

Read the [architecture overview](architecture.md), [runtime contract](runtime-contract.md), [entity identity contract](ecs.md), and [accepted decisions](adr/index.md) before building on the experimental API.

## Quick check

```console
uv sync --frozen --all-groups
uv run ludoweave doctor
uv run python examples/hello_headless.py --ticks 120
```

Neither command needs a display, GPU, native compiler, or network listener.
