# LudoWeave Engine

**Build worlds humans can play and agents can operate.**

LudoWeave is an experimental, deterministic, headless-first Python engine for 2D and layered-2D games. It is being designed so human-facing tools, tests, replay, and software agents can eventually operate the same canonical world through typed, validated commands.

> Project status: pre-alpha walking skeleton. APIs are experimental and may change without deprecation.

## What exists in M0

- A typed engine lifecycle with explicit ownership and close semantics.
- Monotonic and deterministic virtual clocks.
- An engine-owned rendering protocol and validation-only null renderer.
- A headless fixed-tick example.
- `ludoweave --version` and a structured `ludoweave doctor` command.
- Architecture rules, ADRs, tests, documentation, packaging, and cross-platform CI.

Canonical ECS state, commands and receipts, WebGPU rendering, physics, audio, networking, MCP, and editor tooling are deliberately not part of M0.

## Requirements

- CPython 3.12, 3.13, or 3.14 (standard GIL builds are the baseline)
- Windows, macOS, or Linux
- [uv](https://docs.astral.sh/uv/) 0.11.x for contributor workflows

No native compiler or GPU is required.

## Quick start

```console
uv sync --frozen --all-groups
uv run ludoweave --version
uv run ludoweave doctor
uv run python examples/hello_headless.py --ticks 120
```

The example prints one JSON summary and uses virtual time plus the null renderer, so it does not open a window or wait in real time.

## Public API

The root package intentionally exposes only the initial application surface:

```python
from ludoweave import Engine, EngineConfig, LifecycleState, __version__
from ludoweave.core.clock import VirtualClock
from ludoweave.render import NullRenderBackend, RenderDescriptor

clock = VirtualClock()
backend = NullRenderBackend()

with Engine(EngineConfig(), backend, clock=clock) as engine:
    summary = engine.run(ticks=10)
```

See the [architecture overview](docs/architecture.md) and [runtime contract](docs/runtime-contract.md) before depending on these experimental APIs.

## Quality commands

```console
uv lock --check
uv sync --frozen --all-groups
uv run --frozen ruff format --check .
uv run --frozen ruff check .
uv run --frozen pyright
uv run --frozen pytest -q
uv run --frozen mkdocs build --strict
uv build
uv run --frozen python scripts/smoke_wheel.py dist
git diff --check
```

Passing status is recorded only after commands have actually run; see [test evidence](.ai/TEST_EVIDENCE.md).

## Contributing and project policy

Contributions use the [Developer Certificate of Origin](CONTRIBUTING.md), not a CLA. Please also read the [code of conduct](CODE_OF_CONDUCT.md), [security policy](SECURITY.md), [governance model](GOVERNANCE.md), and repository guidance in [AGENTS.md](AGENTS.md).

LudoWeave Engine is licensed under the [Apache License 2.0](LICENSE).
