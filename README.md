# LudoWeave Engine

**Build worlds humans can play and agents can operate.**

LudoWeave is an experimental, deterministic, headless-first Python engine for 2D and layered-2D games. It is being designed so human-facing tools, tests, replay, and software agents can eventually operate the same canonical world through typed, validated commands.

> Project status: pre-alpha. M0, the pure-Python M1 deterministic world core, M2 typed command/snapshot/replay protocols, and the M3 isolated 2D rendering vertical slice are implemented. APIs and wire formats are experimental and may change without deprecation.

## What exists

- A typed engine lifecycle with explicit ownership and close semantics.
- Monotonic and deterministic virtual clocks.
- An engine-owned rendering protocol and validation-only null renderer.
- A headless fixed-tick example.
- `ludoweave --version` and a structured `ludoweave doctor` command.
- Architecture rules, ADRs, tests, documentation, packaging, and cross-platform CI.
- Generational entity IDs and a deterministic allocator whose stale handles never revive.
- Explicit immutable component schemas, UUID-sorted registries, and validated forward migrations.
- Canonical pure-Python dense/sparse world storage with copy-safe component ownership.
- Typed storage-neutral queries with explicit writable cursor lifetimes and change filters.
- Atomic local structural command buffers with exact deferred-entity ownership.
- Explicit copy-owned typed resources and deterministic conflict-aware serial schedule planning.
- An additive fixed-step application runner with immutable virtual/recorded input and declared-access system contexts.
- An independent dictionary reference world exercised by state-machine property tests.
- Versioned canonical world commands with atomic transactions, optimistic hashes, dry-run, semantic diffs, and structured receipts.
- Complete authority snapshots, SHA-256 state hashes, explicit persistent-resource migrations, and deterministic named random streams.
- Self-contained verified replay/checkpoint files and immutable parent-referenced timeline branches.
- Project-confined `apply`, `snapshot`, `replay`, and `diff` CLI workflows for a deliberately data-only empty project composition.
- Immutable presentation extraction, backend-neutral descriptors and scoped generational render handles, explicit render-graph validation, and deferred destruction.
- An optional exactly pinned wgpu/rendercanvas/GLFW adapter with orthographic instanced atlas sprites, tile/debug batches, resize, typed loss, and offscreen RGBA capture.

General game-project loading, scenes/assets, platform input, physics, audio, networking, MCP, editor tooling, 3D, and automatic GPU recovery are not implemented yet.

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
uv run python examples/fixed_step_world.py --ticks 6
```

The example prints one JSON summary and uses virtual time plus the null renderer, so it does not open a window or wait in real time.

GPU rendering is an optional locked extra and is selected only by a composition root:

```console
uv sync --frozen --all-groups --extra graphics
uv run --frozen --extra graphics python examples/hello_sprite.py
```

The sprite example renders two atlas regions in one instanced draw and prints a versioned offscreen-capture summary. Add `--window` to exercise the rendercanvas/GLFW window surface on a desktop session.

## Public API

The root package intentionally exposes only the initial application surface:

```python
from ludoweave import Engine, EngineConfig, LifecycleState, __version__
from ludoweave.core.clock import VirtualClock
from ludoweave.ecs import ComponentRegistry, EntityAllocator, World
from ludoweave.render import NullRenderBackend, RenderDescriptor

clock = VirtualClock()
backend = NullRenderBackend()

with Engine(EngineConfig(), backend, clock=clock) as engine:
    summary = engine.run(ticks=10)

entities = EntityAllocator()
entity_id = entities.create()
entities.validate(entity_id)

world = World(ComponentRegistry())
world_entity = world.spawn()
assert world.entities() == (world_entity,)

for queried_id, in world.query().stable().rows():
    assert queried_id == world_entity

commands = world.commands()
pending = commands.spawn()
result = world.flush(commands)
assert result.resolve(pending) in world.entities()
```

See the [architecture overview](docs/architecture.md), [runtime contract](docs/runtime-contract.md), [entity identity contract](docs/ecs.md), and [2D rendering contract](docs/rendering.md) before depending on these experimental APIs.
The [headless command workflow](docs/cli-workflows.md) documents the M2 data-only project manifest and full CLI example.

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
uv run --frozen python benchmarks/benchmark_m1.py --samples 30 --seed 1 --json-out .tmp/m1-benchmark.json
uv run --frozen python benchmarks/validate_m1_results.py .tmp/m1-benchmark.json
uv run --frozen python benchmarks/benchmark_m2.py --samples 30 --seed 1 --json-out .tmp/m2-benchmark.json
uv run --frozen python benchmarks/validate_m2_results.py .tmp/m2-benchmark.json
uv run --frozen --extra graphics python benchmarks/benchmark_m3.py --samples 30 --output .tmp/m3-benchmark.json
uv run --frozen --extra graphics python benchmarks/validate_m3_results.py .tmp/m3-benchmark.json
git diff --check
```

Milestone benchmark commands are not part of every edit's fast gate. M1 and M3 record local target observations; M2 measurements are informational and have no timing pass threshold. Results are recorded only after commands have actually run; see [test evidence](.ai/TEST_EVIDENCE.md) and the [benchmark methodology](docs/benchmarks.md).

## Contributing and project policy

Contributions use the [Developer Certificate of Origin](CONTRIBUTING.md), not a CLA. Please also read the [code of conduct](CODE_OF_CONDUCT.md), [security policy](SECURITY.md), [governance model](GOVERNANCE.md), and repository guidance in [AGENTS.md](AGENTS.md).

LudoWeave Engine is licensed under the [Apache License 2.0](LICENSE).
