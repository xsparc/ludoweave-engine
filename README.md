# LudoWeave Engine

**Build worlds humans can play and agents can operate.**

LudoWeave is an experimental, deterministic, headless-first Python engine for 2D and layered-2D games. Human-facing tools, tests, replay, and software agents operate the same canonical world through typed, validated commands.

> Current validation: M0 through M75 are hosted-validated and integrated into
> `main`; M76 is the active private release-consumer hardening milestone.

> Project status: community-alpha release candidate (`0.1.0a1`). M0 through M75 are hosted-validated and integrated into `main`. M28 retains its empty reviewed sample-game manifest and zero-adoption result; M29 retains its empty reviewed contributor-retention manifest and zero-retention result; M30 retains its empty reviewed installation-matrix manifest and no published-wheel installation claim; M31 retains its empty reviewed measurement manifest for response/review latency and no response-time, review-time, or SLA claim. M32 retains its empty reviewed execution manifest and no measured divergence rate. M33 retains its empty reviewed benchmark comparison manifest and no measured regression rate. M34 retains its empty reviewed call manifest and no measured recovery-free completion rate. M35 retains an empty reviewed third-party conformance submission manifest and zero passing external implementations. M36 consolidates the unchanged eight validation slices into three hosted runner allocations. M37 adds fail-closed change qualification so documentation-only work uses a bounded Linux gate while substantive work retains every M36 slice. M38 enforces same-source wheel/sdist byte reproducibility inside those existing distribution jobs. M39 enforces an annotated, GitHub-verified release tag at the exact `origin/main` commit before expensive or publishing work. M40 verifies the private draft's exact remote asset identities before publication. M41 requires its authenticated release-notes body to exactly match staged `RELEASE_NOTES.md`. M42 extends the same-release identity boundary through an exact postpublication state observation. M43 adds exact-ID authenticated asset retrieval and byte revalidation. M44 adds exact-source provenance verification for every retrieved asset and SPDX SBOM verification for the pure wheel. M45 adds bounded credential-free exact-ID public retrieval and installed-candidate smoke. M46 adds a separate fresh-runner rehearsal. M47 replaces its Bash-only verifier and widens that tag-only rehearsal to Ubuntu, Windows, and macOS. M48 constrains the shared client's response and failure semantics. M49 confines every actual connected peer to globally reachable unicast. M50 isolates the portable verifier from ambient TLS key logging. M51 validates each actual negotiated TLS session before HTTP transmission. M52 observes the URL-derived TLS service identity and non-empty peer certificate before session checks and HTTP. M53 binds the actual socket to its exact verified client context. M54 requires each connected socket to report an exactly fresh, non-reused TLS session before later TLS evidence or HTTP. M55 validates the documented HTTP/1.1-class value and supported framing before status, redirect, or body use, without claiming exact raw status-line identity. M56 adds strict response-status and single bounded Location URI-reference validation. M57 constrains response-body block shapes and declared-length agreement without changing workflows, pull-request allocations, or release authority. M60 adds non-following output collision checks, M61 separates candidate and output-root filesystem identities, M62 constrains portable asset names, M63 confines subordinate consumer output, M64 bounds staged sample extraction, M65 constrains portable sample member paths, M66 stages complete sample roots before publication, M67 requires the exact expected sample inventory before extraction, M68 bounds the regular archive container before ZIP parsing, M69 rejects encrypted-member indicators before reads or staging, M70 binds parsing and publication to the staged sample checksum, M71 parses an owned checksum-admitted sample snapshot, M72 normalizes documented ZIP parser failures content-silently, M73 adds strict ZIP-name decoding failures, M74 adds exact deflate decompression failures to that stable boundary, M75 rejects compressed patched data before reads or staging, and M76 rejects method-8 enhanced-deflate indicators before reads or staging. The M12 manifest surface remains the first preview contract under RFC-0002.

M58 through M66 are hosted-validated and integrated. M60-M66 harden public-
release filesystem, asset-name, and consumer-output handling without changing
engine runtime or a public protocol. M59's tool-neutral repository metadata
convention remains enforced.

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
- A strict external-consumer-feedback admission harness whose empty reviewed
  manifest keeps the current adoption gate false.
- A strict supported feature-release-channel admission harness whose empty
  reviewed manifest keeps the deprecation-channel gate false.
- A strict external-contributor rehearsal admission harness whose empty
  reviewed manifest explicitly does not claim that an independent human has
  completed the public contribution path without private maintainer knowledge.
- A strict external sample-game adoption admission harness whose empty reviewed
  sample-game manifest keeps the externally authored game count at zero.
- A strict published-wheel installation-matrix admission harness whose empty
  reviewed manifest keeps the current clean-install result false.
- A strict issue-response and pull-request-review latency admission harness
  whose empty reviewed manifest keeps all counts and latency aggregates absent.
- A strict controlled benchmark-regression-rate admission harness whose empty
  reviewed manifest keeps all comparison counts and rate absent.
- A strict agent-tool recovery-rate admission harness whose empty reviewed
  agent-tool call manifest keeps all call counts and recovery-free rate absent.
- A strict third-party conformance-adoption admission harness whose empty
  reviewed submission manifest keeps the passing external implementation count
  at zero without discovering, loading, or executing packages.
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
- Deterministic release staging with a pure wheel, source distribution, sample bundle, checksums, SPDX SBOM, notices, manifest, installed-artifact smoke, a pinned provenance workflow, fail-closed repeat-build byte verification, and signed annotated-tag identity/main-ancestry admission.
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
uv run python examples/external_consumer_feedback_readiness.py
uv run python examples/supported_release_channel_readiness.py
uv run python examples/external_contributor_rehearsal_readiness.py
uv run python examples/external_contributor_retention_readiness.py
uv run python examples/external_sample_game_adoption_readiness.py
uv run python examples/installation_matrix_readiness.py
uv run python examples/response_review_latency_readiness.py
uv run python examples/replay_divergence_rate_readiness.py
uv run python examples/benchmark_regression_rate_readiness.py
uv run python examples/agent_tool_recovery_rate_readiness.py
uv run python examples/third_party_conformance_adoption_readiness.py
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
The [external-contributor rehearsal readiness guide](docs/external-contributor-rehearsal-readiness.md)
documents M27's reviewed-history, human-review, privacy, and installed-artifact
contract while retaining the current empty-record result as false.
The [external sample-game adoption readiness guide](docs/external-sample-game-adoption-readiness.md)
documents M28's authorship, provenance, installed-capability, licensing, and
complete-history gate while retaining the current externally authored game
count at zero.
The [external contributor-retention readiness guide](docs/external-contributor-retention-readiness.md)
documents M29's same-person, chronology, DCO, validation, provenance, and
complete-history gate while retaining the current retained-contributor count
at zero and excluding popularity metrics.
The [installation-matrix readiness guide](docs/installation-matrix-readiness.md)
documents M30's immutable public-wheel, clean-environment, exact-matrix, and
complete-history gate while retaining the current zero-record result.
The [response and review latency readiness guide](docs/response-review-latency-readiness.md)
documents M31's complete-census, pending-item, first-qualifying-action, and
complete-history gate while retaining the current empty reviewed measurement
manifest and defining no SLA.
The [replay-divergence-rate readiness guide](docs/replay-divergence-rate-readiness.md)
documents M32's complete CI execution cohort, preserved non-execution outcomes,
exact rational rate, and history gate while retaining the current empty
reviewed execution manifest and no measured divergence rate.
The [benchmark-regression-rate readiness guide](docs/benchmark-regression-rate-readiness.md)
documents M33's registered paired-benchmark cohort, controlled-comparability,
predeclared integer tolerance, non-execution, and history gates while retaining
the current empty reviewed comparison manifest and no measured regression rate.
The [agent-tool recovery-rate readiness guide](docs/agent-tool-recovery-rate-readiness.md)
documents M34's complete task-directed call cohort, exact manual-recovery
definition, terminal-evidence and history gates while retaining the current
empty reviewed agent-tool call manifest and no measured recovery-free
completion rate.
The [third-party conformance-adoption readiness guide](docs/third-party-conformance-adoption-readiness.md)
documents M35's fixed installed-profile registry, independent-authorship,
plugin-manifest, failure-preservation, and complete-history gates while
retaining the current empty reviewed submission manifest and zero passing
third-party implementations.
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
uv build --out-dir .tmp/dist-first
uv build --out-dir .tmp/dist-second
uv run --frozen python scripts/verify_distribution_reproducibility.py .tmp/dist-first .tmp/dist-second
uv run --frozen python scripts/smoke_wheel.py .tmp/dist-first
uv run --frozen python scripts/release_artifacts.py .tmp/dist-first .tmp/release-candidate
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

Milestone benchmark/profile commands are not part of every edit's fast gate. M1, M3, and M4 record local target observations; M2 measurements are informational and have no timing pass threshold. M7 profile time is diagnostic rather than a benchmark. Results are recorded only after commands have actually run; see [test evidence](.project/TEST_EVIDENCE.md), the [benchmark methodology](docs/benchmarks.md), and [RFC-0001](docs/rfcs/0001-defer-first-native-kernel.md).

M36 pull-request CI preserves the same eight validation slices while grouping
them into three OS-owned hosted runner allocations: one Ubuntu runner covers
quality/distribution, CPython 3.12-3.14, and Linux graphics; Windows and macOS
each cover CPython 3.12 graphics plus 3.14 compatibility. This uses five fewer
runner allocations without deleting a version, platform, graphics, package,
installed-wheel, release, documentation, or static-analysis slice. The pure
universal wheel is smoke-tested once rather than rebuilding the same artifact
three times, provider tests run only after the required graphics runtime is
installed, and superseded runs are cancelled automatically.
The gate runs only for substantive pull requests: a validated tree is not run
again after merge to unprotected `main`, and `.project/**`-only factual record
pull requests consume no hosted runner quota.

M37 keeps one visible pull-request workflow but qualifies the diff from the
trusted base revision. Documentation-only changes run one Linux allocation for
lock, formatting/lint, strict docs, architecture, build, installed-wheel, and
release-candidate checks. Any unrecognized, empty, mixed, or indeterminate diff
is substantive or fails closed. Substantive changes retain all three hosted
allocations and eight M36 validation slices; Windows and macOS begin only after
the Linux qualification and complete gate succeed.

M38 builds the pure wheel and source distribution twice inside the already
allocated Linux distribution step and fails unless both artifact pairs are
byte-identical. The same comparison runs before smoke, staging, attestation, or
publication in the tag workflow. It adds no runner, matrix entry, dependency,
action, permission, trigger, credential, or cross-platform reproducibility
claim.

M39 makes the existing tag-only release job fail before system setup, tests,
build, attestation, or publication unless the exact `vVERSION` ref is an
annotated tag whose signature GitHub reports as valid, whose local/GitHub tag
object targets the checked-out event commit, and whose commit is reachable from
fetched `origin/main`. The validator emits only safe tag/object/commit identities
and never prints the signature or payload. This adds no runner, action,
permission, trigger, dependency, key allowlist, tag, or publication authority;
RFC-0022 defines the trust boundary.

M40 makes the existing GitHub release transition explicit: create a prerelease
draft without assets, upload every staged file without clobbering, fetch the
version-pinned release document, and compare every uploaded name, byte size,
state, and SHA-256 digest with bounded local staging before publication. A
failure leaves an unpublished draft for inspection. This adds no runner,
action, permission, trigger, dependency, tag, release, or publication authority
and does not enable immutable releases; RFC-0023 defines the boundary.

M41 requires the authenticated private draft's release-notes body to exactly
equal the bounded non-empty UTF-8 `RELEASE_NOTES.md` already supplied through
`--notes-file` and covered as a staged asset. Missing, null, substituted,
truncated, or normalization-different bodies fail without logging note content.
This changes no workflow, runner, permission, dependency, tag, release, or
publication authority; RFC-0024 defines the source-body boundary.

M42 carries the exact authenticated release database ID across the publication
transition and rechecks the resulting public prerelease's state, UTC
publication time, notes, and assets. A mismatch fails the release job but never
automatically unpublishes or deletes evidence. This adds one read-only API
request inside the existing tag job, no runner or permission, and neither
requires nor claims immutable releases; RFC-0025 defines the boundary.

M43 requires each published asset to have a unique bounded numeric ID, writes
an exclusive runner-temporary retrieval plan only after complete validation,
downloads those exact IDs through the authenticated GitHub asset API, and
rehashes the retrieved directory against the same published document. It adds
no job, runner, action, permission, dependency, tag/release authority, clobber,
or rollback. It does not claim unauthenticated availability, global CDN state,
future immutability, or consumer installation; RFC-0026 defines the boundary.

M44 verifies SLSA v1 provenance for every exact M43-retrieved asset and an
SPDX 2.3 SBOM attestation for the single pure wheel. Each content-silent,
30-second-bounded GitHub CLI call fixes the repository, release workflow, tag,
source/signer commit, OIDC issuer, hosted-runner class, predicate, and candidate
limit. Failure occurs after publication and grants no mutation or rollback.
This is an integrity/identity check, not artifact-security, independent-build,
predicate-truth, future-availability, immutability, installation, or supported-
channel evidence; RFC-0027 defines the boundary. No real attestation pass is
claimed until an authorized signed-tag release run executes.

M45 follows M44 by fetching the exact public release ID and every exact M43
asset ID from fixed HTTPS GitHub API endpoints without supplying a GitHub
credential. It revalidates the public document and bounded downloaded set,
then runs complete release smoke—including isolated wheel installation and the
sample bundle—against those public bytes. The step adds no job, runner, action,
permission, dependency, release, or publication authority. It observes one
same-run public API path, not an independent/external consumer, every CDN or
browser path, future availability, immutability, cross-platform installation,
PyPI, or a supported channel; RFC-0028 defines the boundary. No real public-
path pass is claimed until an authorized signed-tag release run executes.

M46 follows M45 with one dependent read-only Linux job on a fresh hosted runner.
It retrieves the exact candidate preserved by the publishing job, creates a new
bounded plan, downloads the public bytes without a release credential,
revalidates them, and runs complete installed release smoke in its own
workspace. This is a same-workflow rehearsal—not independent/external or cross-
platform consumer evidence, a clean machine outside GitHub-hosted Actions,
future availability, immutability, artifact security, PyPI, or a supported
channel. RFC-0029 defines the boundary. No real fresh-runner pass is claimed
until an authorized signed-tag release run executes.

M47 follows M46 by replacing the internal Bash verifier with one typed,
standard-library Python program and running the tag-only fresh-consumer job on
Ubuntu, Windows, and macOS. Every operating-system runner retrieves the same
admitted candidate, creates its own bounded plan, fetches exact public bytes
without a release credential, and runs complete installed release smoke. This
is cross-platform same-workflow evidence, not independent/external verification,
a clean machine outside GitHub-hosted Actions, every delivery path, future
availability, immutability, artifact security, PyPI, or a supported channel.
RFC-0030 defines the boundary. No real cross-platform public-consumer pass is
claimed until an authorized signed-tag release run executes.

M48 follows M47 by accepting only the GitHub-documented response shapes: a
direct `200` for the public release document, and `200` or bounded `302`
handling for assets. API-version headers stay on `api.github.com`; timeout,
transport/protocol, and local-output failures retain distinct stable codes.
RFC-0031 defines the boundary. This changes no workflow, dependency, runtime
API, release authority, or independent/external evidence claim, and no real
M48 pass is claimed without an authorized signed-tag run.

M49 follows M48 by explicitly connecting each fixed API or redirected asset
hop and validating its actual port-443 TLS socket peer before any HTTP request.
Only globally reachable unicast IPv4/IPv6 is accepted; IPv4-mapped IPv6 is
classified by its embedded address. RFC-0032 defines the stable forbidden,
timeout, and request-failure boundary. This is not a hostname/IP allowlist,
separate DNS preflight, network sandbox, real public release observation, or
release-authority change, and no real M49 pass is claimed without an authorized
signed-tag run.

M50 replaces ambient-sensitive default TLS context creation with an explicit
client context for every public API or asset hop. It retains system server-auth
trust, mandatory certificate and hostname validation, TLS 1.2 or newer, and
strict X.509 verification while ensuring `SSLKEYLOGFILE` cannot enable TLS
session-secret logging or create its target. RFC-0033 defines the stable
content-silent TLS-context failure boundary. M50 changes no workflow,
dependency, runtime API, release authority, or real-release claim.

M51 inspects the actual negotiated TLS session after the connected-peer check
and before every HTTP request. It accepts only TLSv1.2 or TLSv1.3, a
well-formed cipher report with at least 128 secret bits, no TLS compression,
and ALPN `http/1.1` or no negotiated ALPN. The client advertises only
`http/1.1`; every redirected hop repeats the complete check. RFC-0034 defines
the content-silent failure and ownership boundary. This adds no cipher-name
allowlist, custom trust, workflow, dependency, runtime API, release authority,
or real public release observation.

M52 observes the actual TLS socket's service identity after the connected-peer
check and before the M51 session check. The URL hostname is normalized with
built-in IDNA to the reference hostname; the socket must retain that hostname
case-insensitively and expose a non-empty DER peer certificate. The M50 verified
context remains authoritative for certificate-path and hostname matching. Every
redirect repeats the check. RFC-0035 defines the content-silent failure and
ownership boundary. This adds no certificate parsing, pinning, custom trust,
revocation/CT policy, workflow, dependency, runtime API, release authority, or
real public release observation.

M53 verifies after the handshake that every actual TLS socket retains the
exact context object supplied for that hop and is strictly client-side. It then
revalidates the complete M50 context policy before M52 service-identity and M51
session checks or any HTTP transmission. Every redirect repeats the binding
and policy check with an independent context. RFC-0036 defines the content-
silent failure and ownership boundary. This adds no custom trust, pinning,
workflow, dependency, runtime API, release authority, or real public release
observation.

M54 reads `session_reused` from that actual socket after M53 context binding
and requires exactly `False` before service identity, negotiated-session
inspection, or HTTP transmission. Every redirect repeats the observation.
RFC-0037 defines the content-silent failure and ownership boundary. This adds
no session cache, ticket control, custom TLS implementation, workflow,
dependency, runtime API, release authority, or real public release observation.

M55 validates every response, including every redirect, through documented
HTTP/1.1-class metadata before status or body use. The public version value must
be integer `11`, while RFC-0038 explicitly records that CPython can normalize
other raw `HTTP/1.x` values and this is not exact status-line token evidence.
`Transfer-Encoding` must be absent or exactly `chunked` case-insensitively; it
may not coexist with `Content-Length`, whose existing bounded ASCII-decimal
checks remain. This adds no alternate HTTP client, private response-state
dependency, workflow, runtime API, release authority, or real public release
observation.

M56 validates the documented response status after M55 framing and before
comparison, redirect resolution, or body use. The status is a non-boolean
integer from 100 through 599. Every followed `302` exposes exactly one Location
field whose value is a single URI-reference from 1 through 8,000 ASCII octets
with complete percent escapes; bracket delimiters are permitted only in a
parsed authority, not a path, query, or fragment. The resolved target then
repeats the bounded HTTPS, peer, TLS, framing, deadline, size, and exact-byte
checks. RFC-0039 adds no host allowlist, raw parser, workflow, dependency,
runtime API, release authority, or real public release observation.

M57 validates each successful response body after M56 status/redirect checks.
Every `HTTPResponse.read(amount)` result must be immutable bytes no larger than
the requested amount before EOF interpretation, accounting, or local output.
Any validated `Content-Length` must exactly equal the streamed octets for both
the release document and final asset responses. RFC-0040 retains short reads,
chunked decoding through the standard-library client, close-delimited bodies
without a declaration, and independent expected asset sizes. It adds no raw
parser or cleanup, introduces no alternate client, and changes no workflow,
dependency, runtime API, release authority, or real public release observation.

M58 closes every obtained response before its created connection and makes
both close attempts even when response close fails. An active primary failure
remains primary; cleanup-only ordinary failures become content-silent
`public_release.request_failed`, while cleanup control signals remain
unwrapped. Successful cleanup occurs before redirect continuation and before
partial publication to a separate final asset path. RFC-0041 adds no rollback,
retry, workflow, dependency, runtime API, release authority, or real public
release observation.

M60 checks each fresh release document, download directory, retrieval plan,
asset target, and asset partial by final-entry `lstat()` before network or
validator work can use it. A file, directory, live link, or dangling link is a
filesystem collision; normal output collisions retain
`public_release.output_exists`, a fresh-plan collision retains
`public_release.plan_exists`, and inspection failure is content-silent. File
and hard-link publication keep their exclusive creation and no clobber
semantics. RFC-0043 makes no race-free filesystem claim and adds no workflow,
dependency, runtime API, release authority, rollback, or real public release
observation.

M61 keeps the expected candidate directory read-only by strictly resolving it
and the runner-owned output root before network or validator side effects. The
output root may not equal or resolve beneath the candidate directory; a
resolved alias receives the same stable `public_release.path_overlap` failure.
Filesystem-identity comparison across the output ancestry also catches aliases
whose resolved spelling differs on a case-insensitive filesystem. Resolution
or identity-inspection failures retain content-silent candidate or temporary-
directory codes, while a separate candidate child of the output root remains
valid. RFC-0044 makes no race-free filesystem claim and adds no workflow,
dependency, runtime API, release authority, rollback, or real public release
observation.

M62 constrains every public-release retrieval-plan asset to a portable asset
name: 1 through 255 allowed ASCII characters, no trailing period, no classic
Windows device stem, and no case-insensitive duplicate. An invalid plan fails
content-silently before asset download or creation of the asset output
directory. RFC-0045 uses no filesystem probing and adds no workflow,
dependency, runtime API, release authority, cleanup, or real public release
observation.

M63 confines subordinate stdout and subordinate stderr while the public
consumer runs its in-process validator and complete smoke. Success now emits
exactly one JSON document, and each subordinate must return an exact zero
integer; booleans, floats, integer subclasses, and custom comparison objects
fail content-silently. RFC-0046 relies on this verifier's single-thread utility
ownership and adds no workflow, dependency, runtime API, release authority, or
real public release observation.

M64 preflights staged sample bundles before extraction: at most 256 members,
1 MiB per member, and 8 MiB total declared expansion. Valid members stream in
64 KiB blocks and must reproduce their declared size. Only stored and deflated
ZIP members are admitted; BZIP2, LZMA, and unknown methods fail before
extraction. RFC-0047 adds no workflow, dependency, runtime API, cleanup
guarantee, release authority, or real public release observation.

M65 adds a portable sample member path policy to that complete preflight.
Relative paths contain at most 255 ASCII characters; each component uses the
existing portable ASCII grammar and excludes trailing periods and Windows
device stems. Exact/case-insensitive duplicates, case-ambiguous ancestors,
explicit directory entries, explicitly encoded non-regular file types, and
file/directory prefix collisions fail before extraction. ZIP members without
file-type mode bits remain compatible with common producers. RFC-0048 performs
no Unicode normalization or filesystem probing and adds no workflow,
dependency, sample-producer, runtime API, cleanup, release-authority, or real
public release observation claim.

M66 extracts admitted sample members beneath an owned same-filesystem temporary
staging directory and validates completeness there. The final sample root must
not already exist and becomes visible only through a single rename after the
staged tree is complete. Any pre-publication copy, validation, or rename failure
cleans the partial staging tree and leaves the final root absent. RFC-0049 adds
no workflow, dependency, runtime API, sample-producer, or release-authority
change; the visibility boundary is not crash-durable, provides no concurrent
filesystem race isolation, and is not a real public release observation.

M67 requires the exact sample-bundle inventory of 50 regular files after the
complete metadata/path preflight. Any unexpected member or missing member fails
with one content-silent category before extraction opens a member or creates a
staging directory. The expectation is source-defined independently of the
unchanged sample producer. RFC-0050 adds no workflow, dependency, runtime API,
sample-producer, or release-authority change; this is not content scanning, a
general archive sandbox, or a real public release observation.

M68 rejects an obvious non-regular or oversized bundle from path metadata,
opens an admitted bundle once, revalidates that its descriptor identifies a
regular file no larger than 16 MiB, and passes the same handle to `ZipFile`.
An oversized or non-regular container fails content-silently before ZIP parser
construction, central-directory parsing, member reads, or staging. RFC-0051
adds no workflow, dependency, runtime API, sample-producer, or release-authority
change; this does not replace expanded-size limits, make archive bytes
immutable, create a general archive sandbox, or establish a real public release
observation.

M69 rejects sample members whose ZIP general-purpose bit flags indicate
traditional encryption, strong encryption, or masked header values. The
content-silent rejection occurs in the complete metadata preflight before
member reads, password handling, or staging. RFC-0052 adds no password,
decryption support, workflow, dependency, runtime API, sample-producer, or
release-authority change; this is not a general archive sandbox or a real
public release observation.

M70 binds sample extraction to the digest already admitted from `SHA256SUMS`.
It hashes and rewinds the same opened handle before ZIP parsing and again after
member reads and completeness checks but before publication. A persistent
content-silent mismatch prevents publication and cleans owned staging. RFC-0053
adds no workflow, dependency, runtime API, sample-producer, or release-authority
change; it provides no immutable-input guarantee, is not a general archive
sandbox, and is not a real public release observation.

M71 copies the bounded sample source into one owned checksum-admitted snapshot.
The binary spooled temporary file receives at most 16 MiB while SHA-256 is
computed, and `ZipFile` parses those exact bytes after admission. Mismatch is
content-silent before ZIP parsing or staging. RFC-0054 adds no persistent copy,
workflow, dependency, runtime API, sample-producer, or release-authority change;
it is not a general archive sandbox or a real public release observation.

M72 confines the documented `BadZipFile` and `LargeZipFile` boundary around
that private parser. Archive-controlled parser diagnostics become one stable
error, the rendered exception uses suppressed context, and owned cleanup still
runs before control returns. RFC-0055 adds no workflow, dependency, runtime
API, or sample producer change; it is not a general archive sandbox or a real
public release observation.

M73 extends that same narrow boundary to `UnicodeDecodeError` raised while the
standard ZIP reader decodes archive-controlled UTF-8 names in the central
directory or local header. The stable error, suppressed context, and owned
cleanup contract remain unchanged. RFC-0056 adds no broad Unicode catch,
workflow, dependency, runtime API, sample producer, or release authority; it
is not a general archive sandbox or a real public release observation.

M74 extends the boundary with exactly `zlib.error` raised while reading a
checksum-admitted deflated member whose compressed payload is invalid. The
stable error, suppressed context, and owned cleanup contract remain unchanged.
RFC-0057 adds no EOF/filesystem/general catch, workflow, dependency, runtime
API, sample producer, or release authority; it is not a general archive
sandbox or a real public release observation.

M75 rejects ZIP general-purpose bit 5, compressed patched data, during the
existing all-member flag preflight. The exact content-silent policy error wins
before staging, inventory validation, or member reads; M69's encryption error
retains precedence when both indicators are present. RFC-0058 adds no broad
flag allowlist, workflow, dependency, runtime API, sample producer, or release
authority; it is not a general archive sandbox or a real public release
observation.

M76 rejects the central-directory ZIP general-purpose bit 4 exposed on
compression method 8 members during the same all-member preflight. PKWARE
reserves that combination for enhanced deflating. The exact content-silent
policy error wins before staging,
inventory validation, or member reads, while encryption and compressed-patch
checks retain their precedence. Stored members carrying bit 4 remain outside
this exact decision, as do local-header inconsistencies. RFC-0059 adds no broad
flag allowlist, workflow, dependency, runtime API, sample producer, or release
authority; it is not a general archive sandbox or a real public release
observation.

The M9 Box2D probe is also evaluation tooling, not a normal quality command or
dependency. Run it only in an isolated environment with an explicit candidate:

```console
uv run --no-project --python 3.12 --with box2d-python==0.1.2 python scripts/probe_box2d_candidate.py
```

A successful result establishes only bounded same-binary headless/lifecycle
smoke. It does not admit the binding or claim cross-platform determinism; see
[ADR-0024](docs/adr/0024-defer-box2d-v3-plugin-after-admission-review.md).

Repeat-build verification and release staging require new empty output
directories. The tag workflow is
defined for a future maintainer-created signed annotated `vVERSION` tag at an
exact `origin/main` commit. This repository task does not create a tag, publish
a GitHub release, configure a signing-key allowlist, or upload to PyPI.

## Contributing and project policy

Contributions use the [Developer Certificate of Origin](CONTRIBUTING.md), not a CLA. Start with the [first-contribution walkthrough](docs/first-contribution.md) and [roadmap board](ROADMAP.md). Please also read the [code of conduct](CODE_OF_CONDUCT.md), [security policy](SECURITY.md), [governance model](GOVERNANCE.md), and repository guidance in [MAINTAINERS.md](MAINTAINERS.md).

LudoWeave Engine is licensed under the [Apache License 2.0](LICENSE).
