# LudoWeave Engine

**Build worlds humans can play and agents can operate.**

LudoWeave is a pre-alpha, deterministic, headless-first Python engine for 2D and layered-2D worlds. M0 establishes the repository contract and a pure-Python lifecycle skeleton; it is not yet a game runtime.

## M0 capabilities

- Explicit engine initialization, fixed-tick run, shutdown, and close behavior.
- Monotonic real time and deterministic virtual time behind one protocol.
- A backend-neutral rendering boundary with a null validation backend.
- Structured errors, JSON diagnostics, and a headless example.
- Tested architecture rules and a pure-Python wheel.

Read the [architecture overview](architecture.md), [runtime contract](runtime-contract.md), and [accepted decisions](adr/index.md) before building on the experimental API.

## Quick check

```console
uv sync --frozen --all-groups
uv run ludoweave doctor
uv run python examples/hello_headless.py --ticks 120
```

Neither command needs a display, GPU, native compiler, or network listener.
