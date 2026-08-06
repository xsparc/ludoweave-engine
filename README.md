# LudoWeave Engine

**Build worlds humans can play and agents can operate.**

LudoWeave is an experimental, deterministic, headless-first Python engine for 2D and layered-2D games. Human-facing tools, tests, replay, and software agents operate the same canonical world through typed, validated commands.

> Project status: community-alpha release candidate (`0.1.0a1`). M0 through M23 are hosted-validated and integrated into `main`. M24 adds a strict cross-version corpus admission harness while correctly retaining the current single-version gate as false. The M12 manifest surface remains the first preview contract under RFC-0002.

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
- Provider-neutral key/pointer/window/gamepad events, explicit gamepad deadzones,
  immutable transition-aware action snapshots, and virtual/recorded/live input
  sources.
- Project-confined `asset://` manifests, content-addressed dependency caching, bounded PNG loading, and retained safe texture replacement.
- Deterministic AABB/circle collision, a property-tested spatial grid, documented kinematic resolution, and a minimal owned Null audio adapter.
- Bounded tick animation, bitmap atlas text layout, immutable chunked tilemaps,
  seeded fixed-point particles, and a Null-audio acyclic mix graph, all
  exercised by one dependency-free headless showcase.
- Preview canonical data-only plugin manifests with deterministic
  environment/policy/dependency checks and no discovery or code execution.
- Bounded offline correction-branch evidence that records the current replay
  input-history gap and defers networking/live rollback under ADR-0027.
- Deterministic installed-surface evidence that retains layered 2D and defers
  constrained 3D under ADR-0028 without adding runtime contracts or providers.
- Deterministic installed-surface evidence that confirms the command/receipt,
  typed-tool, MCP, and inspector foundation through an actual ephemeral
  receipted mutation while deferring a visual editor under ADR-0029 without
  adding a GUI, runtime API, format, or dependency.
- A security threat model and deterministic installed evidence that preserve
  the data-only plugin boundary and defer WASM runtimes, guest execution, WASI,
  and host calls under ADR-0030.
- A versioned installed render-device baseline that produces sanitized,
  deterministic evidence from an explicitly supplied trusted adapter factory;
  it performs no discovery and is not a security certification.
- A versioned installed agent-tool baseline that exercises all 12 typed tools,
  transaction/tick receipts, stale-hash atomicity, query/diff, provider result
  shapes, and close behavior through an explicitly supplied trusted factory.
- A versioned installed `WorldStore` baseline that exercises entity generations,
  epochs, detached copies, queries, command atomicity, cloning, and structured
  failures through an explicitly supplied trusted factory.
- Deterministic installed command/receipt stability evidence that confirms the
  same-version canonical and atomic foundation while retaining experimental
  status under RFC-0003 until every compatibility gate is evidenced.
- A strict bounded `ludoweave.receipt/1` reader with detached immutable output,
  typed failures, configurable resource limits, and frozen `0.1.0a1` fixtures
  that seed—but do not yet satisfy—a cross-version compatibility corpus.
- A deterministic admission harness that verifies those historical bytes and
  requires a different installed reader version plus supported-release
  evidence before any cross-version claim.
- Exact v1 contracts and an explicit versioned evolution policy for all seven
  built-in operation argument shapes, exercised from installed artifacts
  without adding a runtime schema layer.
- ECS-authoritative Clockwork Arena with fixed-seed waves, enemies, projectiles, health, score, restart, exact 3,600-tick replay evidence, optional wgpu presentation, and stress workloads.
- A transport-independent typed agent service with explicit capabilities, quotas, redaction, serialized mutations, and the same canonical command receipts used by direct Python.
- Twelve observation/control tools exposed through Python, a project-confined CLI, and a local-only MCP `2025-11-25` stdio adapter with no network listener.
- An owned local `ludoweave inspect` child composition with read-only defaults,
  explicit receipted sample/tick mutations, versioned semantic observations,
  and verified snapshot/diff hash continuity.
- An Agent World Builder acceptance loop covering typed creation, validation, application, ticks, capture, query, adjustment, diff, telemetry, tests, and replay evidence.
- Deterministic release staging with a pure wheel, source distribution, sample bundle, checksums, SPDX SBOM, notices, manifest, installed-artifact smoke, and a pinned provenance workflow.
- Explicit stability metadata for every public Python export, community-alpha user/adapter/contribution guides, and a repository-native triage/roadmap queue.
- Versioned, sanitized profiling for the representative M1/M3 misses plus an accepted RFC retaining the pure-Python/no-compiler baseline.
- A bounded isolated Box2D-candidate probe plus ADR-0024; no physics binding,
  adapter, native object, or runtime dependency is shipped.

General scene importers, production audio, international text shaping,
rigid-body physics, networking or remote agent transport, visual editor
tooling, executable Python/WASM mods, constrained or general 3D, and automatic
GPU recovery are not implemented.

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
uv run python examples/clockwork_arena.py --ticks 600
uv run python examples/rollback_readiness.py --ticks 120 --branch-tick 60
uv run python examples/cross_version_corpus_readiness.py
uv run python examples/command_receipt_stability_decision.py
uv run python examples/operation_argument_compatibility.py
uv run python examples/receipt_reader.py
uv run python examples/constrained_3d_decision.py
uv run python examples/visual_editor_decision.py
uv run python examples/wasm_mod_security_decision.py
uv run python examples/render_device_conformance.py
uv run python examples/agent_tool_conformance.py
uv run python examples/world_store_conformance.py
uv run python examples/world_store_conformance.py --backend reference
uv run python examples/alpha_acceptance.py
uv run ludoweave plugin check examples/example.plugin.json
uv run ludoweave inspect --sample agent-world-builder
```

The example prints one JSON summary and uses virtual time plus the null renderer, so it does not open a window or wait in real time.

GPU rendering is an optional locked extra and is selected only by a composition root:

```console
uv sync --frozen --all-groups --extra graphics
uv run --frozen --extra graphics python examples/hello_sprite.py
uv run --frozen --extra graphics python examples/agent_world_builder.py
uv run --frozen --extra graphics python examples/render_device_conformance.py --backend wgpu
```

The sprite example renders two atlas regions in one instanced draw and prints a versioned offscreen-capture summary. Add `--window` to exercise the rendercanvas/GLFW window surface on a desktop session.

Clockwork Arena can use the same optional renderer. Add `--window --interactive`
for WASD/arrows, pointer aim, primary-button fire, and R restart. Gamepad slot 0
uses left/right sticks, A, and Start:

```console
uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 36000 --renderer wgpu --window --interactive
```

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

See the [architecture overview](docs/architecture.md), [runtime contract](docs/runtime-contract.md), [entity identity contract](docs/ecs.md), [2D rendering contract](docs/rendering.md), and [M4 gameplay guide](docs/gameplay.md) before depending on these experimental APIs.
The [headless command workflow](docs/cli-workflows.md) documents the M2 data-only project manifest and full CLI example.
The [agent control interface](docs/agent-control.md) documents M5 tools, capabilities, limits, Python/CLI/MCP composition, and the Agent World Builder loop.
The [live semantic inspector guide](docs/inspector.md) documents M10 local child
ownership, observation events, explicit write receipts, bounds, and failures.
The [rich 2D presentation guide](docs/presentation.md) documents M11 animation,
bitmap text, tilemap, particle, and audio-mix ownership and determinism.
The [plugin compatibility guide](docs/plugins.md) documents M12 inert manifests,
preview compatibility, deterministic reports, and the explicit no-loader boundary.
The [rollback-readiness guide](docs/rollback-readiness.md) documents M13's
offline correction proof, external input-history limitation, network deferral,
and complete revisit gate.
The [constrained 3D decision](docs/constrained-3d-decision.md) documents M14's
installed-surface evidence, retained layered-2D scope, and complete revisit
gate.
The [visual-editor admission decision](docs/visual-editor-decision.md)
documents M15's positive protocol foundation, missing authoring contracts,
target users and jobs, and complete revisit gate. It retains the finite
headless inspector instead of creating a widget-side state model.
The [WASM-mod security decision](docs/wasm-mod-security-decision.md) documents
M16's threat model, current inert boundary, prospective blockers, complete
admission gate, and explicit runtime deferral.
The [render-device conformance guide](docs/render-device-conformance.md)
documents M17's explicit-factory trust boundary, versioned checks, sanitized
report, limitations, and evidence expectations for external adapters.
The [agent-tool conformance guide](docs/agent-tool-conformance.md) documents
M18's fixed 12-check profile, fresh-authority precondition, ownership,
sanitized evidence, and explicit non-certification boundary.
The [WorldStore conformance guide](docs/world-store-conformance.md) documents
M19's fixed 10-check profile, borrowed registry identity, current no-close
in-memory boundary, sanitized evidence, and non-certification limitations.
The [command and receipt stability decision](docs/command-receipt-stability-decision.md)
documents M20's installed same-version evidence, complete preview gate, and
RFC-0003 decision to retain experimental status without changing a wire format.
The [bounded receipt-reader guide](docs/receipt-reader.md) documents M21's
exact v1 schema checks, limits, immutable decoding, failure behavior, and
single-version fixture non-claim under RFC-0004.
The [operation-argument compatibility guide](docs/operation-argument-compatibility.md)
documents M22's exact seven v1 shapes, fail-closed unknown-field rule,
versioned breaking-change policy, installed evidence, and remaining RFC-0003
gates under RFC-0005.
The [receipt semantic compatibility guide](docs/receipt-semantic-compatibility.md)
documents M23's exact v1 diff fields and meanings, status-specific presence,
diagnostic-code identity/fallback rules, installed evidence, and remaining
RFC-0003 gates under RFC-0006.
The [community-alpha user guide](docs/user-guide.md), [adapter guide](docs/adapter-guide.md), [API policy](API_COMPATIBILITY.md), and [release verification guide](docs/release-process.md) cover the M6 evaluation boundary.

Agent mutation is disabled unless the trusted composition root explicitly
enables it. For example, these launch the built-in sample over local stdio:

```console
uv run ludoweave mcp --sample agent-world-builder
uv run ludoweave mcp --sample agent-world-builder --write --renderer wgpu
uv run ludoweave inspect --sample agent-world-builder
uv run ludoweave inspect --sample agent-world-builder --write --bootstrap --ticks 2
```

The first MCP process and first inspector session are read-only. None of these
commands opens a network listener; the inspector can launch only the built-in
MCP child through the current Python interpreter.

## Quality commands

```console
uv lock --check
uv sync --frozen --all-groups --extra graphics
uv run --frozen ruff format --check .
uv run --frozen ruff check .
uv run --frozen pyright
uv run --frozen pytest -q
uv run --frozen mkdocs build --strict
uv build
uv run --frozen python scripts/smoke_wheel.py dist
uv run --frozen python scripts/release_artifacts.py dist .tmp/release-candidate
uv run --frozen python scripts/smoke_release.py .tmp/release-candidate
uv run --frozen python benchmarks/benchmark_m1.py --samples 30 --seed 1 --json-out .tmp/m1-benchmark.json
uv run --frozen python benchmarks/validate_m1_results.py .tmp/m1-benchmark.json
uv run --frozen python benchmarks/benchmark_m2.py --samples 30 --seed 1 --json-out .tmp/m2-benchmark.json
uv run --frozen python benchmarks/validate_m2_results.py .tmp/m2-benchmark.json
uv run --frozen --extra graphics python benchmarks/benchmark_m3.py --samples 30 --output .tmp/m3-benchmark.json
uv run --frozen --extra graphics python benchmarks/validate_m3_results.py .tmp/m3-benchmark.json
uv run --frozen python benchmarks/benchmark_m4.py --samples 300 --warmups 60 --output .tmp/m4-benchmark.json
uv run --frozen python benchmarks/validate_m4_results.py .tmp/m4-benchmark.json
uv run --frozen python -m benchmarks.profile_m7 --repeats 5 --output .tmp/m7-profile-base.json
uv run --frozen python -m benchmarks.validate_m7_profile .tmp/m7-profile-base.json
uv run --frozen --extra graphics python -m benchmarks.profile_m7 --repeats 5 --include-wgpu --output .tmp/m7-profile-graphics.json
uv run --frozen python -m benchmarks.validate_m7_profile .tmp/m7-profile-graphics.json
git diff --check
```

Milestone benchmark/profile commands are not part of every edit's fast gate. M1, M3, and M4 record local target observations; M2 measurements are informational and have no timing pass threshold. M7 profile time is diagnostic rather than a benchmark. Results are recorded only after commands have actually run; see [test evidence](.ai/TEST_EVIDENCE.md), the [benchmark methodology](docs/benchmarks.md), and [RFC-0001](docs/rfcs/0001-defer-first-native-kernel.md).

Pull-request CI deliberately uses eight essential hosted jobs: one complete
Ubuntu 3.12 quality, non-provider test, documentation, package,
installed-wheel, and release gate; four compatibility jobs spanning CPython
3.13/3.14 plus Windows and macOS; and three real graphics jobs across Linux,
Windows, and macOS. The pure universal wheel is smoke-tested once rather than
rebuilding the same artifact three times, provider tests run only in jobs with
the required graphics runtime, and superseded runs are cancelled automatically.

The M9 Box2D probe is also evaluation tooling, not a normal quality command or
dependency. Run it only in an isolated environment with an explicit candidate:

```console
uv run --no-project --python 3.12 --with box2d-python==0.1.2 python scripts/probe_box2d_candidate.py
```

A successful result establishes only bounded same-binary headless/lifecycle
smoke. It does not admit the binding or claim cross-platform determinism; see
[ADR-0024](docs/adr/0024-defer-box2d-v3-plugin-after-admission-review.md).

Release staging requires a new empty output directory. The tag workflow is
defined for a future maintainer-created `vVERSION` tag; this repository task
does not create a tag, publish a GitHub release, or upload to PyPI.

## Contributing and project policy

Contributions use the [Developer Certificate of Origin](CONTRIBUTING.md), not a CLA. Start with the [first-contribution walkthrough](docs/first-contribution.md) and [roadmap board](ROADMAP.md). Please also read the [code of conduct](CODE_OF_CONDUCT.md), [security policy](SECURITY.md), [governance model](GOVERNANCE.md), and repository guidance in [AGENTS.md](AGENTS.md).

LudoWeave Engine is licensed under the [Apache License 2.0](LICENSE).
