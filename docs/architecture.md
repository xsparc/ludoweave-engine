# Architecture overview

## Product boundary

LudoWeave is designed around deterministic world operations. The ECS/world store is the only canonical runtime state. Human tools, tests, CLI adapters, replay, and software-agent adapters submit the same versioned, validated world commands and receive receipts.

M0 established lifecycle, time, error, rendering, packaging, and dependency contracts. M1-01 adds generational entity identity, M1-02 adds immutable component schemas and registries, M1-03 adds canonical world storage plus an independent reference model, M1-04 adds storage-neutral queries and local deferred structural commands, and M1-05 adds typed resources plus conflict-aware serial schedule planning.

M2 introduces `ludoweave.world` as the simulation-protocol layer. It may
depend on core and public ECS contracts, while application and tools may depend
on it. Persistent command envelopes are explicitly distinct from M1 local ECS
command buffers; see [the command protocol](commands.md) and ADR-0008.

M3 adds the isolated 2D presentation device. M4 adds provider-neutral platform
events, project-confined content-addressed assets, bounded deterministic 2D
collision, minimal audio ownership, and the ECS-backed Clockwork Arena sample.
See [the M4 gameplay vertical slice](gameplay.md).

M5 adds `ludoweave.agent` as a transport-independent typed observation and
control service over the existing world protocol. Python, the project-confined
CLI, and the local stdio MCP adapter all reach the same transaction service and
receipts. See [the agent control interface](agent-control.md).

M6 hardens distribution and contribution surfaces without adding another
runtime subsystem. Deterministic release tooling consumes built artifacts;
public stability metadata describes exact exports; user, adapter, triage, and
release guides document the existing boundaries. Release files and workflows
never become canonical world input.

M7 profiles the inherited M1/M3 target misses and retains the pure-Python
boundary. Query/extraction/packing optimizations preserve detached ownership
and backend-neutral bytes. No native module, compiler, NumPy storage, or new
runtime dependency is introduced. See
[RFC-0001](rfcs/0001-defer-first-native-kernel.md) and ADR-0022.

M8 adds standardized gamepad input without changing the authority boundary.
Engine-owned connection, button, and axis values map into the existing
tick-indexed action snapshots. The optional wgpu adapter polls its already
pinned GLFW provider; the Null device remains empty and headless. ADR-0023
defers an SDL3 adapter until its Python binding, binary delivery, ownership,
and cross-platform conformance meet explicit gates.

M9 evaluates the current Box2D v3 Python candidate and defers admission. The
evaluation script is repository tooling, not an engine dependency or adapter.
The base lock and package remain pure Python. ADR-0024 records failed and
incomplete wheel, stability, ownership, threading, determinism, conformance,
and maintenance gates.

M10 adds an owned local inspector process over the existing MCP tools. It keeps
no canonical state and emits only detached semantic observations, receipts,
and diffs after verifying exact authority-hash continuity. See the
[live semantic inspector](inspector.md) and ADR-0025.

M11 adds bounded headless-first rich 2D authoring without another world store.
Tick animation, bitmap text, immutable tilemaps, and fixed-point particles live
in `ludoweave.presentation` and translate only into existing backend-neutral
render records. Audio gains use an immutable mix graph validated by the Null
adapter; no real audio provider is admitted. See the
[presentation guide](presentation.md) and ADR-0026.

M12 adds a preview data-only plugin manifest and compatibility layer. It
canonicalizes inert declarations and checks explicit environment, policy, and
dependency facts without discovering, importing, installing, or executing
plugin code. CLI filesystem access stays in tools. See the
[plugin guide](plugins.md) and RFC-0002.

M13 evaluates existing snapshot/replay readiness from a dependency-free
example. It proves bounded local correction branches and exact immutable
lineage, then records that tick input remains an external replay dependency.
No runtime package, persistent protocol change, listener, or remote authority
is added. See the [rollback-readiness guide](rollback-readiness.md) and
ADR-0027.

M14 retains the layered-2D product boundary after an exact installed-surface
audit. M15 retains the finite headless inspector after confirming one real
receipted semantic mutation. Both milestones add decision evidence only and
introduce no runtime provider or second authority.

M16 treats executable WebAssembly mods as a separate security workstream. It
retains the M12 inert manifest boundary and adds only a threat model, installed
evidence, exact artifact validation, and architecture guards. There is no WASM
runtime, loader, guest ABI, WASI context, host call, public export, dependency,
or canonical guest state. See the [WASM-mod security
decision](wasm-mod-security-decision.md) and ADR-0030.

M17 adds a reusable installed behavioral profile over the existing
`RenderDevice` protocol. Callers explicitly construct trusted adapters; the
engine runner imports no backend and returns only frozen, sanitized evidence.
See the [render-device conformance guide](render-device-conformance.md) and
ADR-0031.

M18 adds the corresponding installed behavioral profile over the existing
12-tool `AgentCommandService`. Callers explicitly construct trusted adapters;
the engine runner imports no transport or provider and returns only frozen,
sanitized evidence. See the [agent-tool conformance
guide](agent-tool-conformance.md) and ADR-0032.

M19 adds the installed behavioral profile over the existing storage-neutral
`WorldStore`. Callers explicitly construct trusted implementations with the
runner's immutable fixture registry; the runner selects or references no
concrete implementation and returns only frozen, sanitized evidence. See the
[WorldStore conformance guide](world-store-conformance.md) and ADR-0033.

## Dependency direction

The active packages follow these rules:

```text
composition roots  ludoweave.tools, examples
                          |
inspector parent   tools.inspector --stdio--> tools.mcp child

agent service      ludoweave.agent ----> world/runtime   ludoweave.world
                         |
                         +--------------> core contracts ludoweave.core
agent evidence     ludoweave.agent.conformance ---> agent service/contracts

application        ludoweave.app ----> world/runtime   ludoweave.ecs
                         |                    |
ecs evidence       ludoweave.ecs.conformance ---> ECS contracts/WorldStore
render contracts   ludoweave.render.api/device/contracts/extraction
render evidence    ludoweave.render.conformance ---> render contracts/device
                         |                    |
core contracts     ludoweave.core <----------+

concrete adapters  ludoweave.render.backends.null[_device]
                   ludoweave.render.backends.wgpu (optional exact module)

focused contracts  ludoweave.platform, assets, collision, audio
presentation       ludoweave.presentation ---> render contracts/extraction
plugin contracts   ludoweave.plugins ---> core version/errors + canonical JSON

sample composition ludoweave.samples.clockwork_arena
                   ludoweave.samples.agent_world_builder
```

- `ludoweave.core` imports only the Python standard library.
- `ludoweave.ecs` may depend on core errors but not application, rendering, tools, or concrete backends.
- ECS conformance may depend on standard-library value helpers, core errors,
  and public ECS contracts only. It cannot import the concrete `World` or
  `ReferenceWorld` names or the private storage module, discover/select
  implementations, or use filesystem/process/network modules.
- `ludoweave.world` may depend on core and public ECS contracts but not application, rendering, tools, or backend packages.
- `ludoweave.agent` may depend on core and world contracts but not application, rendering, tools, samples, or concrete backends. Its conformance module may use only those same agent/core/world contracts and standard-library value helpers; it cannot discover or select adapters.
- Render contracts, handles, extraction, and graphs may depend on core errors but not application, tools, world, ECS storage, or concrete backends.
- Render conformance may depend on public render/platform/core contracts but
  never concrete backends, plugin discovery, filesystem/process/network
  facilities, or provider packages.
- Platform, asset, collision, and audio contracts depend only on their own package and core errors. Render adapters may emit engine-owned platform events.
- Presentation authoring may depend on core plus exact render contracts,
  extraction records, and opaque handles. It may not import ECS/world,
  application/tools, samples, concrete backends, or third-party providers.
- Plugin contracts may depend on core version/errors and world canonical-JSON
  helpers only. They may not import application/tools, ECS authority, samples,
  backends/providers, discovery/package metadata, process, or network modules,
  and may not evaluate Python.
- No engine module may import a WASM runtime. A future guest adapter must be an
  explicitly admitted, engine-owned boundary whose values are copied and whose
  world mutations use commands and receipts; runtime/guest objects may never
  enter public or canonical state.
- Concrete render backends may import the render API and core contracts.
- `ludoweave.app` composes core contracts, public ECS/runtime contracts, and the `RenderBackend` protocol, never a concrete backend. ECS never imports application implementations.
- `ludoweave.tools` and examples are composition roots and may select `NullRenderBackend`.
- MCP exists only as a local stdio composition adapter in `ludoweave.tools.mcp`; it may not import networking modules or implement a listener.
- The inspector exists only in `ludoweave.tools.inspector`; it may launch the built-in MCP composition, retain detached JSON plus one prior snapshot for a diff, and must not import networking modules or evaluate Python.
- The package root may re-export the deliberately small application API but never a concrete backend or third-party native object.
- Only `ludoweave.render.backends.wgpu` may import wgpu, rendercanvas, or GLFW.
  SDL/PySDL3 remains forbidden until ADR-0023's adapter gate is accepted by a
  superseding decision. NumPy storage and future native extension objects are
  forbidden from engine source and public APIs.

The M2 CLI keeps filesystem policy in `ludoweave.tools`. Its data-only
headless-project manifest cannot name Python modules or callables, and every
artifact path is resolved beneath the explicitly selected project root before
bounded I/O. World, snapshot, replay, ECS, and application packages remain
path- and transport-agnostic.

These rules are enforced by an AST-based test over the source tree. The test also analyzes a generated invalid fixture so a broken checker cannot silently pass.

The M5/M10 architecture checks additionally reject upward agent imports,
Python-evaluation primitives in the agent package and inspector, and networking
modules in both local stdio adapters. Agent tools expose provider-neutral JSON
documents, not filesystem, ECS-storage, or GPU objects.

The M12 checks reject discovery, import/execution, installation/process, and
network facilities from `ludoweave.plugins`. Manifests contain no implementation
locator, and no positive compatibility report mutates or composes runtime state.

The M13 evidence composition lives under `examples/` and imports existing
application, sample, and world contracts. Its validator is repository tooling.
Neither is a runtime dependency, and architecture checks continue to prohibit
network facilities from local stdio/inspector boundaries and provider objects
from canonical state.

The M16 evidence composition also lives under `examples/`; its validator is
repository tooling. The AST checker explicitly rejects common WASM runtime
imports even inside plugin contracts, while exact dependency tests keep both
the baseline and graphics-extra requirement sets unchanged.

The M17 installed runner lives with render contracts and accepts only an
explicit callable factory. Concrete adapter selection remains in examples or
external composition roots. Its report is presentation evidence and cannot
enter canonical world state or establish plugin trust.

The M18 installed runner lives with agent contracts and accepts only an
explicit callable factory. Adapter/transport selection remains in examples or
external composition roots. The runner imports no tools, samples, rendering,
plugin, provider, filesystem, process, network, discovery, or package-loading
module. Its report is detached diagnostic evidence and cannot enter canonical
world state or establish provider trust.

The M19 installed runner lives with ECS contracts and accepts only an explicit
`factory(ComponentRegistry)`. Implementation selection remains in examples or
external composition roots. The runner imports neither `World` nor
`ReferenceWorld`, concrete storage, persistence, tools, plugins, providers,
filesystem, process, network, discovery, or package-loading modules. Its report
is detached evidence and cannot become canonical state or admit storage.

## Ownership and close order

An `Engine` receives a clock and render backend by dependency injection. The engine owns the backend after construction and closes it exactly once. It does not own or close the clock because clocks hold no external resources in M0.

Normal close order is:

1. Stop the active run loop.
2. Close the render backend.
3. Mark the engine closed even if backend cleanup raises.
4. Surface a structured cleanup failure with the original exception chained.

Initialization failure enters a transient failed state, attempts backend cleanup, and leaves the engine closed before returning the structured error.

## State and determinism boundary

`World` is the sole canonical owner of live entity and component state. It owns a generational allocator and private component tables. Values are copied and validated at public boundaries; external aliases cannot mutate canonical state. Public inspection sorts entities and component records independently of private dense history. Component UUIDs and versions are persistent identity, while qualified Python names are diagnostic aliases.

World, structural, table-structural, and component-change epochs derive only from successful logical mutations. Swap relocation is an implementation detail and does not mark the moved row as changed. Failed operations do not advance epochs. `ReferenceWorld` duplicates behavior using dictionaries and is prohibited from depending on the production allocator or dense/sparse implementation.

Queries expose detached component values, never canonical table objects. Read-only query changes are discarded. Writable rows use explicit context-managed ownership, validate a complete row before writeback, and advance one epoch for all changed components in that row. Direct mutation and command flushing are forbidden while a query cursor is active. Stable order is opt-in; native query order is private and must not enter authoritative logic.

Local `Commands` buffers copy values at enqueue time and identify deferred spawns with exact buffer-generation tokens. Flush applies operations to a clone and adopts it only after complete success. These in-process buffers and their `FlushResult` are not the persistent, versioned commands, transactions, and receipts reserved for M2.

Persistent M2 transactions instead target a single-owner `WorldSession`.
World, resources, and completed ticks are cloned and operated on as one staged
record, then adopted with one pointer assignment only after complete success.
Public world, resource, and random accessors return detached copies; mutating
those views cannot bypass the persistent command/receipt boundary. Internal ECS
checkpoint ports are private to engine-owned world services.
The authority image includes allocator/free-list and epoch state, explicit
codec-backed state resources, completed ticks, and engine-owned named random
streams. Application tick execution
is dependency-injected through a world-owned protocol and can run only against
staged world, resources, and random state; the world layer never imports
application code. Canonical snapshots rebuild this complete record before one
safe-point adoption, preserving future allocation, changed-query, and random
behavior without persisting private storage layout.

Every resource in a `WorldSession` has exactly one explicit `STATE`, `INPUT`,
or `RUNTIME_EXCLUDED` role. M2 persistent tick commands advance exactly one
tick and are accepted only for state-only resource compositions. This makes
every recorded tick a replay/branch boundary and prevents unrecorded input or
runtime values from influencing M2 replay. M4 gameplay composition injects an
immutable tick-indexed action source into the staged executor; replay callers
must inject the equivalent recorded snapshots, and checkpoint hashes detect any
divergence. Input resources themselves remain outside persistent ticks until a
future command/replay codec explicitly embeds them. Snapshot load replaces
state resources while preserving destination-owned input/runtime resources.
M2 `WorldSession` registries reject presentation schemas entirely and accept
canonical authoritative components only; presentation components are not
coerced into the authority hash. M3 owns presentation extraction. A later
mixed authoritative/presentation composition must define a separate
excluded-state store and reconstruction boundary before renderer integration.

Resource keys are explicit composition-owned identities; registries and stores are never global. Resource stores copy values through per-key adapters at every public boundary. Adapters are trusted read-only-input copy functions; objects that cannot be copied without mutation, I/O, external state, or retained aliases are excluded from deterministic storage. System declarations are immutable metadata on module-level synchronous functions. The scheduler validates registered component/resource access, deterministic eligibility (including rejection of D0 component access in deterministic-required plans), same-phase dependencies, and write conflicts, then produces an input-order-independent serial plan without invoking application code. Fixed phases resolve cross-phase conflicts; same-phase conflicts require an explicit direct or transitive path. Python concurrency and non-Python execution classes are rejected in M1.

`FixedStepApplication` is the single active mutation owner of its injected world and resources. Integer accumulator units preserve rational tick boundaries, catch-up backlog is retained, and immutable tick-indexed input is published as an explicit resource. Invocation-scoped query, resource, and command facades enforce declared access for normal system code. PRE/SIM commands share one buffer flushed before POST. Presentation occurs once per pump and cannot feed authoritative state. Tick failure is nontransactional until M2.

Entity slot reuse is deterministic for a given operation sequence, generation counters never wrap, and registry enumeration is UUID-sorted. Tick number and virtual time remain deterministic control values. Presentation frame counts, monotonic samples, diagnostics, logs, and platform metadata are not authoritative simulation state and must not become inputs to future state hashes.

Fixed deadlines are derived from the initial time and tick number rather than accumulated rounded deltas. This makes a virtual run repeatable and prevents rounding error from compounding.

## Backend isolation

`RenderBackend` is owned by the M0 engine lifecycle, while M3's
`RenderDevice` owns resource creation, submission, fences, capture, and
destruction. Both are engine protocols; neither creates a global singleton.
The Null implementations validate lifecycle, resource generations, command
targets, pipeline/texture use, graph hazards, and deferred destruction without
graphics libraries.

The optional production device lives only in
`ludoweave.render.backends.wgpu`. Its provider imports and native objects do
not enter package roots, application configuration, ECS/world state, command
protocols, snapshots, replay, or captures. Composition roots explicitly
select it. Provider capture arrays are immediately normalized to immutable
RGBA bytes. Exact dependency pins and upgrade gates are recorded in ADR-0015.

M3 presentation frames are immutable copies outside `WorldSession`. They may
interpolate previous/current transforms and carry a camera, layers, tiles, and
debug records. They identify a completed tick for diagnostics but cannot be
serialized by the canonical authority codec and cannot affect hashes or
future commands. Draw lists name an explicit target and camera matrix. Scoped
generational handles are retired logically at once and destroyed physically
only after their last referencing fence completes. See the
[rendering contract](rendering.md) and ADR-0013.

Render graphs use explicit reads, writes, dependency paths, and transient
first/last passes. Stable topological compilation rejects cycles,
read-before-write, lifetime escapes, and unordered writer hazards before any
GPU submission. Physical transient allocation/aliasing is deferred.

## M4 gameplay boundary

Clockwork Arena is a composition root over `WorldSession`; it does not create a
parallel gameplay store. Each fixed tick is a received `world.tick` command and
receipt. The tick kernel mutates only staged ECS components, the staged Arena
state resource, and staged named random streams. Live and replay kernels receive
equivalent immutable action snapshots.

Asset cache payloads, audio handles, window events, render handles, and
presentation frames remain outside canonical state. Logical asset URIs and
action values may be recorded, but provider/native objects may not. Collision
uses copied scalar values and returns deterministic sorted IDs.

## M5 agent-control boundary

`AgentCommandService` observes detached authority documents and submits
mutations only through the existing versioned command protocol. It never owns a
parallel world. Read is implicit; write, capture, and registered-test access are
separate immutable capabilities disabled by default. Requests, results,
transactions, query counts, ticks, snapshots, captures, tests, and rate are
bounded, and credential-shaped diagnostic values are redacted.

The constructing thread owns the service. Mutations use a non-blocking gate and
reject wrong-thread or reentrant access. Each requested tick is one atomic,
receipted transaction; a multi-tick request is a sequence of safe points rather
than one atomic batch. The service owns and closes its optional capture provider
but does not own the session, clock, telemetry provider, or test provider.

The MCP adapter implements a small local-only stdio subset. It has no remote
listener, HTTP transport, authentication claim, dynamic import, shell access,
or arbitrary evaluation. The Agent World Builder remains a trusted sample
composition root whose canonical room objects live in the ECS/world store.

## M7 performance boundary

Profiler output is engineering evidence, not canonical state or a runtime API.
The repository-only profiling tool imports benchmark composition helpers; the
engine package does not depend on benchmarks. Artifacts normalize code
locations to module names and never record workspace paths or environment
values.

The remaining ECS cost traverses detached Python component records for
validation, copying, mutation detection, and writeback. The remaining
extraction cost constructs immutable presentation records. Sprite packing has
an owned `bytes` output, but its input remains nested Python objects that cannot
be read by a native loop while releasing the GIL. These are not admitted native
boundaries. A later proposal must first establish an internal contiguous scalar
batch without exposing storage or native objects through public APIs.

## M8 gamepad boundary

Gamepad providers own polling and native state. Public events contain only a
bounded logical player slot, a standardized engine enum, and an exact normalized
value. Polling is ordered by slot, then button, then axis for every control the
provider can represent without ambiguity; connection loss clears all state for
that slot. Focus loss suppresses live controls until focus and a current state
sample return. A provider must omit an indeterminate control rather than
synthesize an active value.

Action-map deadzones and scales are presentation/input policy. They become
simulation-relevant only after mapping into an immutable `InputSnapshot` for an
exact tick. Raw provider events, device names, GUIDs, mapping databases,
timestamps, haptics, and hardware capabilities are non-canonical and are not
serialized into world snapshots, commands, receipts, or replay headers.

## M9 external-physics boundary

An external solver cannot become a second canonical world. A future adapter
may receive copied engine-owned descriptors only at explicit safe points and
may return copied observations or command proposals. Provider bodies, shapes,
contacts, callbacks, allocators, pointers, and snapshots cannot enter public
APIs, ECS records, commands, receipts, authority snapshots, or replays.

External physics is D0 by default. Same-process repeated traces do not prove
cross-platform determinism, rollback, snapshot/restore, contact ordering, or
upgrade compatibility. A stronger classification needs exact provider-version
identity and cross-platform snapshot/replay/hash conformance. Explicit close,
failure reconciliation, bounded work, and single-owner threading must be
exercised before a runtime protocol is introduced.

The M9 candidate probe lives under `scripts/`, imports no LudoWeave module, and
loads the candidate only from an isolated caller environment after matching the
resolved module file to the distribution's installed-file inventory. A shadow
module fails before import and is never attributed to the candidate version.
Engine source imports of Box2D names are architecture violations. See
[ADR-0024](adr/0024-defer-box2d-v3-plugin-after-admission-review.md).

## M10 inspector boundary

The inspector parent owns exactly one child launched through the current
interpreter, its three pipes, and its bounded shutdown. It cannot accept an
executable, shell command, dynamic module, remote endpoint, process ID, or
provider selection. The child owns the live `AgentCommandService` and canonical
`WorldSession`; the parent owns only detached JSON documents and one ephemeral
snapshot string used to request the next semantic diff.

Read access is the default. Every requested bootstrap or tick requires an
explicit write grant and crosses the existing transaction/tick safe point with
a receipt and optimistic hash. The inspector verifies MCP lifecycle, response
identity, typed tool discovery, transition commitment, completed ticks, and
snapshot/world/query/telemetry/diff hash continuity before emitting each
post-transition observation.

No observation contains the snapshot itself, a path, environment value,
process identifier, provider-native object, or mutable world alias. Service
telemetry and child lifecycle timing remain non-authoritative. The finite
caller-driven stream is not a visual editor, network transport, remote attach,
or wall-clock watcher. See [ADR-0025](adr/0025-owned-local-semantic-inspector.md).

## M13 rollback-readiness boundary

The existing replay branch is an immutable offline child timeline, not a live
rollback service. A composition root may replay a parent to an exact boundary,
construct a child recorder, and inject a different future `TickExecutor`, but
the recorded `world.tick` transactions do not own the action snapshots that
executor consumes. Equivalent tick input must be supplied independently or
checkpoint verification diverges.

Canonical input history, full/delta correction envelopes, peer authority,
sequence/acknowledgement/reorder semantics, transport security, abuse limits,
loss/latency simulation, and bounded catch-up budgets remain absent. No socket,
listener, remote attach, replication store, or background authority is
authorized by a successful local proof. ADR-0027's complete gate must be
superseded before those boundaries change.

## M14 constrained-3D boundary

Layered 2D is the accepted rendering and product boundary. The public engine
owns an orthographic `Camera2D`, color-only texture and pipeline descriptors,
a 2D texture limit, and sprite/tile/debug extraction records. Array texture
layers, draw ordering, parallax, and presentation layers do not establish a
third spatial axis. The built-in sprite shader uses fixed presentation depth,
and no command operation gives an external actor 3D world semantics.

WebGPU depth/stencil and 3D-coordinate capability remains behind the optional
adapter boundary. Provider capability cannot enter core/application APIs or
become canonical state without an engine-owned contract that Null/headless
execution can validate. The M14 composition-root evidence inspects the
installed public descriptors and operation registry; it neither imports a
provider nor adds an authority format.

Architecture tests close source imports to the standard library and
engine-owned modules, except for the exact existing wgpu/rendercanvas/GLFW
imports inside the one adapter. They also lock the exact public render exports,
descriptor fields, positive orthographic camera/layer ordering, fixed-depth
shader, and absence of a 3D runtime module. A superseding proposal must change
these guards intentionally only after satisfying the product,
spatial/asset/render, agent/replay, headless-conformance, cross-platform,
resource-budget, lifecycle, and maintenance gates together.

## M15 visual-editor admission boundary

The existing typed command/receipt protocols, twelve semantic tools, local
stdio MCP adapter, and owned inspector are necessary foundations for human and
agent authoring. They are not an editor contract. The agent surface remains
experimental, the inspector remains an internal finite composition, and no
document/scene, selection/hierarchy, undo/conflict, property metadata,
viewport/picking, asset-authoring, dirty-state recovery, accessibility,
desktop packaging, or operational-budget contract exists.

M15 therefore composes installed facts only under `examples/` and validates
their exact deterministic JSON from source, the isolated pure wheel, and the
release sample bundle. It adds no engine module, API, persistent format,
dependency, lock change, toolkit, background process, or CI job. Architecture
checks reject standard-library GUI/TUI/browser-launch imports in engine source;
the existing closed external-import policy rejects third-party GUI frameworks.
Editor-named runtime modules and root exports remain absent.

Any future editor must preserve one ECS/world authority, use versioned commands
and receipts for every mutation, and retain a headless Null conformance path.
ADR-0029 requires the complete product, compatibility, authoring, recovery,
accessibility, packaging, performance, and ownership gate before these guards
may change.

## M16 WASM-mod security boundary

The WebAssembly core sandbox provides no ambient host access, but LudoWeave as
embedder would define every imported capability. A future guest therefore
cannot receive filesystem, network, process, environment, clock, randomness,
render/audio, persistence, or world authority implicitly. Guest values must be
copied and validated, and every world mutation must cross the existing staged
command/transaction path and produce a receipt. Guest memory, runtime handles,
compiled modules, and host-function objects cannot enter public APIs or
canonical state.

M16 implements none of that execution surface. It audits the installed inert
manifest contract from a dependency-free example, validates the exact document
from source/wheel/release artifacts, and adds synthetic AST fixtures rejecting
common WASM runtime imports. The baseline remains a universal pure-Python wheel
with only the existing optional graphics extra.

ADR-0030 requires complete capability, resource, determinism, trap/lifecycle,
persistence, isolation, adversarial-conformance, cross-platform,
supply-chain, and maintenance evidence before these guards may change. Core
memory isolation or a successful guest prototype is insufficient.

## M17 installed adapter-conformance boundary

The first reusable conformance profile targets the existing `RenderDevice`
contract because it is shared by the Null reference and production wgpu
adapter. A caller explicitly supplies a trusted factory. The runner imports no
concrete backend and performs no discovery, module lookup, installation,
filesystem access, subprocess launch, networking, or global registration.

Each run owns one device on the calling thread, uses only engine descriptors,
handles, commands, events, capabilities, captures, and structured errors, and
closes the device twice before probing use-after-close. Versioned reports
contain stable check status/error codes but no exception messages, paths,
environment values, timing, capture bytes, or provider-native objects.

Conformance is a behavioral self-test, not trust or admission. Provider code
runs in-process and can still block, crash, consume resources, or exercise
ambient authority. Security, provenance, full OS/Python support, performance,
device loss, and maintenance remain separate evidence gates. The M12 manifest
stays inert and cannot name a factory. See
[ADR-0031](adr/0031-explicit-installed-render-device-conformance.md).

## M18 installed agent-tool-conformance boundary

The second reusable conformance profile targets the existing
`AgentCommandService` contract. A caller explicitly supplies a trusted factory
for one fresh, clean, fully capable adapter. The runner performs no discovery,
module lookup, installation, filesystem access, subprocess launch, networking,
or global registration.

One adapter is invoked synchronously on the caller thread. The fixed profile
checks exact tool discovery and capabilities, detached reads, baseline
snapshot/hash consistency, dry-run and committed receipts, stale-hash
atomicity, entity query, per-tick receipts, semantic diff, capture/test/
telemetry result shapes, idempotent close, and structured use-after-close
rejection. All world mutations continue through the existing canonical
commands and receipts.

Reports contain fixed statuses and runner-owned codes, never provider
messages/codes, paths, environment or platform metadata, timing, snapshots,
captures, entity values, credentials, or provider-native objects. The runner
attempts cleanup after interrupted stages but cannot contain malicious code.

Conformance is a behavioral self-test, not provider trust or admission.
Transport security, provenance, complete OS/Python support, performance,
free-threaded behavior, maintenance, and real-agent manual-recovery rates
remain separate evidence gates. The project-owned direct-service pass is
reference evidence; external adoption remains zero until independently
authored evidence is reviewed. See
[ADR-0032](adr/0032-explicit-installed-agent-tool-conformance.md).

## M19 installed WorldStore-conformance boundary

The third installed profile targets the existing public `WorldStore` contract.
A caller explicitly supplies a trusted `factory(ComponentRegistry)`. The runner
creates one immutable fixture registry, invokes the factory once on the calling
thread, and requires the returned store to retain that exact borrowed registry
identity. It performs no discovery, module lookup, installation, filesystem
access, subprocess launch, networking, or global registration.

The fixed profile checks deterministic entity generations, world/component
epochs, detached value ownership, query order/change/writeback and lifecycle,
atomic retryable local command buffers, independent state/allocator cloning,
and structured failure atomicity. Canonical state remains solely in the tested
store; the runner produces only detached status evidence.

Reports contain fixed statuses and runner-owned codes, never provider
messages/codes, paths, environment/platform metadata, timing, component/entity
values, storage layout, credentials, or native objects. The current in-memory
`WorldStore` protocol has no `close()` method, so the runner performs no cleanup
call and excludes stores requiring external-resource ownership.

Conformance is a behavioral self-test, not provider trust, certification, or
admission. Provenance, complete OS/Python support, performance, persistence,
free-threaded behavior, external-resource recovery, and maintenance remain
separate evidence gates. The project-owned `World` and `ReferenceWorld` passes
are references; independent adoption remains zero until separately authored
evidence is reviewed. See
[ADR-0033](adr/0033-explicit-installed-world-store-conformance.md).

## M20 command/receipt stability boundary

M20 evaluates compatibility readiness without adding a second command layer or
changing the existing one. Its installed example composes only public
`ludoweave.world`, ECS, sample, and agent-conformance APIs. It creates one
in-memory authority, exercises canonical decode, dry-run, commit, stale-hash,
unsupported-hash, and failed-batch behavior, and then runs the existing M18
twelve-check profile against a separately owned fresh authority.

The evidence reports protocol/status/error identities, field and operation
names, boolean relationships, stability labels, and package version. It omits
authority hashes and values, entity/component values, snapshots, captures,
paths, environment/platform facts, timing, credentials, and provider messages.
It performs no discovery, dynamic import, installation, filesystem access,
subprocess launch, networking, registry mutation, or backend composition.

RFC-0003 retains the command, transaction, and receipt surfaces as
experimental. The evidence confirms strong same-version canonical and atomic
behavior but also records the absent public bounded receipt reader and the
missing cross-version corpus, external feedback, operation/diff/diagnostic
evolution rules, and supported deprecation-capable release channel. A future
promotion must satisfy the complete gate in one assigned decision; it cannot be
inferred from a green same-version test or project-owned adapter pass.

## M21 receipt-reader boundary

M21 adds one engine-owned decoding edge inside `ludoweave.world`. It accepts a
decoded JSON-domain object or bounded UTF-8 JSON, applies canonical limits
before domain construction, validates the exact existing receipt/1 graph, and
returns only immutable backend-neutral value objects. It calls no operation
handler and has no reference to a `WorldSession`, registry, provider, tool,
filesystem, process, or network surface.

The parser depends downward on canonical JSON, command attribution, receipt
value types, semantic-diff records, and structured world-protocol errors. No
application, CLI, tool, plugin, render backend, or optional dependency enters
the contract. `ReceiptLimits` makes byte/tree/string/outcome/diagnostic/alias/
diff work explicit; caller containers are recursively detached.

The repository freezes exact committed, dry-run, and rejected v1 documents
under a single-version fixture manifest. This creates immutable historical
inputs for a later version but does not itself prove cross-version behavior.
RFC-0004 keeps every new export experimental and versions M20's living
readiness evidence to `/2`, with only the reader gate true.

## M22 operation-argument policy boundary

M22 adds no engine module. Its machine-readable contract, installed example,
validator, and tests live outside `src/ludoweave`; runtime handlers do not load
or depend on them. The example composes public ECS/world contracts and fresh
in-memory authorities to exercise all seven built-in v1 operations plus exact
missing-required and unknown-field rejection.

Architecture tests require the frozen operation identities to match
`BUILTIN_OPERATION_SPECS`, require the example literals to match the fixture,
and reject filesystem, discovery, process, network, tool, plugin, and concrete-
backend imports from the evidence files. RFC-0005 versions the living readiness
evidence to `/3` and marks only the operation-policy and bounded-reader gates
true. No second runtime schema, operation registry, API, or canonical state is
introduced.

## M23 receipt-semantic policy boundary

M23 adds no engine module. Its machine-readable receipt-v1 contract, installed
example, strict validator, and tests remain outside `src/ludoweave`; the public
reader and transaction service do not load the repository fixture. The example
uses fresh in-memory authorities to exercise all semantic-diff record families,
status presence, current top-level rejection codes, fail-closed fields, and an
additive unknown-code fallback.

Architecture tests require every policy literal to match the exact fixture and
reject filesystem, discovery, process, network, tool, plugin, and concrete-
backend imports. RFC-0006 versions the living readiness evidence to `/4` and
marks the operation-policy, bounded-reader, and receipt-policy gates true. No
runtime API, receipt field, handler, provider, dependency, or canonical state
is introduced; cross-version history remains a separate false gate.

## M24 cross-version corpus admission boundary

M24 adds no engine module. One explicitly invoked example reads a selected
repository/release corpus manifest, verifies safe-basename child manifests and
receipts by exact byte length/SHA-256, and decodes the historical receipts only
through the installed bounded public reader. Runtime source never loads or
depends on the corpus.

The admission rule requires a reader version different from a preserved source
version, at least two distinct observed package versions, and supported-release
records for every observed version. The current deterministic report is
`not-ready`: source and reader are both `0.1.0a1`, and the supported-release set
is empty. The synthetic future-state regression proves only the Boolean gate
logic and cannot count as history.

Evidence reads are bounded and synchronous. Unsafe names, unknown fields,
duplicates, hash/byte drift, incomplete status coverage, release-record drift,
reader failure, and canonical drift fail closed. Reports omit paths, state
values/hashes, environment facts, timing, credentials, and provider messages.
There is no discovery, dynamic import, installation, subprocess, networking,
tag lookup, publication, provider selection, or retained external resource.

## M28 external sample-game adoption boundary

M28 adds no engine module. One explicitly invoked example reads a selected
reviewed manifest outside `src/ludoweave` and emits sanitized aggregate
readiness evidence. The runtime package never loads the manifest or evaluator.

Every future admitted record must describe an independently authored public 2D
or layered-2D game using an installed wheel and exercising headless fixed ticks,
typed command receipts, and verified replay. Human reviewers own authorship,
independence, public provenance, licensing, and outcome judgments. The evaluator
validates only frozen fields, exact identities, complete history, and resource
bounds. The current empty manifest deterministically reports zero external
sample games and `not-ready`; project samples and synthetic regressions cannot
change that result.

Reads are bounded, explicit, synchronous, and symlink-rejecting. Evidence code
uses no discovery, networking, remote lookup, dynamic import, installation,
subprocess, provider execution, telemetry, or retained resource. Reports omit
authors, repositories, revisions, artifact hashes, licenses, paths, platforms,
and timings. RFC-0011 adds no runtime API, canonical state, protocol, format,
dependency, lock, version, workflow, publication, or stability change.

## M29 contributor-retention boundary

M29 adds no engine module. One explicitly invoked example reads a selected
reviewed manifest outside `src/ludoweave` and emits sanitized aggregate
readiness evidence. The runtime package never loads the manifest or evaluator.

Every future admitted record must describe the same independently reviewed
external human completing a first and later return contribution to this
project. Both contributions require distinct public issues and merged pull
requests, exact Git and artifact identities, valid DCO, complete validation,
reviewed provenance, and canonical merge chronology. Human reviewers own
identity, independence, same-person continuity, chronology, and retention
judgments. The evaluator validates only frozen fields, complete history, and
resource bounds. The current empty manifest deterministically reports zero
retained contributors and `not-ready`; popularity metrics, project actors, and
synthetic regressions cannot change that result.

Reads are bounded, explicit, synchronous, and symlink-rejecting. Evidence code
uses no discovery, networking, remote lookup, dynamic import, installation,
subprocess, provider execution, telemetry, or retained resource. Reports omit
contributors, public references, revisions, artifact hashes, timestamps,
paths, platforms, and timings. RFC-0012 adds no runtime API, canonical state,
protocol, format, dependency, lock, version, workflow, publication, or
stability change.

## M30 installation-matrix boundary

M30 adds no engine module. One explicitly invoked example reads a selected
reviewed manifest outside `src/ludoweave` and emits sanitized aggregate
readiness evidence. The runtime package never loads the manifest or evaluator.

Every future admitted matrix must cover the exact supported practical
OS/CPython set with clean isolated installations of one immutable public
`py3-none-any` release wheel. Records bind canonical project release and asset
locations, wheel and installation-log SHA-256 identities, CPython patch and
platform values, dependency/compiler absence, the required installed checks,
and reviewed provenance and validation. The evaluator validates only frozen
fields, complete history, and resource bounds. The current empty manifest
deterministically reports zero successful environments and `not-ready`;
source-checkout CI, local builds, and synthetic regressions cannot change that
result.

Reads are bounded, explicit, synchronous, and symlink-rejecting. Evidence code
uses no discovery, networking, remote lookup, dynamic import, installation,
subprocess, provider execution, telemetry, or retained resource. Reports omit
release/asset locations, Python patch versions, platforms, log identities,
timestamps, paths, hosts, and timings. RFC-0013 adds no runtime API, canonical
state, protocol, format, dependency, lock, version, workflow, publication, or
stability change.

## M31 response/review-latency boundary

M31 adds no engine module. One explicitly invoked example reads a selected
reviewed manifest outside `src/ludoweave` and emits sanitized aggregate
measurement-readiness evidence. The runtime package never loads the manifest
or evaluator.

Every future admitted window must cover the complete reviewed public cohort of
eligible external-human issues and pull requests opened during its bounded
interval. Records preserve pending items and bind first qualifying public human-
maintainer actions to canonical project locations, exact UTC timestamp/latency
agreement, frozen source/review identities, and reviewed eligibility,
provenance, validation, maintainer status, and participant distinctness. Public
census and review artifacts share one immutable project revision. The evaluator
validates only frozen fields, aggregate calculations, complete history, and
resource bounds. The current empty manifest deterministically reports zero
windows and measurements and `not-ready`; automation, project history, and
synthetic regressions cannot change that result.

Reads are bounded, explicit, synchronous, and symlink-rejecting. Evidence code
uses no discovery, networking, remote lookup, dynamic import, installation,
subprocess, provider execution, telemetry, contributor contact, issue/PR
mutation, or retained resource. Reports omit resource/action locations,
timestamps, identities, per-record hashes, paths, hosts, private data, and raw
evidence. RFC-0014 adds no runtime API, canonical state, protocol, format,
dependency, lock, version, workflow, publication, stability, SLA, or support
change.

## M32 replay-divergence-rate boundary

M32 adds no engine module. One explicitly invoked example reads a selected
reviewed manifest outside `src/ludoweave` and emits sanitized aggregate CI
replay-divergence-rate readiness evidence. The runtime package and CI workflow
never load the manifest or evaluator.

The evaluator accepts only bounded exact-schema data. A future window must
contain the complete reviewed public cohort of eligible CI replay executions
that started in its interval. Each execution binds canonical project workflow
run/job locations, an exact head revision, immutable workflow and test sources,
and a frozen result artifact. Outcomes are exactly `verified`, `diverged`, or
`not-executed`. Verified outcomes require equal expected/actual hashes;
divergence requires distinct hashes, the first divergent tick, and
`world.replay.diverged`; non-execution carries no replay hashes/tick and
retains a bounded cancellation, early-failure, skip, or unavailable-result
reason. Eligibility is fixed before outcomes: it covers replay-verification
cases expected to reproduce canonical state with hash verification enabled and
excludes intentionally divergent negative fixtures and verification-disabled
diagnostics. An actual divergence in an eligible case remains counted. Human
review owns cohort completeness, eligibility, outcome, provenance, and
validation.

Only the exact reviewed manifest and complete mandatory history can expose
admitted counts. A rate requires at least one execution and no non-executed
case, and is emitted only as an exact integer numerator/denominator pair. The
current 175-byte manifest contains no windows, so the deterministic result is
`not-ready`, no divergence rate is exposed, and a passing CI job is not treated
as zero divergence. Reports omit run/job URLs, revisions, timestamps, case
names, state hashes, artifacts, paths, environment values, and raw logs.

M32 does not query GitHub, collect telemetry, execute providers, or change
runtime source, replay behavior, public exports, formats, protocols,
dependencies, lock, version, workflows, CI topology, publication, stability,
reliability targets, or support policy.

## M33 benchmark-regression-rate boundary

M33 adds no engine or benchmark module. One explicitly invoked example reads a
selected reviewed manifest outside `src/ludoweave` and emits sanitized
aggregate benchmark-regression-rate readiness evidence. The runtime package,
benchmark scripts, and CI workflow never load the manifest or evaluator.

A future window must contain the complete reviewed controlled cohort of
eligible paired comparisons that started in its interval. The evaluator
registers only the existing M1-M4 `time.perf_counter_ns` workloads and exact
`p95_ns`; M7 cProfile documents remain diagnostic attribution evidence. Each
comparison binds distinct base/head revisions, both exact benchmark sources,
the candidate workflow source, one frozen runner profile, an environment
profile, a predeclared integer basis-point tolerance, and frozen result
artifacts. Human review owns runner control, parameter equality, eligibility,
comparability, threshold predeclaration, outcome, provenance, validation, and
census completeness.

Outcomes are exactly `stable`, `regressed`, or `not-executed`. Executed results
require positive base/candidate p95 values and complete artifacts; their
classification is exact integer arithmetic, with equality at the tolerance
boundary stable. Non-execution carries no timing artifacts and retains a
bounded cancellation, pre-benchmark failure, skip, or unavailable-evidence
reason. Only exact reviewed manifest identity and complete mandatory history
expose admitted counts. A rate additionally requires a non-empty cohort with
no non-executed comparison and is emitted only as an integer numerator and
denominator.

The current 199-byte manifest contains no windows, so the deterministic result
is `not-ready` and no comparison count or regression rate is exposed. Reports
omit run/job URLs, revisions, timestamps, workload names, tolerances, timings,
runner/environment details, artifacts, paths, and raw logs. M33 changes no
runtime/benchmark implementation, optimization, API, format, dependency,
lockfile, version, workflow, telemetry, provider, native/WASM boundary,
publication, performance target, reliability promise, or support policy.

## M34 agent-tool recovery-rate boundary

M34 adds no engine or agent module. One explicitly invoked example reads a
selected reviewed manifest outside `src/ludoweave` and emits sanitized
aggregate recovery-rate readiness evidence. The runtime package and agent
service never load the manifest or evaluator.

A future window must contain every dispatched call from a complete reviewed
cohort of eligible task-directed software-agent sessions. Calls are restricted
to the exact 12 names in `ludoweave.agent.service/1` and bind immutable service-
contract, dispatch, terminal-result, and recovery evidence. Synthetic fixtures,
conformance runs, benchmarks, CI contract exercises, maintainer-invoked calls,
and unreviewed/private sessions are ineligible. Human review owns session and
call eligibility, census completeness, task context, manual-recovery status,
outcome, provenance, and validation.

Outcomes are exactly `completed-without-manual-recovery`,
`completed-after-manual-recovery`, `not-completed`, or `terminal-unobserved`.
Known failures remain in the denominator. Missing terminal evidence remains
counted and blocks publication. Only exact reviewed manifest identity and
complete mandatory history expose admitted counts. A rate additionally
requires a non-empty cohort with no unobserved terminal state and is emitted
only as an exact integer numerator and denominator.

The current 195-byte manifest contains no windows, so the deterministic result
is `not-ready` and no call count or recovery-free completion rate is exposed.
Reports omit sessions, adapter IDs, tool names, revisions, timestamps, prompts,
arguments, results, errors, evidence locations, paths, and environment values.
M34 adds no runtime/API/protocol/format/dependency/version/telemetry/provider or
release change. Its only workflow change retains the eight existing essential
jobs while limiting them to substantive pull requests, excluding redundant
post-merge and `.project/**`-only runs.

## M35 third-party conformance-adoption boundary

M35 adds no engine, adapter, plugin-loader, or registry module. One explicitly
invoked example outside `src/ludoweave` reads a bounded reviewed manifest and
emits sanitized aggregate admission evidence. Existing installed M17-M19
conformance runners produce evidence only when a caller explicitly supplies a
trusted factory; the M35 evaluator neither imports nor executes that factory.

The accepted registry contains only the existing render-device, agent-tool,
and WorldStore baseline protocols, profiles, and fixed check counts. A
plugin-backed record is possible only for the existing M12 `render.device`
capability and requires both a compatible reviewed inert manifest and a
passing installed render-device profile. The inert manifest alone is never
behavioral conformance. Agent-tool and WorldStore records remain adapter
records because no matching whole-service plugin capability exists.

Eligibility is established before outcome. Project-owned and maintainer-
authored implementations are excluded. Human review owns independence,
authorship, license, eligibility, provenance, outcome, validation, privacy,
consent, and completeness of the project-accepted submission census. Passed,
failed, and not-executed submissions remain in complete accepted history; only
distinct passing implementation identities contribute to the aggregate count.

The current reviewed 250-byte manifest contains no submissions, so the result
is `not-ready` with a zero passing count. The report omits implementation,
package, repository, revision, artifact, evidence-location, platform, and
environment identities. It is not a global package census, support matrix,
security or performance result, provider certification, or ecosystem claim.
M35 changes no runtime/public API/protocol/profile/format, dependency, lock,
version, CI topology, release, publication, discovery, installation, provider
execution, network, telemetry, or support policy.

## M36 CI runner-ownership boundary

M36 changes workflow orchestration only. The same eight validation slices
remain: Ubuntu CPython 3.12 quality/distribution, Ubuntu 3.13 and 3.14
compatibility, Windows and macOS 3.14 compatibility, and CPython 3.12 real-
graphics evidence on all three desktop operating systems.

Those slices are owned by three runners rather than eight. One Ubuntu runner
performs quality, distribution, Linux graphics, and then the two later-CPython
compatibility slices. A two-entry desktop matrix gives Windows and macOS one
runner each; each performs its 3.12 graphics slice before replacing the locked
environment with 3.14 for compatibility tests. Environment replacement is
explicit and no slice relies on packages left by another Python version.

The tradeoff is deliberate: slices within an OS fail sequentially, reducing
parallel feedback and rerun granularity while avoiding five runner allocations
and five repeated checkout/setup sequences. Windows and macOS remain isolated
from each other with matrix fail-fast disabled. The workflow remains pull-
request only, least privilege, pinned, cached, bounded, credential-free, and
cancelable. M36 changes no test scope, runtime, dependency, lockfile, package,
release workflow, or supported platform/version contract.

## M37 CI change-qualification boundary

M37 classifies the exact pull-request three-dot diff inside the existing Linux
job. The classifier is loaded from the exact base revision, so the candidate
diff cannot change the policy used to classify itself. Missing policy, empty or
invalid input, unrecognized paths, decoding failure, and Git failure are
substantive or block the Linux gate; none can silently select a smaller gate.

Documentation-only means root Markdown, Markdown below `docs/` and `.project/`,
and the bounded issue/pull-request metadata files named by RFC-0020. `mkdocs.yml`
and non-Markdown files remain substantive so executable hooks cannot enter
through the smaller gate. One Linux
allocation still performs lock, formatting/lint, strict docs, architecture,
build, installed-wheel, and release-candidate checks. Those checks protect the
package metadata and release bundle that include documentation.

Every other change is substantive. The existing Linux job performs its full
M36 quality/distribution/graphics/CPython 3.12-3.14 slices before the dependent
Windows/macOS matrix starts. The two desktop jobs run only for a successful
`substantive=true` Linux result. This preserves all eight slices and three-
allocation ceiling for substantive work, avoids desktop allocation after an
early Linux failure, and trades additional wall time for lower avoidable quota.
Workflow triggers, privileges, pins, credentials, cache, timeouts, runtime,
dependencies, lock, release workflow, and supported versions remain unchanged.

## M38 distribution-reproducibility boundary

M38 compares two independent output directories after rebuilding the pure
wheel and source archive in the existing Linux pull-request and tag-release
jobs. The standard-library verifier requires exactly one matching
`py3-none-any` wheel/source pair per directory, rejects symlinks, nested or
extra entries, missing or inconsistent names, unreadable files, and differing
bytes, and emits deterministic versioned JSON with sizes and SHA-256 digests.

Comparison happens before installed-wheel smoke, release staging, attestation,
or publication. It adds one build to each already allocated distribution job
without adding a workflow job, matrix entry, action, permission, trigger,
dependency, lock entry, credential, runtime import, or public API. The bounded
claim is same-source byte identity inside one validated job. It is not
cross-platform reproducibility, a hermetic-build claim, independent rebuild
consensus, provenance, publication, or package availability. RFC-0021 defines
the complete decision.

## M39 release-ref integrity boundary

M39 separates release-ref admission from artifact validation. The existing
tag job first requires the exact `vVERSION` ref to target an annotated tag
object, GitHub to report its signature as valid, the local and GitHub tag
objects to target the exact checked-out event commit, and that commit to be an
ancestor of fetched `origin/main`. Only then may system setup, tests, builds,
M38 comparison, staging, attestations, or publication proceed.

The standard-library verifier consumes runner-temporary GitHub API documents
plus the local repository. The job materializes the verifier from fetched
`origin/main` rather than trusting the not-yet-admitted tag checkout's script.
It caps strict duplicate-free JSON inputs, checks local Git without a shell,
and emits only tag, tag-object SHA, commit SHA, and main-ref identity. Signature
and payload bytes never enter output. GitHub's tag-object API is the signature-
verification authority; local Git proves object, checkout, and ancestry
identity but owns no signing-key trust store.

M39 adds no runner allocation, action, permission, trigger, credential,
dependency, runtime import, public API, tag, release, or publication authority.
It does not define a signer/key allowlist, key rotation or revocation, immutable
release policy, PyPI channel, trusted publishing, or supported release channel.
It also cannot protect a workflow file that an authorized tag actor can replace;
tag and environment protection remain repository operations.
RFC-0022 defines the full trust and non-claim boundary.

## M40 draft-release asset integrity boundary

M40 separates remote asset admission from the final publication transition.
After the exact tag, quality, build, staging, smoke, and attestation gates pass,
the existing tag job creates a prerelease draft without assets and uploads the
complete staged set without clobbering. It fetches the draft through a pinned
GitHub REST API version and publishes only after the standard-library validator
confirms the exact tag/title/draft state and every local/remote asset name, byte
size, upload state, and SHA-256 digest.

The validator owns no network client, token, shell, dynamic import, release
mutation, or cleanup authority. It accepts at most 32 safe regular files, caps
individual/total bytes and the strict duplicate-free JSON document, and emits
only sorted safe identities. An invalid or incomplete remote set fails with a
versioned structured result and leaves the release unpublished for deliberate
inspection.

M40 adds no runner allocation, action, permission, trigger, credential,
dependency, runtime import, public API, tag, release, or publication authority.
It does not enable immutable releases, independently verify GitHub storage,
download remote assets, change attestations, define signer policy, or establish
a supported release channel. RFC-0023 defines the full trust and non-claim
boundary.

## M41 release-notes body integrity boundary

M41 closes the remaining draft metadata gap without changing workflow topology.
The M40 validator already receives bounded local staging and the authenticated
GitHub draft document after `gh release create --notes-file` and asset upload.
Protocol `ludoweave.release-draft-integrity/2` additionally reads the fixed
staged `RELEASE_NOTES.md` member and requires the remote release `body` to equal
that exact text before asset admission and publication.

The notes reader accepts only a regular non-symlink file of at most 256 KiB,
strict non-empty UTF-8, and no NUL. It accepts no normalization: missing, null,
non-text, substituted, truncated, newline-different, whitespace-different, or
Unicode-different bodies fail closed. Output contains only the existing safe
tag/asset identities or a stable code; release-note content never enters logs.

M41 adds no network client, workflow change, runner allocation, action,
permission, trigger, credential, dependency, runtime import, public API, tag,
release, or publication authority. It compares GitHub's API source body rather
than rendered Markdown and does not verify link safety, factual completeness,
human approval, independent storage, or immutability. RFC-0024 defines the full
trust and non-claim boundary.

## M42 published prerelease integrity boundary

M42 extends the exact release identity through the final public-state
transition. Protocol `ludoweave.release-draft-integrity/3` requires every
validator invocation to select `draft` or `published`. The draft contract adds
an explicit null `published_at`; the published contract requires
`draft=false`, `prerelease=true`, a boolean `immutable`, and a valid UTC
publication timestamp. Both states retain exact tag, title, notes, and asset
verification.

The draft step exposes only its validated numeric release database ID. After
the existing `gh release edit --draft=false` transition, one read-only API call
fetches that same ID and the same standard-library validator confirms published
state. Success emits only state, tag, and safe asset identities, never the
timestamp, immutable policy, or notes text.

This is a postpublication observation, not transaction rollback: mismatch
fails the job but the prerelease is already public, and no automatic deletion,
unpublishing, or mutation occurs. Accepting either boolean immutable value
avoids silently imposing repository policy. M42 does not prevent later edits,
enable immutability, download public assets, replace attestations, add a runner
or permission, or expand publication authority. RFC-0025 defines the full trust
and non-claim boundary.

## M43 published asset retrieval integrity boundary

M43 extends M42 from authenticated metadata to one exact stored-byte retrieval
observation. Protocol `ludoweave.release-draft-integrity/4` requires every
remote asset to carry a unique positive 63-bit database ID. Only after complete
published-state, notes, and asset verification may the validator create an
exclusive `ludoweave.release-asset-retrieval-plan/1` runner-temporary file.
The plan contains only a protocol header plus canonical name-sorted decimal ID,
expected byte size, and safe-basename tuples; normal structured output
continues to omit IDs, URLs, paths, notes, timestamps, and immutable state.

The existing tag job owns retrieval. It validates plan tokens again, requests
each exact asset ID from the versioned GitHub API with
`Accept: application/octet-stream`, streams at most the expected size plus one
byte into each new partial path, rejects short/long responses, enforces the
expected-total cap, and invokes the same validator on the retrieved directory
and exact M42 published document. The validator owns only deterministic bounded
local reads and the explicit exclusive plan write; it owns no token, network
client, shell, process, release mutation, retry, rollback, or cleanup authority.

This establishes that the authenticated release-asset endpoint returned the
same complete byte set as staged and reported at one observation point. It
does not prove unauthenticated access, global CDN/cache state, future bytes,
immutability, consumer installation, sample execution, or attestation
verification. A mismatch occurs after publication and fails the job without
unpublishing, deleting, clobbering, or otherwise mutating the release. M43 adds
no runner, action, permission, trigger, credential, dependency, runtime import,
public API, tag, release, upload, or publication authority. RFC-0026 defines
the full trust and non-claim boundary.

## M44 published release attestation integrity boundary

M44 extends M43's exact downloaded-subject set into one bounded hosted
attestation observation. After every downloaded byte is revalidated against
the same published document, a standard-library verifier requires SLSA v1
provenance for each admitted asset and an SPDX 2.3 SBOM attestation for exactly
one pure `ludoweave-*-py3-none-any.whl`.

Every `gh attestation verify` call constrains the exact repository, release
workflow, source ref, source and signer commit, GitHub Actions OIDC issuer,
hosted-runner class, predicate type, candidate count, and 30-second timeout.
The M43 plan remains the authority for a maximum of 32 exact safe basenames,
individual/total sizes, and directory equality. Child stdin, stdout, and
stderr are discarded; the verifier reports only stable failure codes or
aggregate success counts. With one additional wheel SBOM check, at most 33
sequential child processes can run.

The existing tag job owns the token, CLI, network, plan, and temporary files;
the verifier owns only bounded local validation and child-process execution.
Failure occurs after publication and does not retry, unpublish, delete, edit,
clean up, or roll back the release. Verified subject and identity evidence does
not establish artifact security, an independent or trusted build, predicate
truth beyond the constrained type/identity, future availability or non-
revocation, global asset access, immutability, consumer installation, sample
execution, or a supported release channel. M44 adds no runner, action,
permission, trigger, dependency, credential, runtime import, public API, tag,
release, upload, publication, rollback, or cleanup authority. RFC-0027 defines
the complete trust and non-claim boundary.

## M45 public release consumer-path integrity boundary

M45 extends M44 with one credential-free observation of the consumer-facing
GitHub API path. The existing tag job fetches the exact M42 release ID and each
exact M43 asset ID from fixed `api.github.com` HTTPS endpoints without a GitHub
credential, authorization header, cookie, browser URL, or caller-selected
host. Client configuration is disabled; redirects, connect/request duration,
document bytes, asset count, individual/total bytes, names, IDs, and new
partial paths remain bounded.

The public release document must independently satisfy the same exact staged
tag/title/notes/asset/published-state contract before downloads. Every public
asset must have its planned exact length before rename, the complete public
directory must satisfy the same validator, and the existing release smoke then
checks hashes, manifest, SPDX metadata, safe extraction, isolated wheel
installation, and bundled acceptance scenarios against those bytes.

This occurs after publication and M44. Failure does not retry, unpublish,
delete, edit, clean up, or roll back anything. One same-run hosted Linux public
API and installed-candidate pass is not independent/external consumer evidence,
a clean-machine or cross-platform matrix, proof for every browser/CDN/cache/
geographic path, a future-availability or immutability guarantee, artifact
security, PyPI availability, or a supported release channel. M45 adds no job,
runner, action, permission, trigger, dependency, credential, runtime import,
public API, package version, tag, release, upload, publication, rollback, or
cleanup authority. RFC-0028 defines the complete boundary.

## M46 fresh-runner consumer-rehearsal boundary

M46 separates the final public-byte and installed-candidate observation from
the publishing runner without pretending the result is external. The existing
release job exposes only its verified numeric release ID and package version.
After that job succeeds, one read-only Linux job starts with a new workspace,
checks out the exact tagged source without persisted credentials, installs the
pinned tool/Python pair without a dependency cache, and retrieves the exact
named candidate preserved by the same workflow.

One repository-owned shell verifier serves both jobs. Its explicit mode owns
the plan boundary: the publishing runner must reuse M43's existing plan, while
the fresh runner requires the path to be absent and creates a new exclusive
plan only after the admitted candidate matches the bounded public document.
Both paths retain M45's fixed repository, ID, HTTPS/redirect/time, document,
name, count, byte, partial-file, exact-set, and installed-smoke bounds.

The fresh job has `contents: read` and no release, attestation, or identity-
token write permission. Public requests receive no release credential, but the
checkout and artifact actions use GitHub's scoped workflow services. Failure
occurs after publication and adds no retry, mutation, rollback, or cleanup.

One fresh GitHub-hosted Linux runner is not independent/external verification,
a cross-platform public matrix, a clean machine outside the same provider,
every delivery path, future availability, immutability, artifact security,
PyPI, or a supported release channel. M46 adds one tag-only runner and one
pinned download action but changes no pull-request CI allocation, release
trigger or publication authority, staged artifact, dependency, runtime, or
public API. RFC-0029 defines the complete boundary.

## M47 cross-platform public consumer-rehearsal boundary

M47 replaces the internal Bash public verifier with one typed standard-library
Python program and expands M46's existing tag-only fresh-consumer job to the
exact Ubuntu, Windows, and macOS matrix. The publishing invocation reuses the
existing M43 plan; each fresh operating-system runner rejects a preexisting
plan, retrieves the exact named same-workflow candidate, and creates its own
exclusive plan before downloading public bytes and running complete installed
release smoke.

The portable verifier owns no credential or caller-selected endpoint. Initial
requests are fixed to the exact GitHub API repository and numeric IDs. Remote
redirects must remain HTTPS on port 443 and stop after three responses. A
verified default TLS context, 10-second blocking limit, 30-second monotonic
deadline, 4-MiB document, 16-KiB plan, 32 unique safe assets, 256-MiB per-asset
limit, 512-MiB total, exclusive ID-derived partials, exact length checks, and
the existing before/after release-document validation bound the observation.

Every fresh job has read-only contents permission, no dependency cache, and no
release, attestation, or identity-token write permission. The matrix adds two
tag-only runner allocations but no pull-request allocation. It adds no release
trigger, artifact, mutation, publication, rollback, credential, dependency,
runtime, package, or public API.

A successful authorized tag run would provide hosted same-workflow observations
on the three supported operating systems. It would not provide an independent
or external consumer/provider/build, a clean machine outside GitHub-hosted
Actions, every delivery path, future availability, immutability, artifact
security, PyPI, or a supported channel. RFC-0030 defines the complete boundary.

## M48 public release HTTP response-conformance boundary

M48 narrows the shared M47 verifier to the exact documented endpoint response
shapes. The fixed public release-document request accepts only a direct `200`.
Each fixed asset-ID request accepts a direct `200` or follows at most three
`302` responses through the existing bounded HTTPS/default-port URL parser.
Every other redirect status fails closed. The GitHub API-version header is
included only when the current host is `api.github.com`, so remote object hosts
receive no API-only request metadata.

The initial connection retains M47's ten-second blocking timeout within a
30-second monotonic request deadline. The connected socket timeout is refreshed
after request transmission and before response headers, then before each
bounded body read. `TimeoutError` maps to the stable request-timeout code before
the broader `OSError` hierarchy is handled. Other socket/HTTP protocol failures
map to request failure, while exclusive local creation, write, finalization, or
removal failures map to output failure. Internal exception chaining preserves
the cause; public JSON remains generic and content-silent.

M48 changes no workflow, allocation, action, permission, credential, trigger,
release mutation, retry, cleanup, dependency, runtime, package, or public API.
It preserves every M47 identity, TLS, document, plan, count, byte, path,
partial, exact-validation, and installed-smoke bound. Pull-request evidence is
not a real public release observation, independent/external verification,
future availability, immutability, artifact security, PyPI, or a supported
channel. RFC-0031 defines the complete boundary.

## M49 public release connected-peer boundary

M49 closes the remaining gap between a syntactically bounded redirect hostname
and the address actually reached. Before sending HTTP on the fixed API request
or any bounded asset redirect, the verifier explicitly establishes its normal
verified TLS connection and inspects `getpeername()`. The peer must be a
well-formed IPv4 or IPv6 address at actual port 443. IPv4-mapped IPv6 is
classified through its embedded IPv4 address.

Only globally reachable unicast addresses proceed to request transmission.
Private, shared, loopback, link-local, documentation, benchmarking,
unspecified, multicast, reserved, and every other non-global address fail with
the content-silent `public_release.peer_forbidden` code. The check applies to
the actual connected socket, avoiding a separate DNS result that could differ
from the connection. It occurs after the TLS handshake needed to discover the
peer but before HTTP method, path, or headers are sent.

Connect or peer-inspection timeouts retain M48's request-timeout code.
Malformed peer results, unavailable sockets, wrong ports, and other inspection
failures use request failure. No public diagnostic includes the peer, hostname,
URL, or response content. M49 adds no hostname/IP allowlist, separate DNS
preflight, proxy, network sandbox, retry, cleanup, workflow, allocation,
permission, credential, dependency, runtime, package, public API, or release
mutation. Pull-request evidence is not a real public release observation,
independent/external verification, every CDN path, future availability,
immutability, artifact security, PyPI, or a supported channel. RFC-0032 defines
the complete boundary.

## M50 public release TLS key-log isolation boundary

M50 removes the portable client's ambient TLS debugging hook. Each fixed API
or bounded redirect hop receives a newly constructed `PROTOCOL_TLS_CLIENT`
context. The verifier explicitly loads system server-auth roots, requires
certificate and hostname validation, sets TLS 1.2 as the minimum protocol
version, and enables strict plus partial-chain X.509 verification. It verifies
that TLS key logging remains disabled before the context reaches an
`HTTPSConnection`.

The standard-library default-context helper is not used because supported
CPython intentionally enables key logging when `SSLKEYLOGFILE` is present.
That behavior can append TLS session secrets to an ambient path. M50 neither
removes nor changes the process environment: the variable remains untouched,
its target is not created, and an independent context is built for every hop.
Context creation, root loading, or invariant failure uses the stable,
content-silent `public_release.tls_failed` code.

M50 retains M49 connected-peer confinement and all M48/M47 request, response,
identity, deadline, size, path, exact-validation, and installed-smoke bounds.
It adds no custom CA bundle, certificate/SPKI pinning, client certificate,
proxy, workflow, allocation, permission, credential, dependency, runtime,
package, public API, retry, cleanup, or release mutation. System trust remains
the trust boundary. Pull-request fixtures are not a real public release
observation, negotiated-session audit, independent/external verification,
future-availability proof, immutability proof, artifact-security result, PyPI
availability, or a supported channel. RFC-0033 defines the complete boundary.

## M51 public release negotiated TLS-session boundary

M51 validates the actual session established by each M50 context. The context
advertises only `http/1.1`. After the M49 actual connected-peer check and
before any HTTP method, path, or header is sent, the verifier reads the socket's
negotiated version, cipher, compression, and ALPN state.

Only TLSv1.2 and TLSv1.3 are accepted. The cipher report must contain a non-
empty name, a non-empty protocol-that-defines-the-cipher field, and an integer
secret-bit count of at least 128. TLS compression must be absent. Negotiated
ALPN may be `http/1.1` or `None`; any other explicit application protocol is
rejected. There is no cipher-name allowlist, and the cipher report's protocol
field need not equal the negotiated TLS version. A future protocol label must
be admitted by a reviewed decision rather than silently widening this exact
contract.

The connection owns the negotiated socket. Its existing close path remains
authoritative after session validation succeeds or fails. Every redirect owns
a new context, connection, peer check, and session check. Missing accessors,
malformed values, unsupported inspection, or failed invariants use the stable,
content-silent `public_release.tls_failed` code and occur before HTTP
transmission.

M51 retains every M50-M47 trust, key-log, peer, response, identity, deadline,
size, path, exact-validation, and installed-smoke bound. It adds no custom
trust, certificate/SPKI pinning, revocation policy, TLS fingerprint, workflow,
allocation, permission, credential, dependency, runtime, package, public API,
retry, cleanup, or release mutation. Fixture and pull-request evidence are not
a real public release observation, independent/external verification, every
delivery path, future-availability proof, immutability proof, artifact-security
result, PyPI availability, or a supported channel. RFC-0034 defines the
complete boundary.

## M52 public release TLS service-identity boundary

M52 observes the service identity attached to the actual verified TLS socket.
Before opening the connection, the verifier normalizes the current URL
hostname through built-in IDNA to its ASCII reference hostname and uses that
reference for the hop. After M49 validates the connected peer and before M51
reads negotiated-session state, the socket's `server_hostname` must be a non-
empty case-insensitive match, and `getpeercert(binary_form=True)` must return a
non-empty immutable DER peer certificate.

M50's `PROTOCOL_TLS_CLIENT`, `CERT_REQUIRED`, system trust, hostname checking,
strict X.509 flags, and per-hop context remain authoritative for path,
validity, and certificate/hostname matching. M52 proves only that the actual
socket retained the expected reference hostname and peer certificate; it does
not parse, export, rematch, pin, fingerprint, or independently validate a
certificate or chain.

The connection remains the sole socket owner. Every redirect creates and
checks an independent context, connection, peer, service identity, session,
and close path. Missing or unsupported accessors, invalid IDNA, malformed or
mismatched reference hostname, unavailable/non-byte certificate, or inspection
failure uses the stable, content-silent `public_release.tls_failed` code before
HTTP transmission.

M52 retains every M51-M47 trust, key-log, peer, session, response, identity,
deadline, size, path, exact-validation, and installed-smoke bound. It adds no
custom trust, certificate/SPKI pinning, certificate-chain parser/export,
revocation/OCSP/CRL/CT policy, DNSSEC, workflow, allocation, permission,
credential, dependency, runtime, package, public API, retry, cleanup, or
release mutation. Fixture and pull-request evidence are not a real public
release observation, independent/external verification, every delivery path,
future-availability proof, immutability proof, artifact-security result, PyPI
availability, or a supported channel. RFC-0035 defines the complete boundary.

## M53 public release TLS context-binding boundary

M53 observes the context binding on the actual connected TLS socket. After the
handshake and M49 peer confinement, but before M52 service-identity evidence,
M51 negotiated-session inspection, or HTTP transmission, the socket must expose
the exact context object supplied to that hop's `HTTPSConnection` and an
exactly client-side `server_side` value of `False`.

The verifier then revalidates the complete M50 context policy after the
handshake: `PROTOCOL_TLS_CLIENT`, `CERT_REQUIRED`, hostname checking, an exact
TLSv1.2 minimum, strict plus partial-chain verification flags, and no key-log
file. Object identity is required; a separately configured equivalent context
does not establish ownership of the actual socket. Every redirect owns and
checks a new exact context independently.

A missing socket or accessor, substituted context, non-client role, changed
policy, unsupported inspection, or inspection failure uses the stable,
content-silent `public_release.tls_failed` code before service identity,
session inspection, or request transmission. The existing per-hop `finally`
path owns connection closure and preserves a local chained cause when one is
available.

M53 changes no workflow, runner allocation, dependency, package, runtime API,
or release authority. It adds no trust replacement, pinning, certificate/chain
parser, revocation, session reuse, channel binding, proxy policy, or network
sandbox. Fixture and pull-request evidence are not a real public release
observation, independent/external verification, every delivery path, future-
availability proof, immutability proof, artifact-security result, PyPI
availability, or a supported channel. RFC-0036 defines the complete boundary.

## M54 public release TLS session-freshness boundary

M54 observes whether the actual connected TLS socket reports session reuse.
After the handshake, M49 peer confinement, and M53 exact context binding, but
before service identity, negotiated-session inspection, or HTTP transmission,
the socket's `session_reused` property must be exactly `False`. A falsey
non-boolean value does not satisfy this contract.

The connection remains the sole socket owner. Every redirect creates its own
context and connection, then repeats the post-handshake freshness observation.
A missing socket or accessor, unsupported observation, resumed session,
malformed value, or inspection failure uses the stable, content-silent
`public_release.tls_failed` code before later TLS evidence or a request. An
available local inspection exception remains chained as its cause.

This check consumes the supported TLS implementation's per-connection report;
it does not reconstruct the handshake or independently prove a certificate
exchange. M54 changes no workflow, runner allocation, dependency, package,
runtime API, or release authority. It adds no session cache, session
assignment, ticket control, TLS implementation introspection, custom trust,
pinning, certificate/chain parser, revocation, channel binding, proxy policy,
or network sandbox. Fixture and pull-request evidence are not a real public
release observation, independent/external verification, every delivery path,
future-availability proof, immutability proof, artifact-security result, PyPI
availability, or a supported channel. RFC-0037 defines the complete boundary.

## M55 public release HTTP response-framing boundary

M55 validates the documented HTTP response metadata after all connected-peer
and TLS checks and `getresponse()`, but before status, redirect, or body use.
Every response, including every redirect, must report `version` as the non-
boolean integer `11`, Python's documented HTTP/1.1-class value.
`Transfer-Encoding` must be absent or exactly `chunked` under case-insensitive
comparison and cannot coexist with `Content-Length`. Any present content length
must be a string before the existing ASCII-decimal, maximum-size, and exact-
size validation runs.

The public version property is not exact status-line token evidence. CPython
can normalize another raw `HTTP/1.x` token into value `11`; M55 deliberately
does not use a private parser surface to distinguish it.

The standard-library HTTP connection remains the owner and decoder. Valid
chunked payloads reach the existing deadline-aware, byte-bounded decoded-body
reader. Unsupported versions or transfer codings, ambiguous framing, malformed
metadata, and inspection failures use stable, content-silent
`public_release.request_failed`; supported local inspection errors remain
chained. Redirect responses are checked before their status or `Location` is
used.

M55 uses no private response `chunked`, `length`, or `will_close` state, adds no
raw HTTP or chunk parser, alternate client, HTTP/2 or HTTP/3, proxy,
decompression, workflow, allocation, dependency, package, runtime API, or
release authority. Fixture and pull-request evidence are not a real public
release observation, exact status-line identity, a general request-smuggling
defense, independent or external verification, every intermediary or delivery path, future
availability, immutability, artifact security, PyPI availability, or a
supported channel. RFC-0038 defines the complete boundary.

## M56 public release status and redirect-reference boundary

M56 validates documented response status after M55 framing and before status
comparison, redirect resolution, or body use. Every response status must be an
integer, but not a boolean, from 100 through 599. Each followed `302` must expose
a documented header-pair list containing exactly one case-insensitive Location
field. Its value must be a single URI-reference from 1 through 8,000 ASCII
octets, use RFC 3986 reference characters, and contain only complete percent
escapes. Bracket delimiters are permitted only inside a parsed authority and
are rejected in its path, query, or fragment.

Only the validated Location is resolved against the current URL. The resolved
value must pass the existing bounded HTTPS URL policy before it becomes the
next hop. Relative references and cross-host absolute references remain
supported; every resulting hop independently repeats connected-peer, TLS
context/freshness/identity/session, HTTP framing, deadline, byte-bound, and
exact-artifact validation. There is no host allowlist.

Malformed or raising status uses stable, content-silent
`public_release.request_failed`. Missing, duplicate, malformed, unsupported,
oversized, or raising Location metadata and invalid resolution use
`public_release.redirect_failed`; supported local causes remain chained.

M56 uses only documented `status` and `getheaders()` surfaces. It adds no
private response state, raw HTTP or general URI parser, alternate client,
proxy, DNS preflight, network sandbox, workflow, allocation, dependency,
package, runtime API, or release authority. Fixture and pull-request evidence
are not a real public release observation, general SSRF defense, independent
or external verification, every delivery path, future availability,
immutability, artifact security, PyPI availability, or a supported channel.
RFC-0039 defines the complete boundary.

## M57 public release response-body boundary

M57 validates every successful response body after M55 framing and M56
status/redirect checks. Each `HTTPResponse.read(amount)` result must be
immutable bytes no larger than the requested amount. Validation occurs before
EOF interpretation, byte accounting, or local output, so malformed text,
mutable buffers, absent values, and oversized blocks fail closed.

When M55 exposes a `Content-Length`, M57 retains the validated integer and
requires it to equal the total streamed octets after EOF. The check applies to
the public release document and every successful response after an asset
redirect. Existing expected asset sizes remain independently enforced with or
without a declared length. Malformed block shapes use content-silent
`public_release.request_failed`; declared-versus-streamed disagreement uses
`public_release.size_mismatch`; supported local causes remain chained.

M57 uses only documented `HTTPResponse.read(amount)` and the already validated
M55 length. It adds no private response/socket state, raw HTTP/chunk parser,
content decoder, alternate client, cleanup, proxy, DNS preflight, network
sandbox, workflow, allocation, dependency, package, runtime API, or release
authority. It does not claim general completeness for unframed close-delimited
bodies. Fixture and pull-request evidence are not a real public release
observation, independent or external verification, every delivery path,
future availability, immutability, artifact security, PyPI availability, or a
supported channel. RFC-0040 defines the complete boundary.

## M58 public release cleanup boundary

M58 makes ownership cleanup explicit after the M47-M57 public-release checks.
Every obtained response receives one response close attempt before its created
connection receives one connection close attempt. Both close attempts occur
when response close fails. An already-active request, protocol, validation,
output, or control-flow failure remains the primary failure; cleanup-only
ordinary failures use content-silent `public_release.request_failed` with the
first cleanup cause chained.

Cleanup completes successfully before redirect continuation and before partial
publication from a separate asset partial path. Cleanup control signals remain
unwrapped after both close attempts. M58 uses only documented public close
methods and adds no private state, alternate client, raw parser, rollback,
retry, workflow, allocation, dependency, package, runtime API, or release
authority. Fixture and pull-request evidence are not a real public release
observation. RFC-0041 defines the complete boundary.

## M60 public release output-path boundary

M60 makes filesystem collision detection a fail-before-side-effect boundary
for the portable public-release verifier. Before network or validator work,
the verifier inspects the final directory entry for its fresh release document,
download directory, and retrieval plan without following that final link. Each
asset target and separate asset partial receives the same check before a
connection is created. A file, directory, live link, or dangling link therefore
blocks the operation with the existing output- or plan-collision taxonomy.
Inspection failures are content-silent output or plan failures.

The existing `x`/`xb` exclusive creation and hard-link publication remain the
authoritative no clobber operations after preflight. M60 makes no race-free
filesystem guarantee and adds no descriptor-confined sandbox, rollback,
cleanup, retry, workflow, allocation, dependency, lock, version, runtime API,
release authority, or real public release observation. RFC-0043 defines the
complete boundary.

## M61 public release candidate/output-root boundary

The expected release candidate directory is read-only input. After rejecting a
missing or final-link root, the verifier strictly resolves both that candidate
directory and the runner-owned output root. A resolution failure remains a
content-silent candidate- or temporary-directory failure. Before network or
validator side effects, the output root must neither equal nor resolve beneath
the candidate directory; a resolved alias receives stable
`public_release.path_overlap`. Each resolved output ancestor is also compared
to the candidate by filesystem identity, covering an alias whose spelling
differs on a case-insensitive filesystem. Identity inspection fails closed as
a content-silent temporary-directory error. The resolved directories become
the owned verification context. A separate candidate directory beneath the
output root remains valid when the fixed M60 output entries are siblings rather
than ancestors.

M61 makes no race-free filesystem guarantee. It does not add descriptor-
relative opens, a directory-descriptor or general path sandbox, locks,
rollback, cleanup, retry, workflow, allocation, dependency, lockfile, version,
runtime API, release authority, or real public release observation. RFC-0044
defines the complete boundary.

## M62 portable public release asset-name boundary

The public-release retrieval-plan parser admits one portable asset name as 1
through 255 ASCII characters from the existing restricted basename alphabet.
It rejects a trailing period, a first period-delimited Windows device stem, and
any case-insensitive duplicate in the same plan. The existing
`public_release.invalid_plan` failure is content-silent and occurs before asset
download and before creation of the asset output directory. Portable existing
release names remain byte-for-byte identities; the verifier never rewrites or
normalizes them.

M62 uses no filesystem probing, host-specific reserved-name API, locale,
Unicode normalization, path resolution, or race isolation. It adds no cleanup,
rollback, retry, workflow, dependency, lockfile, version, runtime API, release
authority, or real public release observation. RFC-0045 defines the complete
boundary.

## M63 public release subordinate-output boundary

The standalone public-release consumer owns stdout and stderr around both
in-process subordinate types: the release-document validator and complete
release smoke. Subordinate stdout and subordinate stderr are redirected to
private text sinks and restored on normal return or exception. The consumer
therefore emits one JSON document on stdout for success or one content-silent
JSON document on stderr for an admitted failure.

Subordinate success is an exact built-in zero integer. Boolean, float, integer-
subclass, and custom comparison values fail without calling their comparison or
truth hooks. Invalid validator status retains document mismatch; invalid smoke
status retains smoke failure.

Python stream redirection is process-global, so this boundary relies on the
verifier's existing single-thread command ownership. It makes no thread-safe
library, direct file-descriptor, or arbitrary subprocess-output claim. M63 adds
no workflow, dependency, lockfile, version, runtime API, release authority, or
real public release observation. RFC-0046 defines the complete boundary.

## M64 bounded sample-bundle extraction boundary

The release smoke preflights every staged sample ZIP member before extraction
creates a path. The archive may contain at most 256 members, each member may
declare at most 1 MiB uncompressed, and all members together may declare at
most 8 MiB uncompressed. Existing path confinement and symbolic-link rejection
are part of the same complete preflight. Stored and deflated are the only
admitted compression methods; BZIP2, LZMA, and unknown methods fail before a
filesystem write because their standard-library read paths do not share the
deflate path's bounded decompressor-output behavior.

After preflight, regular files stream through `ZipFile.open()` in 64 KiB blocks.
The extracted byte count must exactly equal the preflight declaration, avoiding
whole-expanded-member allocation and failing closed on a size disagreement.
The actual M63 sample bundle is far below every limit.

This boundary is private release tooling, not a runtime or public Python API.
It adds no cleanup or rollback guarantee after preflight, general archive
sandbox, or raw parser that bounds `zipfile`'s initial central-directory parse.
It adds no workflow, dependency, release authority, or real public release
observation. RFC-0047 defines the complete boundary.

## M65 portable sample member path boundary

M65 extends the same complete preflight with deterministic lexical identity.
Each regular-file member has the exact expected root and a relative portable
sample member path of at most 255 ASCII characters. Every component begins
with an ASCII alphanumeric, uses only the admitted ASCII punctuation, excludes
a trailing period and Windows device stem, and is retained without rewriting.
Explicit directory members are rejected; extraction derives directories only
from admitted file ancestors. An explicitly encoded ZIP file type must be a
regular file; missing type bits remain compatible with common ZIP producers.

Complete paths are unique case-insensitively, every case-insensitive directory
ancestor has one exact spelling, and no admitted file is a prefix ancestor of
another file. Duplicate, case-ambiguous, or file/directory prefix collision
paths therefore fail before extraction creates a directory or file. Validated
component tuples are paired with the already-preflighted `ZipInfo` sequence for
M64's stored/deflated bounded streaming pass.

This is a private project-bundle policy, not a general archive sandbox or a
guarantee that every host accepts every admitted absolute extraction path. It
performs no Unicode normalization, locale comparison, filesystem probing,
path rewriting, race isolation, or transactional cleanup. M65 adds no workflow,
dependency, sample-producer, runtime API, release authority, or real public
release observation. RFC-0048 defines the complete boundary.

## M66 staged sample-root publication boundary

M66 requires the release smoke's caller-owned output parent to exist as a real
directory and the versioned final sample root not to exist, including as a
dangling symbolic link. These checks run before archive content is opened.
After the complete M64/M65 preflight, admitted files stream into the expected
root beneath an owned same-filesystem temporary staging directory.

Required-file completeness is checked against that staged root. Only a complete
tree becomes the final sample root through a single rename. The temporary-
directory context performs cleanup after a copy, decompression, write,
completeness, or publish failure, so a partial tree never occupies the final
identity. Existing final entries remain untouched.

This is a private single-process visibility boundary, not a general archive
sandbox, filesystem transaction, recovery journal, or cleanup authority over
unowned paths. It is not crash-durable, performs no `fsync`, supplies no
concurrent filesystem race isolation, and cannot roll back after successful
publication. The private random staging name is never emitted or retained.
M66 adds no workflow, dependency, sample producer, runtime API, release
authority, or real public release observation. RFC-0049 defines the complete
boundary.

## M67 exact sample-bundle inventory boundary

M67 adds one independent source-defined expectation to the complete M64-M66
preflight. The verifier collects the validated relative identities and requires
them to equal the exact sample-bundle inventory of 50 regular files. Archive
order is irrelevant. Any unexpected member or missing member fails with one
content-silent category before extraction opens a member or creates the owned
temporary staging directory.

The sample producer remains unchanged and independently reviewable. An
architecture test builds its current deterministic ZIP and compares its members
with the verifier expectation, so producer drift fails closed and an intentional
inventory change requires both sides to be reviewed explicitly.

This private product-shape check is not a content scanner, malware detector,
file-format validator, permission policy, provenance system, or general archive
sandbox. It adds no workflow, dependency, sample producer, runtime API, release
authority, or real public release observation. RFC-0050 defines the complete
boundary.

## M68 bounded sample-archive container boundary

M68 bounds the parser input that precedes the M64-M67 archive preflight. The
release smoke rejects an obvious non-regular or oversized bundle from path
metadata before opening it. It then opens the bundle once in binary read mode,
revalidates mode and length from that descriptor, and admits only a regular
file no larger than 16 MiB. A non-regular or oversized input fails with a stable
content-silent category before `ZipFile` construction, central-directory
parsing, archive member reads, staging, or extraction output.

The descriptor check is authoritative after the pre-open check, and the same
opened handle is supplied to `ZipFile`, so admission and parsing do not reopen
the source path as separate identities. The archive context closes before its
underlying stream on success and failure. M64's member count,
compression, and expanded-size limits remain necessary and unchanged; a small
container can still expand greatly.

This private project-bundle input boundary is not a raw ZIP parser, general
archive sandbox, authenticated-metadata scheme, malware detector, immutable-
input guarantee, or concurrent filesystem race isolation. It adds no workflow,
dependency, sample producer, runtime API, release authority, or real public
release observation. RFC-0051 defines the complete boundary.

## M69 encrypted sample-member preflight boundary

M69 closes the encrypted-member policy explicitly deferred by M64. During the
existing complete metadata preflight, the release smoke checks every member's
ZIP general-purpose bit flags and rejects traditional encryption, strong
encryption, or masked header values. The stable content-silent failure occurs
before exact-inventory validation, member reads, password handling, staging,
or extraction output.

The public deterministic sample bundle has no confidentiality requirement, so
the verifier adds no password or key lifecycle and the unchanged producer must
emit no encryption indicators. Other ZIP flags retain their existing behavior.

This private check is not a raw ZIP parser, central-directory decryptor,
metadata-authentication scheme, content scanner, malware detector, or general
archive sandbox. It adds no workflow, dependency, sample producer, runtime API,
release authority, or real public release observation. RFC-0052 defines the
complete boundary.

## M70 sample-archive checksum binding boundary

M70 binds the sample extractor to the digest already admitted from the staged
release's `SHA256SUMS`. After M68 path and descriptor admission, the verifier
hashes and rewinds the same opened handle before ZIP parsing. After every
member read and staged-completeness check, it hashes and rewinds that handle
again before publication by final rename. A content-silent mismatch prevents
parser or publication progress as appropriate and preserves M66 cleanup. Each
sample-specific hash reads at most M68's 16 MiB bound plus one rejection byte,
so a growing source does not create unbounded checksum work.

This closes a reopen gap between the earlier artifact checksum pass and sample
consumption, but supplies no immutable-input guarantee: bytes changed and
restored between comparisons may evade the boundary. It is not a general
archive sandbox. It adds no workflow, dependency, sample producer, runtime API,
release authority, or real public release observation. RFC-0053 defines the
complete boundary.

## M71 checksum-admitted sample-snapshot boundary

M71 replaces parsing of the mutable source descriptor with one owned
checksum-admitted snapshot. After path and descriptor admission, the verifier
copies at most 16 MiB into a binary spooled temporary file while hashing. A
mismatch or rejection byte fails content-silently before ZIP parsing or
staging; success rewinds the snapshot and gives it to `ZipFile`. The parser and
member reads therefore consume the exact bytes that matched `SHA256SUMS`.

The snapshot is private and closes before its source, but this creates no
persistent copy, source-immutability guarantee, lock, raw ZIP parser, or general
archive sandbox. It adds no workflow, dependency, sample producer, runtime API,
release authority, or real public release observation. RFC-0054 defines the
complete boundary.

## M72 content-silent sample ZIP failure boundary

M72 places one narrow wrapper around the private checksum-admitted extractor.
Only the standard library's documented `BadZipFile` and `LargeZipFile`
exceptions become the stable error `sample bundle ZIP data is invalid`.
Archive-controlled filenames and parser detail remain available as
programmatic exception context, while suppressed context keeps them out of the
rendered exception. The inner extractor's `ExitStack` and staging contexts
finish owned cleanup before the wrapper normalizes the failure.

Verifier policy failures, filesystem failures, subprocess failures, and other
unexpected exceptions retain their existing categories. M72 adds no general
exception catch, content inspection, raw parser, workflow, dependency, sample
producer, runtime API, release authority, or real public release observation;
it is not a general archive sandbox. RFC-0055 defines the complete boundary.

## M73 content-silent sample ZIP text-failure boundary

M73 adds exactly `UnicodeDecodeError` to M72's private outer catch. CPython's
standard ZIP reader decodes UTF-8-marked archive-controlled names while reading
the central directory and again while reading a local header. Invalid bytes can
therefore fail at constructor time or after owned staging begins. Both paths
now become the existing stable error `sample bundle ZIP data is invalid` after
the inner `ExitStack` and staging contexts finish cleanup.

The original decoding exception remains programmatic context, while suppressed
context keeps its invalid byte sequence, offset, codec, and reason out of the
rendered exception. The catch does not include `UnicodeError`, `ValueError`, or
`Exception`; verifier policy, other text failures, filesystem failures, and
unexpected failures remain specific. M73 adds no raw parser, content scanner,
workflow, dependency, sample producer, runtime API, release authority, or real
public release observation and is not a general archive sandbox. RFC-0056
defines the complete boundary.

## M74 content-silent sample ZIP decompression-failure boundary

M74 adds exactly `zlib.error` to the same private outer catch. After checksum
and exact-inventory admission, Python's ZIP member reader sends deflated bytes
to a raw-deflate decompressor. Invalid compressed payload bytes can therefore
fail after owned staging begins even though the container metadata, declared
sizes, paths, method, and checksum are internally admitted. That exact failure
now becomes the existing stable error `sample bundle ZIP data is invalid`
after the inner `ExitStack`, member/target contexts, and staging context finish
cleanup.

The original decompression exception remains programmatic context, while
suppressed context keeps its library- and content-determined diagnostic out of
the rendered exception. The catch does not include `EOFError`, `OSError`, or
`Exception`; verifier policy, truncated-stream categories outside this
decision, filesystem failures, and unexpected failures remain specific. M74
adds no replacement decompressor, raw parser, content scanner, workflow,
dependency, sample producer, runtime API, release authority, or real public
release observation and is not a general archive sandbox. RFC-0057 defines the
complete boundary.

## M75 compressed-patch sample-member preflight

M75 extends M69's all-member flag preflight with exactly ZIP general-purpose
bit 5. PKWARE assigns that bit to compressed patched data, and supported
CPython `ZipFile.open` paths reject it with `NotImplementedError` only when a
member is opened. The private release smoke instead raises the stable content-
silent policy error `sample bundle uses compressed patched data` before member
metadata validation, exact-inventory validation, staging, or member reads.

Encryption remains the first check, preserving M69's established error when a
member carries both indicators. Other general-purpose bits remain outside this
decision: M75 defines no broad flag allowlist and makes no claim that unexamined
bits are safe. It adds no raw parser, repair, content scanner, workflow,
dependency, sample producer, runtime API, release authority, or real public
release observation and is not a general archive sandbox. RFC-0058 defines the
complete boundary.

## M76 enhanced-deflate sample-member preflight

M76 adds one method-scoped check to the all-member preflight. PKWARE reserves
ZIP general-purpose bit 4 for enhanced deflating with compression method 8.
Supported CPython versions do not reject that indicator when otherwise normal
deflate bytes are read. The private release smoke raises the stable content-
silent policy error `sample bundle uses enhanced deflating` before member
metadata validation, exact-inventory validation, staging, or member reads.

M69's encryption and M75's compressed-patch checks execute first. The new
policy applies only when central-directory bit 4 exposed by `ZipInfo` and
compression method 8 coexist; stored members carrying bit 4 remain outside
this decision. The verifier does not raw-parse or compare local-header flags,
so local-header inconsistencies also remain outside scope. M76 defines no broad
flag allowlist and makes no claim that unexamined flag/method combinations are
safe. It adds no enhanced-deflate decoder, raw parser, repair, content scanner,
workflow, dependency, sample producer, runtime API, release authority, or real
public release observation and is not a general archive sandbox. RFC-0059
defines the complete boundary.

## M77 NUL-suffixed sample-member name preflight

M77 adds one exact NUL check to the existing all-member preflight. Supported
CPython versions retain the decoded central-directory filename used to
construct `ZipInfo` in `orig_filename` but truncate normalized `filename` at
the first NUL byte. Without the new check, an exact visible inventory path can
carry an unvalidated hidden suffix. Private release smoke raises the stable
content-silent error `sample bundle member name contains a NUL byte` before
member metadata validation, exact-inventory validation, staging, or reads.

M69, M75, and M76 flag policy executes first and retains precedence. M77 is an
exact NUL check only: it adds no general normalized-name comparison, no raw
parser, no local-header/central-directory consistency claim, rewriting, repair,
or content scanner. It adds no workflow, dependency, sample producer, runtime
API, release authority, or real public release observation and is not a general
archive sandbox. RFC-0060 defines the complete boundary.

## M78 data-descriptor sample-member preflight

M78 adds one exact check for ZIP general-purpose bit 3, the data-descriptor
indicator exposed by `ZipInfo.flag_bits`. Complete release smoke finishes the
established M69/M75/M76 all-member flag pass, then checks every member for bit
3 in a separate archive-wide pass before M77 name checks, member metadata,
exact-inventory validation, staging, or member reads. The stable content-silent
error is `sample bundle uses a data descriptor`.

The fixed sample profile does not need trailing descriptors because its
producer writes to a seekable output. Rejecting the exact flag avoids adding a
second, deferred-size representation to the private consumer boundary.
RFC-0061 adds no raw descriptor parser, no broad flag allowlist, local-header
comparison, decoder, repair, workflow, dependency, sample producer, runtime
API, release authority, or real public release observation. It is not a
general archive sandbox and makes no claim about unrelated flag combinations.

## M79 Unicode Path extra-field preflight

M79 rejects exact Info-ZIP Unicode Path extra-field ID `0x7075`. Supported
CPython versions parse that central-directory field and, when its version and
CRC are valid, replace `ZipInfo.filename` with its UTF-8 path while retaining
the legacy decoded name in `orig_filename`. Complete release smoke performs a
bounded extra-field walk for every member after all M69/M75/M76/M78 policy and
before M77 name checks, metadata, exact inventory, staging, or member reads.
The stable content-silent error is `sample bundle uses a Unicode Path extra
field`.

The fixed producer emits no extra fields. RFC-0062 rejects only the exact
extra-field ID: it adds no broad extra-field ban, general original-versus-
normalized name comparison, arbitrary extra-field validation, local-header
comparison, rewriting, repair, workflow, dependency, runtime API, sample
producer, release authority, or real public release observation. It is not a
general archive sandbox.

## M80 ZIP64 extra-field preflight

M80 rejects exact PKWARE ZIP64 extended-information extra-field ID `0x0001`.
Supported CPython versions substitute its alternate 64-bit size, compressed-
size, and local-header-offset values when corresponding central-directory
fields contain ZIP64 sentinels; current CPython does not consume the field's
defined disk-start value. Complete release smoke walks
every member's already decoded central-directory extra bytes in a separate
pass after M79 Unicode Path policy and before M77 name checks, metadata, exact
inventory, staging, or member reads. The stable content-silent error is
`sample bundle uses a ZIP64 extra field`.

The fixed producer emits no extra fields and its bounded sample has no need
for an alternate large-archive representation. RFC-0063 is an exact extra-
field ID check implemented by a bounded extra-field walk. It adds no broad
extra-field ban, raw ZIP64 parser, archive-record validator, large-file
support change, local-header comparison, repair, workflow, dependency,
runtime API, sample producer, release authority, or real public release
observation. It is not a general archive sandbox.

## M81 ZIP comment preflight

M81 rejects both comment surfaces exposed by the standard ZIP reader for the
fixed sample profile. A parser-exposed non-empty end-of-central-directory
archive comment raises `sample bundle uses an archive comment`; a non-empty
central-directory member comment raises `sample bundle uses a member comment`.
Both errors are stable and content-silent.

Complete release smoke first finishes every established M69/M75/M76 flag pass,
M78 descriptor policy, M79 Unicode Path policy, and M80 ZIP64 policy. It then
checks the archive comment once and every member comment in a separate all-
member pass before M77 decoded-name policy, member metadata, exact inventory,
staging, or member reads. Archive-comment policy therefore precedes member-
comment policy, while established categories retain archive-wide precedence.
Owned source, checksum-admitted snapshot, and archive resources close before
either error returns.

The fixed producer emits neither archive nor member comments. RFC-0064 adds no
raw ZIP parser, general comment scanner, comment decoder, rewriting, repair,
workflow, producer, dependency, runtime API, or release authority. It is not a
general archive sandbox and is not a real public release observation.
Malformed structures that fail before CPython exposes either comment retain
the existing stable ZIP-data failure instead of an M81 comment error.

## M82 split-volume sample-member preflight

M82 rejects a central-directory disk-start value outside the fixed single-
volume sample profile. PKWARE defines that field as the disk on which a member
begins; CPython exposes it as `ZipInfo.volume`. A parser-exposed nonzero value
raises stable content-silent error `sample bundle uses a split-volume member`.

Complete release smoke finishes every established flag, descriptor, Unicode
Path, ZIP64, archive-comment, and member-comment pass first. It then checks
every `ZipInfo.volume` in a separate all-member pass before M77 decoded-name
policy, member metadata, exact inventory, staging, or member reads. Established
categories therefore retain archive-wide precedence. Owned source, checksum-
admitted snapshot, and archive resources close before the error returns.

The fixed producer emits volume zero for all 50 entries. RFC-0065 adds no raw
end-record parser, no local-header parser, no multi-volume assembler, no
neighboring-file discovery, workflow, producer, dependency, runtime API, or
release authority. It is not a general archive sandbox and is not a real
public release observation. M82 deferred end-record disk fields; M83 below
addresses only the conventional final record.

## M83 conventional archive disk-field preflight

M83 closes the remaining conventional end-record disk-field gap for the fixed
single-file sample profile. PKWARE defines current-disk and central-directory-
start disk numbers in the end-of-central-directory record. Supported CPython
3.12-3.14 parses but ignores those fields for an ordinary archive: patched
nonzero and `0xFFFF` fixtures still expose a volume-zero member and readable
payload.

After every established flag, descriptor, exact extra-field, archive/member-
comment, and member-volume pass completes, release smoke reads exactly the
final conventional 22-byte record from the owned checksum-admitted snapshot.
It requires the signature, zero comment length, and both disk fields equal to
zero, restores the previous snapshot position, and then proceeds to M77 name
policy. Either nonzero field raises stable content-silent error `sample bundle
uses unsupported archive disk fields` before metadata, exact inventory,
staging, or member reads. Structural mismatch uses the existing stable ZIP-
data error. Owned source, snapshot, and archive resources close first.

The fixed producer emits the conventional record at end of file with both
disk fields zero. RFC-0066 adds no ZIP64 end-record parser, end-record search,
central-directory/local-header parser, neighboring-volume discovery, or multi-
volume assembler. It does not resolve `0xFFFF` or classify actual ZIP64 volume
topology, is not a general archive sandbox, and is not a real public release
observation. Workflows, producer, dependencies, runtime API, and release
authority remain unchanged.

## M84 conventional archive entry-count preflight

M84 closes the next conventional end-record consistency gap for the fixed 50-
member sample profile. PKWARE defines current-disk and total-entry counts in
the end-of-central-directory record. Supported CPython 3.12-3.14 parses but
ignores both for an ordinary archive: zero, asymmetric, inflated, and
`0xFFFF` fixtures still expose the same readable central-directory members.

After every established member policy and M83 disk-field check completes,
release smoke reads exactly the final conventional 22-byte record from the
owned checksum-admitted snapshot. It requires both counts to equal
`len(archive.infolist())`, restores the previous snapshot position, and then
proceeds to M77 name policy. A mismatch raises stable content-silent error
`sample bundle archive entry counts are inconsistent` before metadata, exact
inventory, staging, or member reads. Structural mismatch retains the existing
stable ZIP-data error. Owned source, snapshot, and archive resources close
first.

The fixed producer emits 50 in both fields and exposes 50 parsed members.
RFC-0067 adds no ZIP64 end-record parser, sentinel resolution, end-record
search, central-directory/local-header parser, neighboring-volume discovery,
or multi-volume assembler. It is not a general archive sandbox and is not a
real public release observation. Workflows, producer, dependencies, runtime
API, and release authority remain unchanged.

## M85 conventional central-directory placement preflight

M85 narrows the fixed sample container to zero concatenation adjustment.
PKWARE defines conventional central-directory size and offset fields in
the end-of-central-directory record. Supported CPython 3.12-3.14 deliberately
computes a concatenation adjustment: one or eleven prepended bytes shift parsed
member header offsets and preserve a readable payload.

After every established policy through M84 completes, release smoke reads the
final conventional record through the shared position-restoring structural
helper. It requires the declared central-directory size plus offset to equal
the absolute offset of that final record, then proceeds to M77 name policy. A
nonzero adjustment raises stable content-silent error `sample bundle central
directory placement is inconsistent` before metadata, exact inventory,
staging, or member reads. Structural mismatch retains the existing stable ZIP-
data error. Owned source, snapshot, and archive resources close first.

The fixed producer starts at byte zero and satisfies the relationship exactly.
RFC-0068 adds no central-directory record parser, local-header parser, end-
record search, ZIP64 parser, prepended executable support, self-extracting
archive support, or multi-volume assembler. It is not a general archive
sandbox and is not a real public release observation. Workflows, producer,
dependencies, runtime API, and release authority remain unchanged.

## M86 first local-header placement preflight

M86 narrows the fixed sample profile after M85 without parsing local headers.
Supported CPython 3.12-3.14 reads archives with one or eleven leading bytes when
the central-directory relative local-header offset and end-record central-
directory offset are both updated. Those archives retain zero M85 concatenation
adjustment while the parser exposes an earliest `ZipInfo.header_offset` of one
or eleven.

After every established policy through M85 completes, release smoke requires
the minimum parser-exposed local-header offset to be zero, then proceeds to M77
name policy. A nonzero value raises stable content-silent error `sample bundle
first local header placement is inconsistent` before metadata, exact inventory,
staging, or member reads. Empty archives retain the established later exact-
inventory failure. Owned source, snapshot, and archive resources close first.

The fixed producer exposes 50 members and an earliest local-header offset of
zero. RFC-0069 adds no local-header parser, central-directory parser, inter-
member layout validator, signature classifier, prepended executable support,
or archive repair. It is not a general archive sandbox and is not a real public
release observation. Workflows, producer, dependencies, runtime API, and
release authority remain unchanged.

## M87 distinct local-header-offset preflight

M87 narrows the fixed sample profile after M86 without parsing local headers.
Supported CPython 3.12-3.14 exposes two central entries that identify one local
header as offsets `[0, 0]`. Reading the first entry succeeds, while reading the
alias later raises a local/central filename mismatch. Any overlap warning is
implementation-dependent and is not part of the M87 contract.

After every established policy through M86 completes, release smoke requires
all parser-exposed local-header offsets to be distinct, then proceeds to M77
name policy. A duplicate raises stable content-silent error `sample bundle
local header offsets are inconsistent` before metadata, exact inventory,
staging, or member reads. Empty and single-member parsed inventories satisfy
this aggregate check. Owned source, snapshot, and archive resources close
first.

The fixed producer exposes 50 members and 50 distinct local-header offsets.
RFC-0070 adds no local-header parser, central-directory parser, offset ordering/
bounds rule, inter-member layout validator, field-consistency validator,
signature classifier, or archive repair. It is not a general archive sandbox
and is not a real public release observation. Workflows, producer,
dependencies, runtime API, and release authority remain unchanged.

## M88 local-header-order preflight

M88 narrows the fixed sample profile after M87 without parsing local headers.
Supported CPython 3.12-3.14 returns a central-directory-only record swap in
that swapped entry order and exposes public local-header offsets `[46, 0]`;
both members remain readable. ZIP permits arbitrary file ordering generally,
so this is a producer-profile rule rather than a general validity claim.

After every established policy through M87 completes, release smoke requires
strictly increasing local-header offsets in parser-exposed archive order, then
proceeds to M77 name policy. A non-increasing pair raises stable content-silent
error `sample bundle local header offsets are out of order` before metadata,
exact inventory, staging, or member reads. M87 distinctness retains precedence.
Empty and single-member inventories satisfy the aggregate check. Owned source,
snapshot, and archive resources close first.

The fixed producer exposes 50 members with strictly increasing local-header
offsets. RFC-0071 adds no local-header parser, central-directory record parser,
offset bounds/contiguity rule, inter-member layout validator, or archive repair.
It is not a general archive sandbox and is not a real public release
observation. Workflows, producer, dependencies, runtime API, and release
authority remain unchanged.

## M89 local-header-offset bounds preflight

M89 narrows the fixed sample profile after M88 without parsing local headers.
Supported CPython 3.12-3.14 exposes a central pointer changed only to the
conventional central-directory offset as `[0, 94]`; the first payload remains
readable and the malformed member defers public `BadZipFile` until open.

After every established policy through M88 completes, release smoke requires
every parser-exposed local-header offset to remain strictly before the
conventional central directory, then proceeds to M77 name policy. An offset at
or after that boundary raises stable content-silent error `sample bundle local
header offsets are out of bounds` before metadata, exact inventory, staging, or
member reads. All earlier placement, distinctness, and ordering rules retain
precedence. Empty inventories satisfy the aggregate check. Owned source,
snapshot, and archive resources close first.

The fixed producer exposes all 50 local-header offsets below that boundary.
RFC-0072 adds no local-header parser, central-directory record parser, local-
record extent, adjacency, contiguity, or physical non-overlap rule, no inter-
member layout validator, and no archive repair. It is not a general archive
sandbox and is not a real public release observation. Workflows, producer,
dependencies, runtime API, and release authority remain unchanged.

## M90 local-header-signature preflight

M90 narrows the fixed sample profile after M89 without parsing local-header
fields. Supported CPython 3.12-3.14 exposes a central pointer shifted by one
byte as `[0, 47]`; the first payload remains readable and the malformed member
defers public `BadZipFile` until open.

After every established policy through M89 completes, release smoke reads four
bytes at every parser-exposed offset from the owned checksum-admitted snapshot.
Each must equal the fixed producer's four-byte local-header signature
`PK\x03\x04`. A mismatch or short read raises stable content-silent error
`sample bundle local header signature is inconsistent` before decoded names,
metadata, exact inventory, staging, or member reads. Earlier placement,
distinctness, ordering, and bounds policies retain precedence. Empty
inventories satisfy the aggregate check. Owned source, snapshot, and archive
resources close first.

This signature classifier adds no local-header field parser, central-directory
record parser, record-extent, adjacency, contiguity, payload-bound, or physical
non-overlap rule, no inter-member layout validator, and no archive repair. It
is not a general archive sandbox and is not a real public release observation.
Workflows, producer, dependencies, runtime API, and release authority remain
unchanged. RFC-0073 defines the complete boundary.

## M91 fixed local-header-prefix bounds preflight

M91 narrows the fixed sample profile after M90 without parsing local-header
fields. Supported CPython 3.12-3.14 exposes a parser-reported offset four bytes
before the conventional central directory when those bytes contain
`PK\x03\x04`; the earlier member remains readable and the malformed member
defers public `BadZipFile` until open.

Private complete release smoke uses the owned checksum-admitted snapshot to
read the conventional central-directory offset, then requires
`ZipInfo.header_offset + 30` to be no greater than that offset for every parsed
member. Thirty bytes is ZIP's fixed local-header prefix before its variable file
name and extra field. Failure raises stable content-silent error `sample bundle
local header prefixes are out of bounds` before decoded names, metadata, exact
inventory, staging, or reads. Empty archives retain their later inventory
failure, and the shared end-record reader restores the snapshot position.

This is one prefix-bound classifier. It adds no local-header field parser,
filename/extra-length interpretation, record-extent, payload-bound, adjacency,
contiguity, or physical non-overlap rule, no inter-member layout validator, and
no archive repair. It is not a general archive sandbox and is not a real public
release observation. Workflows, producer, dependencies, runtime API, and
release authority remain unchanged. RFC-0074 defines the complete boundary.

## M92 local-header variable-envelope bounds preflight

M92 narrows the fixed sample profile after M91 by reading only the two local
file-name and extra-field length declarations. Supported CPython 3.12-3.14
exposes a parser-reported second local-header offset of 46 before conventional
central-directory offset 94 when that header declares a 65,535-byte name. Both
signatures and fixed prefixes remain valid, the earlier member remains
readable, and the malformed member defers public `BadZipFile` until open.

Private complete release smoke reads the four length bytes from the owned
checksum-admitted snapshot and requires
`header_offset + 30 + file_name_length + extra_field_length` to be no greater
than the conventional central-directory offset for every parsed member.
Failure raises stable content-silent error `sample bundle local header
envelopes are out of bounds` before decoded names, metadata, exact inventory,
staging, or reads. Empty archives retain their later inventory failure, and
both snapshot readers restore the caller position.

This is one two-field envelope-bound classifier. It performs no local-name
comparison, extra-field parsing, field consistency check, complete local-record
or payload bound, next-header bound, adjacency, contiguity, physical non-
overlap rule, or inter-member layout validator, and no archive repair. It is
not a general archive sandbox and is not a real public release observation.
Workflows, producer, dependencies, runtime API, and release authority remain
unchanged. RFC-0075 defines the complete boundary.

## M93 local-header name consistency preflight

M93 narrows the fixed sample profile after M92 by reading each already bounded
local file-name. Supported CPython 3.12-3.14 accepts central names and offsets
when one same-length local name is changed, keeps an earlier member readable,
and defers public `BadZipFile` until the mismatched member opens.

Private complete release smoke reconstructs each parser-exposed
`ZipInfo.orig_filename` with UTF-8 when the central `flag_bits` language-
encoding bit is set and CP437 otherwise. It compares those expected bytes with
the declared local name from the owned checksum-admitted snapshot. A mismatch
raises stable content-silent error `sample bundle local header names are
inconsistent` before decoded-name policy, metadata, exact inventory, staging,
or reads. Empty archives retain their later inventory failure, and the helper
restores the caller's snapshot position.

This is one raw local-name consistency classifier. It performs no local-flag
comparison, extra-field comparison or parsing, local/central field-wide
consistency check, complete local-record or payload bound, next-header bound,
adjacency, contiguity, physical non-overlap rule, or inter-member layout
validator, and no archive repair. It is not a general archive sandbox and is
not a real public release observation. Workflows, producer, dependencies,
runtime API, and release authority remain unchanged. RFC-0076 defines the
complete boundary.

## M94 local-header flag consistency preflight

M94 narrows the fixed sample profile after M93 by reading the two-byte general-
purpose flag field from each already bounded local-header prefix. Exact CPython
3.12.13, 3.13.13, and 3.14.5 expose unchanged zero central flags and read both
payloads when only the second local encryption bit is set.

Private complete release smoke compares each little-endian local value with the
parser-exposed central `ZipInfo.flag_bits`. A mismatch raises stable content-
silent error `sample bundle local header flags are inconsistent` before
decoded-name policy, metadata, exact inventory, staging, or reads. Empty
archives retain their later inventory failure, and the helper restores the
caller's snapshot position.

This is one two-byte local-flag consistency classifier. It performs no local
compression-method comparison, no extra-field comparison or parsing, no
version/time/CRC/size comparison, no broad flag allowlist, no field-wide local/
central consistency check, no complete local-record or payload bound, no next-
header bound, and no adjacency, contiguity, physical non-overlap rule, or inter-
member layout validator. It is not a general archive sandbox and is not a real
public release observation. Workflows, producer, dependencies, runtime API,
and release authority remain unchanged. RFC-0077 defines the complete boundary.

## M95 local-header compression-method consistency preflight

M95 narrows the fixed sample profile after M94 by reading the two-byte
compression-method field from each already bounded local-header prefix. Exact
CPython 3.12.13, 3.13.13, and 3.14.5 expose unchanged central methods `[8, 8]`
and read both payloads when only the second local method changes from deflate
8 to stored 0.

Private complete release smoke compares each little-endian local value with the
parser-exposed central `ZipInfo.compress_type`. A mismatch raises stable
content-silent error `sample bundle local header compression methods are
inconsistent` before decoded-name policy, metadata, exact inventory, staging,
or reads. Empty archives retain their later inventory failure, and the helper
restores the caller's snapshot position.

This is one two-byte local-compression-method consistency classifier. It
performs no local extra-field comparison or parsing, no version/time/CRC/size
comparison, no method allowlist, no field-wide local/central consistency check,
no complete local-record or payload bound, no next-header bound, and no
adjacency, contiguity, physical non-overlap rule, or inter-member layout
validator. It is not a general archive sandbox and is not a real public release
observation. Workflows, producer, dependencies, runtime API, and release
authority remain unchanged. RFC-0078 defines the complete boundary.

## M96 local-header extra-field consistency preflight

M96 narrows the fixed sample profile after M95 by reading each local extra
field from the already bounded local-header envelope. Exact CPython 3.12.13,
3.13.13, and 3.14.5 retain central extras `feca02006f6b` and read both payloads
when only the second same-length local extra changes to `feca02006f21`.

Private complete release smoke uses the bounded local name and extra lengths to
read the local extra bytes, then compares them with public central
`ZipInfo.extra`. A mismatch raises stable content-silent error `sample bundle
local header extra fields are inconsistent` before decoded-name policy,
metadata, exact inventory, staging, or reads. Empty archives retain their later
inventory failure, and the helper restores the caller's snapshot position.

This is one bounded local-extra equality classifier. It adds no extra-field
semantics parser, no broad extra-field ban, no new field-ID policy, no
version/time/CRC/size or field-wide local/central comparison, no complete
local-record or payload bound, no next-header bound, and no adjacency,
contiguity, physical non-overlap rule, or inter-member layout validator. It is
not a general archive sandbox and is not a real public release observation.
Workflows, producer, dependencies, runtime API, and release authority remain
unchanged. RFC-0079 defines the complete boundary.

## M97 local-header extraction-version consistency preflight

M97 narrows the fixed sample profile after M96 by reading the two bytes at
each already bounded `ZipInfo.header_offset + 4`. Exact CPython 3.12.13,
3.13.13, and 3.14.5 retain central pairs `(20, 0)` and read both payloads when
only the second local extraction-version byte changes from 20 to 21.

Private complete release smoke compares those local bytes with public central
`ZipInfo.extract_version` and `ZipInfo.reserved`. A mismatch raises stable
content-silent error `sample bundle local header extraction versions are
inconsistent` before decoded-name policy, metadata, exact inventory, staging,
or reads. Empty archives retain their later inventory failure, and the helper
restores the caller's snapshot position.

This is one two-byte local-extraction-version consistency classifier. It adds
no supported-version allowlist, minimum extractor-capability rule,
reserved-byte policy, time/CRC/size comparison, field-wide local/central
comparison, complete local-record or payload bound, next-header bound, or
adjacency, contiguity, physical non-overlap rule, or inter-member layout
validator. It is not a general archive sandbox and is not a real public
release observation. Workflows, producer, dependencies, runtime API, and
release authority remain unchanged. RFC-0080 defines the complete boundary.

## M98 local-header timestamp consistency preflight

M98 narrows the fixed sample profile after M97 by reading the four bytes at
each already bounded `ZipInfo.header_offset + 10`. Exact CPython 3.12.13,
3.13.13, and 3.14.5 retain central tuples `(2026, 8, 23, 4, 6, 8)` and read
both payloads when only the second local time's low byte changes from `c4` to
`e4`.

Private complete release smoke reconstructs the corresponding central DOS
time/date bytes from public `ZipInfo.date_time` and requires exact equality.
A mismatch raises stable content-silent error `sample bundle local header
timestamps are inconsistent` before decoded-name policy, metadata, exact
inventory, staging, or reads. Empty archives retain their later inventory
failure, and the helper restores the caller's snapshot position.

This is one four-byte local-timestamp consistency classifier. It is no
timestamp semantics validator and performs no timezone or UTC conversion,
wall-clock comparison, calendar validation, reproducibility rule, extended-
timestamp interpretation, CRC/size comparison, field-wide local/central
comparison, complete local-record or payload bound, next-header bound, or
inter-member layout validator. It is not a general archive sandbox and is not
a real public release observation. Workflows, producer, dependencies, runtime
API, and release authority remain unchanged. RFC-0081 defines the complete
boundary.

## M99 local-header CRC-32 consistency preflight

M99 narrows the fixed sample profile after M98 by reading the four bytes at
each already bounded `ZipInfo.header_offset + 14`. Exact CPython 3.12.13,
3.13.13, and 3.14.5 retain central CRCs `[3724039362, 2868864084]` and read
both payloads when only the second local CRC changes from `2868864084` to
`2868864085`.

The local bytes must equal public central `ZipInfo.CRC` encoded as an unsigned
four-byte little-endian value. Mismatch raises stable content-silent error
`sample bundle local header CRC-32 values are inconsistent` before decoded
names, metadata, exact inventory, staging, or reads. Empty archives retain
their later inventory failure, and the helper restores the caller's snapshot
position.

This is one four-byte local-CRC-32 consistency classifier. It performs no CRC
recomputation, payload-integrity certification, polynomial selection,
compressed/uncompressed size comparison, field-wide local/central comparison,
complete local-record bound, payload or next-header bound, gap, adjacency,
contiguity, physical non-overlap rule, or inter-member layout validator. It is
not a general archive sandbox and is not a real public release observation.
Workflows, producer, dependencies, runtime API, and release authority remain
unchanged. RFC-0082 defines the complete boundary.

## M100 local-header compressed-size consistency preflight

M100 narrows the fixed sample profile after M99 by reading the four bytes at
each already bounded `ZipInfo.header_offset + 18`. Exact CPython 3.12.13,
3.13.13, and 3.14.5 retain both central compressed sizes at `11` and read both
payloads when only the second local compressed size changes from `11` to `12`.

The local bytes must equal public central `ZipInfo.compress_size` encoded as an
unsigned four-byte little-endian value. Mismatch raises stable content-silent
error `sample bundle local header compressed sizes are inconsistent` before
decoded names, metadata, exact inventory, staging, or reads. Empty archives
retain their later inventory failure, and the helper restores the caller's
snapshot position.

This is one four-byte local-compressed-size consistency classifier. It performs
no decompression or recompression, no uncompressed-size comparison, no
compression-ratio or archive-bomb policy, no payload-integrity certification,
no field-wide local/central comparison, no complete local-record bound, no
payload or next-header bound, and no gap, adjacency, contiguity, physical non-
overlap rule, or inter-member layout validator. It is not a general archive
sandbox and is not a real public release observation. Workflows, producer,
dependencies, runtime API, and release authority remain unchanged. RFC-0083
defines the complete boundary.

## M101 local-header uncompressed-size consistency preflight

M101 narrows the fixed sample profile after M100 by reading the four bytes at
each already bounded `ZipInfo.header_offset + 22`. Exact CPython 3.12.13,
3.13.13, and 3.14.5 retain both central uncompressed sizes at `9` and read both
payloads when only the second local uncompressed size changes from `9` to `10`.

The local bytes must equal public central `ZipInfo.file_size` encoded as an
unsigned four-byte little-endian value. Mismatch raises stable content-silent
error `sample bundle local header uncompressed sizes are inconsistent` before
decoded names, metadata, exact inventory, staging, or reads. Empty archives
retain their later inventory failure, and the helper restores the caller's
snapshot position.

This is one four-byte local-uncompressed-size consistency classifier. It
performs no decompression or recompression, no payload-content read during
preflight, no compression-ratio policy, no archive-bomb classification, no
payload-integrity certification, no field-wide local/central comparison, no
complete local-record bound, no payload or next-header bound, and no gap,
adjacency, contiguity, physical non-overlap rule, or inter-member layout
validator. It is not a general archive sandbox and is not a real public release
observation. Workflows, producer, dependencies, runtime API, and release
authority remain unchanged. RFC-0084 defines the complete boundary.

## M102 compressed-payload upper-bound preflight

M102 combines established ordered offsets, the conventional directory boundary,
bounded local envelopes, and matching compressed sizes. Exact CPython 3.12.13,
3.13.13, and 3.14.5 admit matching local/central sizes `[12, 11]` when the
first calculated payload end is byte `54` and the next local header begins at
`53`; only the first later member read raises `BadZipFile`, while the second
payload remains readable.

Each nonfinal compressed payload end must be no greater than the next local-
header offset; the final end must be no greater than the conventional central-
directory offset. Overlap raises stable content-silent error `sample bundle
member payloads are out of bounds` before decoded names, metadata, exact
inventory, staging, or reads. Empty archives retain their later inventory
failure, and the helper restores the caller's snapshot position.

This is one compressed-payload upper-bound classifier. It performs no
decompression or recompression, no payload-content read, adds no exact-
contiguity requirement, no gap or adjacency ban, no compression-ratio or
archive-bomb policy, and no payload-integrity certification. It is not a
complete inter-member layout validator, not a general archive sandbox, and not
a real public release observation. Workflows, producer, dependencies, runtime
API, and release authority remain unchanged. RFC-0085 defines the complete
boundary.

## M103 exact compressed-payload contiguity preflight

M103 builds on M102's proven upper bound. Exact CPython 3.12.13, 3.13.13, and
3.14.5 admit a one-byte inter-member gap when conventional offsets are updated:
gap widths remain `[1, 0]`, local offsets are `[0, 59]`, payload ends are
`[58, 117]`, and both payloads remain readable.

Each compressed payload end must equal the next local-header offset or, for the
final member, the conventional central-directory offset. A shorter extent
raises stable content-silent error `sample bundle member payloads are not
contiguous` before decoded names, metadata, exact inventory, staging, or reads.
M102 retains precedence for overlap, empty archives retain their later inventory
failure, and the helper restores the caller's snapshot position.

This exact compressed-payload contiguity preflight is one compressed-payload
equality classifier. It performs no decompression or recompression, no payload-
content read, no CRC recomputation, no compressed-stream interpretation, and no
payload-integrity certification. It does not parse central records or payload
bytes, is not a general archive sandbox, and is not a real public release
observation. Workflows, producer, dependencies, runtime API, and release
authority remain unchanged. RFC-0086 defines the complete boundary.

## M104 empty sample-member extra-field profile preflight

PKWARE defines member extra fields as an extensibility mechanism, and supported
CPython exposes central bytes through public `ZipInfo.extra` while retaining
uninterpreted field bytes. Exact CPython 3.12.13, 3.13.13, and 3.14.5 each
retain equal local/central `feca02006f6b` fields and read both fixture payloads.
The fixed
50-member LudoWeave producer emits no member extra fields.

After established Unicode Path, ZIP64, local/central consistency, local-record
bounds, payload bounds, and contiguity checks, every parsed sample member must
have empty public central `ZipInfo.extra`. A non-empty value raises stable
content-silent error `sample bundle contains an unsupported extra field` before
decoded-name policy, metadata, exact inventory, staging, or reads. Existing
specific errors and M96/M102/M103 layout policy retain precedence, while empty
archives retain their later exact-inventory failure.

This empty sample-member extra-field profile preflight is one central-extra
emptiness classifier. It adds no extra-field semantics parser, field-ID
registry, payload-content read, decompression, recompression, CRC validation,
archive repair, or general ZIP validity claim. It is not a general archive
sandbox and is not a real public release observation. Workflows, producer,
dependencies, runtime API, and release authority remain unchanged. RFC-0087
defines the complete boundary.

## M105 zero sample-member general-purpose-flag profile preflight

PKWARE assigns semantic meaning to selected general-purpose flag bits and
reserves or leaves others unused. Supported CPython exposes the central value
through public `ZipInfo.flag_bits` and admits an otherwise valid deflated member
whose matching local and central headers carry currently unused bit 7. Exact
CPython 3.12.13, 3.13.13, and 3.14.5 each retain value `128` and read both
fixture payloads. The fixed 50-member LudoWeave producer emits only value zero.

After established specific-flag, local/central consistency, local-record bounds,
payload-layout, and M104 extra-field checks, every parsed sample member must
have public central `ZipInfo.flag_bits == 0`. A nonzero value raises stable
content-silent error `sample bundle contains unsupported general-purpose flags`
after decoded-name/member-metadata policy and before exact inventory, staging,
or reads. Unsupported-codec and nonportable-path diagnostics therefore retain
their established precedence. Encryption, data-descriptor, enhanced-deflate,
compressed-patch, local-flag
consistency, payload-layout, and M104 errors retain precedence, while empty
archives retain their later exact-inventory failure.
M76 remains method-scoped to enhanced deflate; M105 then rejects any residual
nonzero fixed-producer flag, including bit 4 on a stored member.

This zero sample-member general-purpose-flag profile preflight is one central-
flag zero-profile classifier. It adds no flag-semantics parser, bit registry,
raw record parser, payload-content read, decompression, recompression, CRC
validation, archive repair, or general ZIP validity claim. It does not assert
that every nonzero flag is malformed or unsafe outside this fixed producer. It
is not a general archive sandbox and is not a real public release observation.
Workflows, producer, dependencies, runtime API, and release authority remain
unchanged. RFC-0088 defines the complete boundary.

## M106 zero sample-member extraction-version reserved-byte profile preflight

Python documents public central `ZipInfo.reserved` as required to be zero, and
CPython's fixed `ZipInfo` writer default is zero. Exact CPython 3.12.13,
3.13.13, and 3.14.5 nevertheless each expose a matching local/central value of
one and read both fixture payloads. The fixed 50-member LudoWeave producer
emits only value zero.

After M97 has established local/central extraction-version-pair equality and
after the M103 payload, M104 extra-field, member-metadata, and M105 flag-profile
checks, every parsed sample member must have public central
`ZipInfo.reserved == 0`. A nonzero value raises stable content-silent error
`sample bundle has a nonzero extraction-version reserved byte` before exact
inventory, staging, or reads. Established local mismatch, payload-layout,
extra-field, unsupported-codec, nonportable-path, and flag-profile errors retain
precedence. Empty archives retain their later exact-inventory failure.

This zero sample-member extraction-version reserved-byte profile preflight is
one central-reserved zero-profile classifier. It adds no extraction-version
semantics parser, supported-version allowlist, raw record parser, payload-
content read, decompression, recompression, archive repair, or general ZIP
validity claim. It is not a general archive sandbox and is not a real public
release observation. No workflow, producer, dependency, runtime API, or release
authority changes. RFC-0089 defines the complete boundary.

## M107 exact sample-member extraction-version profile preflight

PKWARE assigns extraction version 2.0 to Deflate, Python exposes the public
central value as `ZipInfo.extract_version`, and CPython's fixed writer default
is `20`. Exact CPython 3.12.13, 3.13.13, and 3.14.5 nevertheless each expose a
matching local/central value of `21` and read both fixture payloads. The fixed
50-member LudoWeave producer emits only pair `(20, 0)`.

After M97 has established local/central pair equality and after payload-layout,
extra-field, member-metadata, M105 flag, and M106 reserved-byte checks, every
parsed sample member must have public central `ZipInfo.extract_version == 20`.
Any other value raises stable content-silent error `sample bundle has an
unsupported extraction version` before exact inventory, staging, or reads.
Established local mismatch, layout, extra-field, codec, path, flag, and
reserved-byte errors retain precedence. Empty archives retain their later exact-
inventory failure.

This exact sample-member extraction-version profile preflight is one central-
extraction-version exact-profile classifier. It adds no general extraction-
version semantics parser, feature-capability evaluator, raw record parser,
payload-content read, decompression, recompression, archive repair, or general
ZIP validity claim. It is not a general archive sandbox and is not a real public
release observation. No workflow, producer, dependency, runtime API, or release
authority changes. RFC-0090 defines the complete boundary.

## M108 exact sample-member creation-version profile preflight

PKWARE defines the lower byte of `version made by` as the ZIP specification
version supported by the encoding software. Python exposes the public central
value as `ZipInfo.create_version`, and CPython's fixed writer default is `20`.
Exact CPython 3.12.13, 3.13.13, and 3.14.5 nevertheless each expose central
value `21` and read an otherwise valid fixture payload. The fixed 50-member
LudoWeave producer emits only pair `(create_version, create_system) == (20,
3)`.

After established local-header, payload-layout, extra-field, member-metadata,
M105 flag, M106 reserved-byte, and M107 extraction-version checks, every parsed
sample member must have public central `ZipInfo.create_version == 20`. Any other
value raises stable content-silent error `sample bundle has an unsupported
creation version` before exact inventory, staging, or reads. Established
local-header, layout, metadata, flag, reserved-byte, and extraction-version
errors retain precedence. Empty archives retain their later exact-inventory
failure.

This exact sample-member creation-version profile preflight is one central-
creation-version exact-profile classifier. It adds no general creation-version
semantics parser, producer-capability evaluator, attribute-host policy, raw
record parser, payload-content read, decompression, recompression, archive
repair, or general ZIP validity claim. It is not a general archive sandbox and
is not a real public release observation. No workflow, producer, dependency,
runtime API, or release authority changes. RFC-0091 defines the complete
boundary.

## M109 zero sample-member internal-attribute profile preflight

PKWARE defines central internal file attributes as a two-byte advisory field:
bit zero marks apparent text, bit one marks a mainframe variable-record control
field, and other bits are reserved or unused. Python exposes the complete
public central value as `ZipInfo.internal_attr`, and CPython initializes it to
zero. Exact CPython 3.12.13, 3.13.13, and 3.14.5 nevertheless each expose value
`1` and read an otherwise valid fixture payload. The fixed 50-member LudoWeave
producer emits only zero.

After established local-header, payload-layout, extra-field, member-metadata,
and M105-M108 profile checks, every parsed sample member must have public
central `ZipInfo.internal_attr == 0`. Any other value raises stable content-
silent error `sample bundle has unsupported internal attributes` before exact
inventory, staging, or reads. Established local-header, layout, metadata, flag,
reserved-byte, extraction-version, and creation-version errors retain
precedence. Empty archives retain their later exact-inventory failure.

This zero sample-member internal-attribute profile preflight is one central-
internal-attribute exact-profile classifier. It adds no text/binary content
interpretation, record-control semantics parser, supported-bit mask, external-
attribute or host policy, raw record parser, payload-content read,
decompression, recompression, archive repair, or general ZIP validity claim.
It is not a general archive sandbox and is not a real public release
observation. No workflow, producer, dependency, runtime API, or release
authority changes. RFC-0092 defines the complete boundary.

## M110 retain sample-member timestamp compatibility

ZIP member timestamps are stored as MS-DOS calendar fields with two-second
resolution rather than an absolute UTC instant. Python exposes the decoded
public central value as the six-part `ZipInfo.date_time` tuple. Exact CPython
3.12.13, 3.13.13, and 3.14.5 each expose alternate valid timestamps and read
the otherwise valid fixture payload. The fixed 50-member producer emits only
`(1980, 1, 1, 0, 0, 0)`.

An exact verifier profile for the producer tuple passed its 21 focused
assertions but caused 22 established architecture regressions across bounded
extraction, portable paths, atomic staging, exact inventory, owned snapshots,
and content-silent failure behavior. Those fixtures use supported standard-
library writer behavior and remain valid. The exact profile was therefore
removed rather than rewriting historical compatibility contracts.

M98 local/central timestamp consistency remains the verifier boundary; M104's
empty-extra-field profile remains unchanged; and the producer retains its fixed
reproducible timestamp. M110 is one central-timestamp compatibility decision,
not timestamp admission logic. It performs no timezone or UTC conversion,
wall-clock lookup, extra-field timestamp interpretation, raw record parsing, or
payload-content read. It is not a general ZIP validity claim, not a general
archive sandbox, and not a real public release observation. No workflow,
verifier, producer, dependency, runtime API, or release-authority changes.
RFC-0093 defines the complete boundary.

## M111 retain sample-member permission compatibility

ZIP external attributes are interpreted relative to the creating host. Python
exposes the complete public value as `ZipInfo.external_attr`; CPython's
convenience writer emits mode `0600` without a file-type marker on Windows,
while the fixed LudoWeave producer emits UNIX regular-file mode `0100644`.
Exact CPython 3.12.13, 3.13.13, and 3.14.5 expose multiple regular-file
permission variants and read every fixture payload.

M65 remains the verifier boundary. It reads the upper 16 bits, rejects encoded
symlinks, rejects any other encoded non-regular type, and admits either a
missing type marker or a regular-file marker. Permission bits do not affect
admission once that file-type rule passes. Extraction creates new owned files
and performs no permission restoration.

M111 therefore retains sample-member permission compatibility. It is one
permission-bit compatibility decision, not a new classifier. It adds no exact
external-attribute profile, host-system semantics expansion, permission
allowlist, chmod operation, or payload-content read. It is not a general ZIP
validity claim, not a general archive sandbox, and not a real public release
observation. No workflow, verifier, producer, dependency, runtime API, or
release-authority changes. RFC-0094 defines the complete boundary.

## M112 retain sample-member creating-system compatibility

PKWARE defines the upper `version made by` byte as the host system with which
external attributes are compatible. Python exposes it as
`ZipInfo.create_system`; CPython initializes it to `0` on Windows and `3`
elsewhere. The fixed producer explicitly emits host `3` for every member.

M108 demonstrated that an exact UNIX-only verifier rule would break 54
established Windows-created compatibility fixtures. M111 separately confirmed
that M65's encoded file-type boundary remains sufficient for the current
owned-file extraction design, which does not restore archive permissions or
other host-specific attributes.

M112 therefore retains sample-member creating-system compatibility. It is one
host-marker compatibility decision, not a new classifier. It adds no creating-
system allowlist, no host-specific external-attribute interpretation, and no
payload-content read. M65's symlink/non-regular rejection remains unchanged,
and the producer remains reproducible at host `3`. This is not a general ZIP
validity claim, not a general archive sandbox, and not a real public release
observation. No workflow, verifier, producer, dependency, runtime API, or
release-authority changes. RFC-0095 defines the complete boundary.

## M113 retain sample-member compression-method compatibility

PKWARE defines compression as optional, method `0` as stored, and method `8`
as deflated. Python exposes both through public `ZipInfo.compress_type`, reads
both on every supported runtime, and defaults new archives to stored. The fixed
sample producer explicitly emits deflate for every member.

M64 already admits exactly stored and deflated methods before size bounds and
extraction. M95 independently requires each bounded local-header compression
method to equal the parser-exposed central method. Exact CPython 3.12.13,
3.13.13, and 3.14.5 preserve and read both methods, while complete stored,
deflated, and mixed-method bundles pass every established policy.

M113 therefore retains sample-member compression-method compatibility. It is
one compression-method compatibility decision, not a new classifier. It adds
no exact deflate-only profile, no new decompressor, recompression, compression-
ratio policy, or payload-content read. M64's allowlist and M95's consistency
boundary remain unchanged, and the producer remains reproducible with deflate.
This is not a general ZIP validity claim, not a general archive sandbox, and
not a real public release observation. No workflow, verifier, producer,
dependency, runtime API, or release-authority changes. RFC-0096 defines the
complete boundary.

## M114 retain sample-member compression-level non-observability

PKWARE's DEFLATE option bits distinguish broad normal, maximum, fast, and
super-fast categories; they do not encode Python's exact numeric writer
setting. Python's `compresslevel` controls writing. CPython 3.13 added public
`ZipInfo.compress_level` for writer configuration, while reopened members on
exact CPython 3.12.13, 3.13.13, and 3.14.5 expose no recovered exact level.

Supported-runtime probes requested levels `0`, `1`, `6`, and `9`. Every
reopened member retained method `8`, extraction version `20`, zero flags, and
readable payload bytes while its compression level remained unknown. In the
controlled probe, levels `6` and `9` also produced identical archive bytes.
The fixed producer continues to request level `9`, but its 50 reopened members
likewise provide no exact level metadata.

M114 therefore retains sample-member compression-level non-observability. It
is one compression-level non-observability decision, not a new classifier. The
verifier adds no exact level-9 verifier profile and no inferred compressor level
from attributes, compressed bytes, or sizes. M105's zero-flag profile, M113's
method policy, and the producer's explicit writer setting remain unchanged.
There is no payload-content read. This is not a general ZIP validity claim, not
a general archive sandbox, and not a real public release observation. No
workflow, verifier, producer, dependency, runtime API, or release-authority
changes. RFC-0097 defines the complete boundary.

## M115 sample-bundle byte-reproducibility scope

The fixed sample producer already normalizes inventory, member order,
timestamps, host marker, permissions, method, and writer compression level.
Exact Windows CPython 3.12.13, 3.13.13, and 3.14.5 probes each produced two
byte-identical bundles within the same resolved environment. CPython 3.12 and
3.13 used zlib 1.3.1 and emitted the same archive identity; CPython 3.14 used
zlib-ng 2.2.4 through its zlib-compatible API and emitted a different archive
identity. This is deterministic implementation variance, not within-
environment nondeterminism.

M115 therefore scopes sample-bundle byte reproducibility to the release
environment. The official producer remains the existing baseline CPython 3.12
release job, and the enforceable claim is repeated production within that one
fixed resolved job environment. Supported CPython 3.12-3.14 runtimes remain
compatible consumers and local staging environments; support does not imply
cross-runtime producer-byte identity.

This is one sample-bundle reproducibility-scope decision. It adds no cross-
runtime byte-identity claim, compressor allowlist, runtime rejection,
compressor-identity manifest field, recompression, or new reproducibility
verifier. The fixed producer remains explicit at `compresslevel=9`; RFC-0021's
wheel/sdist same-source, same-job boundary remains separate and unchanged.
There is no workflow, allocation, producer, verifier, dependency, runtime API,
or release-authority change. This is not a general reproducible-build claim and
is not a real public release observation. RFC-0098 defines the complete
boundary.

## M116 sample-bundle semantic-portability boundary

M115 distinguishes repeatable bytes inside one fixed producer environment from
cross-runtime byte identity. M116 separately asks whether the supported runtime
implementations preserve the fixed sample bundle's semantic source tree.
PKWARE assigns method `8` to Deflate, and Python's `ZIP_DEFLATED` reader uses
the available zlib-compatible implementation.

Exact Windows CPython 3.12.13, 3.13.13, and 3.14.5 produced the fixed bundle.
Every runtime then consumed all three outputs through the complete sample
extraction boundary. All nine producer-consumer combinations passed every
established metadata, layout, inventory, ownership, and bounded-read check and
extracted the same 50 files. The 3.12/3.13 zlib archive and the different 3.14
zlib-ng archive therefore share the proven semantic result without sharing a
digest.

M116 separates sample-bundle semantic portability from byte identity. This is
one sample-bundle semantic-portability decision recording exact Windows cross-
runtime producer-consumer compatibility. It adds no alternate compression
method, new decoder, recompression, payload transformation, runtime branch,
digest allowlist, cross-runtime byte-identity claim, or cross-platform proof.
M64's stored/deflated policy, M95's local/central agreement, M113's method
compatibility, M114's level non-observability, M115's byte-reproducibility
scope, and every complete-release diagnostic remain unchanged.

There is no workflow, allocation, producer, verifier, dependency, runtime API,
or release-authority change. This is not a general ZIP interoperability claim
and is not a real public release observation. RFC-0099 defines the complete
boundary.

## M117 free-threaded serial-compatibility boundary

PEP 779 moved free-threaded CPython to officially supported but still optional
Phase II in Python 3.14. That interpreter-level status does not make application
objects concurrently safe. Python's free-threading guide continues to require
explicit object/thread discipline, and uv requires or permits a free-threaded
variant selection such as `3.14t`.

LudoWeave retains standard GIL CPython as the supported baseline for CPython
3.12-3.14. Engine, world, render, platform, audio, and agent lifecycles remain
single-owner contracts. The GIL is not an ownership mechanism: the engine stores
its creating thread identity and rejects lifecycle calls from another thread
before changing state.

An exact Windows CPython 3.14.5t installed-wheel serial compatibility probe ran
with `Py_GIL_DISABLED == 1` and the GIL disabled at runtime. Version and doctor
passed; 120 virtual ticks and frames completed in 2,000,000,000 nanoseconds;
close completed; and a worker-thread lifecycle call retained stable
`engine.wrong_thread`. The installed-wheel headless example reproduced the same
deterministic summary.

M117 records one free-threaded serial-compatibility decision. It is not a
support promise and makes no concurrent-safety claim. It adds no graphics/wgpu
evidence, performance result, parallel execution, cross-platform free-threaded
evidence, extension compatibility, new lock, runtime build branch, workflow,
allocation, dependency, version, runtime package/API, or release-authority
change. It is not a real public release observation. RFC-0100 defines the
complete boundary.

## M119 scene transaction-planning boundary

M119 introduces a narrow downward dependency from `ludoweave.scene` to the
existing asset identity, core error, ECS schema, and world command contracts.
Scene code may depend on `assets`, `core`, `ecs`, `world`, and itself. It may
not depend on application composition, rendering, tools, providers, or samples.
The architecture checker enforces that direction and keeps backend objects out
of the scene surface.

The `ludoweave.scene/1` versioned data-only scene document is normalized and
bounded before planning. The planner resolves component names only through its
injected `ComponentRegistry`, validates or migrates values with existing schema
code, and emits ordinary `entity.spawn` commands in canonical local-ID order.
There is no scene-specific world mutation path. Receipt aliases return the
local-ID-to-runtime-entity mapping, and the compiler-owned `SceneNode`
component records local provenance in ECS authority. Canonical runtime state
remains in the world store.

Documents and plans are immutable caller-owned values. Compilation is pure
planning with no file I/O and no owned resource to close. Transaction service
ownership, owner-thread rules, staging, rejection, and commit remain unchanged.
Unknown schemas, incompatible component data, reserved provenance injection,
or missing `SceneNode` registration fail before authority mutation.

This slice has no prefab inheritance, no live update or reimport behavior, no
runtime `EntityRef` facade, no asset loading, no arbitrary Python graph or
import, no renderer leakage, no dependency, and no workflow or hosted runner
change. RFC-0102 defines the data/schema rationale and complete non-scope.

## M120 prefab fragment planning boundary

M120 remains inside the existing `ludoweave.scene` downward dependency rule.
The prefab module depends only on the established asset identity, core error,
ECS schema, scene document/planner, canonical JSON, and world command
contracts. It does not import application composition, rendering, tools,
providers, samples, file/path loaders, or external dependencies.

`ludoweave.prefab/1` reuses an exact M119 scene fragment below a distinct
prefab identity. `ludoweave.prefab-instance/1` is a detached instance intent:
one exact source ID, one instance ID, and canonical schema-aware overrides
against stable local entity/component pairs. Override decoding is bounded and
duplicate-free. Planning accepts only the registered current version for each
non-empty field replacement, migrates base values first, and validates the
complete merged component before producing a transaction.

The compiler adds ordinary canonical `PrefabNode` provenance, then delegates
to M119. It creates no privileged mutation path and no new persistent
operation: the plan contains ordinary `entity.spawn` commands, and receipt
aliases return the local-ID-to-runtime-entity mapping. Canonical runtime state
remains in the world store. Source fragments, overrides, and plans are
immutable caller-owned data; no runtime source-instance graph exists and
source changes never silently mutate existing entities.

Composition is deliberately one-level. M120 has no nested prefab inheritance,
variant chain, parameter expression, structural override, file I/O, asset
loading, live update, reimport, write-back, runtime `EntityRef`, global
registry, arbitrary import/evaluation, dependency, root export, workflow, or
hosted allocation. RFC-0103 records the standards comparison and complete
boundary.

## M121 project-confined scene file loading boundary

M121 keeps filesystem authority in the existing `ludoweave.tools` composition
root. `HeadlessProject.load_scene()` accepts one project-relative string and an
exact immutable `SceneLimits`. It delegates path parsing, strict resolution,
root containment, regular-file checking, descriptor opening, and both metadata
and handle byte caps to the established M2 reader. Only after the handle is
closed are the detached bytes passed downward to `SceneDocument.from_json()`.
The scene package remains path- and transport-agnostic; its M119/M120 sources
are unchanged.

The result is a detached immutable `ludoweave.scene/1` document. Loading owns no
persistent file handle, source cache, watcher, world, renderer, thread, or
closeable resource. It performs no world mutation. A later caller must
explicitly compile the document and apply the existing transaction, which is
where normal atomic receipt behavior begins. Asset dependencies remain logical
identities and are not resolved by this loader. Changing or deleting the source
file cannot mutate the already returned document or any runtime entity.

Unsafe paths fail with sanitized existing tools errors; unavailable,
non-regular, or oversized input fails before scene decoding. Malformed or
incompatible content retains the structured M119 `SceneError`. The method is a
synchronous caller-thread operation. Root confinement rejects resolved escapes,
but it is not a descriptor-confined, race-free sandbox against concurrent
hostile filesystem mutation.

M121 adds no directory discovery, prefab file loader, file URI, include/import
graph, arbitrary Python import or evaluation, source cache, live update,
reimport, write-back, remote access, operation, dependency, root API, workflow,
or hosted allocation. RFC-0104 records the external standards basis and exact
boundary.

## M122 project-confined prefab file loading boundary

M122 extends only the existing `ludoweave.tools` composition root.
`HeadlessProject.load_prefab()` and `load_prefab_instance()` each take one
project-relative string and exact immutable `PrefabLimits`. They reuse M121
path confinement, regular-file validation, sanitized failure context, metadata
size checks, and bounded descriptor reads before passing detached bytes to the
unchanged prefab decoders. The scene/prefab package remains filesystem- and
transport-agnostic.

Callers select two explicit files: one `ludoweave.prefab/1` source and one
`ludoweave.prefab-instance/1` instance. There is no implicit pairing.
`compile_prefab()` remains responsible for exact source identity matching,
schema-aware overrides, and deterministic transaction planning. Loading owns
no persistent handle, cache, watcher, world, renderer, or background resource,
and performs no world mutation. Only explicit transaction application produces
a receipt and changes canonical world state.

M122 adds no directory discovery, extension-driven routing, manifest lookup,
asset resolution, cache, live update, nested prefab inheritance, source
write-back, operation, dependency, root API, workflow, or hosted allocation.
The same cooperative-filesystem and concurrent hostile-mutation limitation as
M121 applies. RFC-0105 records the external comparison and exact boundary.

## M123 read-only source-check CLI boundary

M123 extends only `ludoweave.tools.cli`, the existing composition adapter.
`ludoweave source check PROJECT --scene FILE` loads one M119 document through
the M121 reader. `ludoweave source check PROJECT --prefab FILE --instance FILE`
loads two explicit files through the M122 readers and checks their exact
`prefab_id` relationship. Both modes emit canonical
`ludoweave.cli.source-check/1` summaries containing protocol/source identities,
canonical content hashes, and bounded counts. Host paths are never emitted.

This is source-structure preflight, not compilation. The command registers or
resolves no application component schema, creates no world/session, calls no
planner or transaction service, performs no world mutation, and produces no
receipt. Consequently it makes no claim that project-specific component names
or values can compile against a later registry. Asset dependencies remain
unresolved logical identities.

M123 adds no directory discovery, suffix routing, implicit pairing, manifest
lookup, cache, watcher, live update, write-back, arbitrary execution, remote
access, dependency, root export, provider, renderer, or workflow allocation.
The workflow and release jobs remain byte-unchanged. RFC-0106 records the
primary-source comparison and complete boundary.

## M124 explicit source-manifest boundary

M124 adds one focused contract inside `ludoweave.scene`:
`ludoweave.source-manifest/1`. A manifest has one stable ID and a bounded
nonempty list of immutable entries. An entry has a stable unique ID and names
either one normalized portable project-relative scene path or one explicit
prefab source/instance pair. Exact repeated references are rejected. Entries
normalize by ID, and canonical bytes supply the manifest identity used in
reports. The existing engine root remains unchanged.

`HeadlessProject.load_source_manifest()` uses the existing confined regular-
file reader and returns a detached value after closing the handle. The CLI's
`--manifest FILE` mode then invokes only the existing M121/M122 source readers
in manifest order. It emits canonical
`ludoweave.cli.source-manifest-check/1` JSON with no host path. Each source
result carries normalized content identity and bounded counts; totals are a
pure aggregation of those results.

The manifest is an explicit input list, not directory discovery, suffix
routing, an asset database, or a component registry. Checking creates no world
or session, calls no planner or transaction service, performs no compile or
world mutation, writes no project file, and produces no receipt. A later entry
failure emits no success document. Individual reads close deterministically,
but the filesystem is not snapshotted atomically; concurrent external changes
remain outside deterministic execution guarantees.

M124 adds no glob, recursion, implicit prefab pairing, dependency traversal,
asset loading, cache, watcher, live update, write-back, arbitrary execution,
remote access, persistent operation, dependency, lock, root export, version,
provider, renderer, workflow job, or workflow allocation. The existing CI and
release workflows remain byte-unchanged. RFC-0107 records the external
comparison, ownership, failure, and compatibility boundary.

## M125 source-integrity lock boundary

M125 adds one focused experimental contract inside `ludoweave.scene`:
`ludoweave.source-lock/1`. A lock binds one normalized M124 manifest ID and
canonical SHA-256 identity to a nonempty, entry-ID-ordered list. Each entry
contains its kind, accepted source protocol, stable source ID, and canonical
content identity. Prefab entries also contain the explicit instance protocol,
ID, and identity. The document contains no project root, manifest path, or
source path. The engine root remains unchanged.

`HeadlessProject.load_source_lock()` reuses the confined bounded regular-file
reader and returns a detached immutable value. `ludoweave source lock` computes
the current document through the unchanged M121-M124 readers and emits it only
to stdout. `ludoweave source verify` reads an expected lock, computes the
current document, and compares manifest identity, entry IDs, and fields in a
fixed order. Success emits `ludoweave.cli.source-lock-verify/1`; mismatch emits
no success document and reports only the first field plus optional entry ID.

The lock establishes repeatable content identity for accepted canonical JSON.
It is not an atomic filesystem snapshot: manifest, lock, scene, prefab, and
instance descriptors are separate sequential reads, so concurrent external
changes remain outside deterministic execution. SHA-256 here is an integrity
identity, not a signature, provenance, authenticity, authorization, or artifact
security proof.

M125 performs no import, compile, application schema registration/resolution,
asset or dependency load, cache, discovery, directory traversal, watcher,
reimport, live update, source write-back, world/session creation, command,
transaction, world mutation, or receipt. Dependencies, metadata, version,
engine-root exports, workflows, permissions, credentials, release authority,
jobs, and allocations remain unchanged. RFC-0108 records the external
comparison, ownership, failure, and compatibility boundary.

## M126 project-confined asset-manifest loading boundary

M126 retains the exact existing `ludoweave.assets/1` shape and asset pipeline.
The focused package adds `ASSET_MANIFEST_PROTOCOL` and tightening-only
`AssetManifestLimits`: 4 MiB of UTF-8 JSON, 4,096 asset entries, 256
dependencies per entry, and 128 scalar settings per entry. Exact fields,
unique logical URIs, declared dependencies, the acyclic graph, and existing
portable source validation remain required.

`AssetManifest.from_json()` decodes caller-owned bytes or text without file
I/O. `AssetManifest.load()` retains its path API, caps one opened handle, closes
it, and delegates to that decoder. Canonical bytes order entries by URI,
settings by key, and dependencies by URI. `HeadlessProject.load_asset_manifest()`
first applies the established confined regular-file reader and returns the
manifest with its pre-existing resolved project-root composition context. No
open descriptor is retained.

This is a loader-only boundary: there is no asset source read, no asset build,
no cache use or creation, no directory discovery, no source-manifest
integration, and no direct or transitive source-to-asset dependency check.
M126 also performs no import, decode of asset payloads, compile, watcher,
reimport, live update, write-back, world/session creation, command,
transaction, world mutation, or receipt. Dependencies, metadata, version,
engine-root exports, CLI, workflows, permissions, credentials, release
authority, jobs, and allocations remain unchanged. RFC-0109 records ownership,
failure, compatibility, and the deferred semantic-resolution boundary.

## M127 source-to-asset dependency-checking boundary

M127 connects only already-declared source dependencies to the already-
validated asset graph. `AssetManifest.dependency_closure()` accepts an exact
tuple of distinct `AssetUri` roots, requires every root to exist, follows the
bounded acyclic manifest graph, and returns one unique URI-sorted tuple that
includes the roots and every reachable dependency.

`ludoweave source assets PROJECT --manifest FILE --assets FILE` first checks
the explicit M124 source manifest and each project-confined scene or prefab,
then loads one explicit M126 asset manifest. Canonical
`ludoweave.cli.source-asset-check/1` output retains each entry's direct source
declarations separately from its resolved closure and reports only deterministic
manifest identities and aggregate counts. Missing roots fail in source-entry
order and URI order before any success output. All descriptors close inside
the existing synchronous readers; the project is unchanged.

The checker cannot infer actual asset use inside application-defined component
values. It does not require a source to redeclare indirect graph edges and has
no unused-asset rejection. It performs no asset source read, payload decode,
asset build, import, cache use or creation, component-registry resolution,
scene/prefab compile, world/session creation, command, transaction, world
mutation, receipt, write, discovery, watcher, reimport, or live update.
Separate sequential reads are not an atomic filesystem snapshot. Dependencies,
metadata, version, engine-root exports, workflows, permissions, credentials,
release authority, jobs, and allocations remain unchanged. RFC-0110 records
the direct/resolved distinction and complete non-scope.

## M128 asset-source lock boundary

M128 adds immutable `ludoweave.asset-source-lock/1` input identities without
entering the M4 asset build pipeline. The lock binds the SHA-256 of the current
canonical M125 source lock, the SHA-256 of the current canonical M126 asset
manifest, the unique URI-sorted M127 direct roots, and every resolved asset as
URI, kind, raw source-byte count, and raw source SHA-256. Empty roots and
entries are valid together. Roots must appear in the exact unique entries.

`AssetSourceLockLimits` can tighten the 1 MiB document, 4,096-root, and 4,096-
entry hard limits. Exact fields, duplicate-key rejection, canonical lowercase
SHA-256 text, frozen/slotted ownership, URI normalization, canonical encoding,
and content-silent verification precedence are enforced in the focused assets
package. The engine root remains unchanged.

`HeadlessProject.hash_relative()` applies the established portable project-
relative resolution, opens one regular file read-only with available no-follow
semantics, checks its size, streams SHA-256 in 64 KiB blocks, checks the limit
again as bytes arrive, and closes the descriptor. Asset-lock generation walks
the URI-sorted resolved closure sequentially with a 256 MiB source limit and
1 GiB accepted aggregate. It retains no payload bytes and emits no success
document before all sources succeed.

Verification compares source-lock identity, asset-manifest identity, roots,
entry URI set, then kind/hash/byte count. Failure includes only the first stable
field and optional logical URI. Paths, expected/actual hashes, and compared
sizes are absent. Stable inputs produce deterministic bytes, but separate
reads are not an atomic filesystem snapshot.

M128 is input identity only. There is no asset decode, no asset build, no
import, no cache read, no cache write, no artifact creation, no automatic
reimport, no watcher, no live update, no discovery, no unused-asset rejection,
no build-inclusion policy, no world/session, no mutation, and no receipt.
Dependencies, metadata, version, engine-root exports, workflows, permissions,
credentials, release authority, jobs, and allocations remain unchanged. There
is no workflow allocation. RFC-0111 records the full boundary.

## M129 deterministic asset build-plan boundary

M129 adds immutable `ludoweave.asset-build-plan/1` prospective work records.
Planning accepts only an exact M126 manifest and M128 lock whose canonical
manifest identity, roots, exact selected closure, and per-entry kinds agree.
The CLI first recomputes and verifies current M128 inputs, so an expected lock
mismatch prevents plan output.

The plan graph is the explicit M127 closure only. A deterministic iterative
topological pass emits each asset once after all of its direct dependencies;
the ready set is ordered by logical URI, avoiding insertion-order dependence.
Empty closures remain valid. A plan entry contains URI, kind, detached sorted
settings, source SHA-256 and byte count, sorted direct dependencies, and the
prospective cache key.

`ASSET_LOADER_PROTOCOL` gives a public focused-package name to the unchanged M4
loader identity. Both `AssetPipeline` and the pure planner use one internal
cache-key function over URI, kind, settings, source hash, loader protocol, and
ordered direct dependency keys. Existing cache-key bytes and artifact behavior
are unchanged. Strict plan decoding revalidates dependency order, rooted
closure, and every cache key.

M129 is plan identity only. There is no asset decode, no asset build, no cache
read, no cache write, no artifact creation, no import, no scheduler, no worker,
no discovery, no watcher, no live update, no source/project write, no world
mutation, and no receipt. Sequential M128 verification is not an atomic
filesystem snapshot. Dependencies, metadata, version, engine-root exports,
workflows, permissions, credentials, release authority, jobs, and allocations
remain unchanged. There is no workflow allocation. RFC-0112 records the full
boundary.

## M130 confined asset build-plan verification boundary

M130 adds no new plan schema. `HeadlessProject.load_asset_build_plan()` reads
one explicit project-relative M129 document through the established confined,
regular-file, no-follow, bounded descriptor path and delegates detached bytes
to strict `AssetBuildPlan.from_json()`. The loader owns closure and retains no
descriptor or path in the returned immutable value.

`AssetBuildPlan.verify()` accepts only an exact plan value. Construction has
already enforced protocol, loader, closure, order, and cache-key invariants;
verification then compares source-lock identity, manifest identity, roots,
entry URI sequence, and each entry field in deterministic order. Failures use
stable `asset_build_plan.mismatch` with only the first field and optional
logical URI. Compared hashes, sizes, settings, keys, and paths remain absent.

The `source asset-plan-verify` composition loads the saved plan, recomputes and
verifies current M128 inputs, regenerates the M129 plan, and compares before
one bounded success document. Separate source reads are still not an atomic
filesystem snapshot. No success bytes precede complete success and the project
is unchanged.

M130 performs no plan execution, asset decode, asset build, cache read, cache
write, artifact creation, import, scheduler, worker, discovery, watcher, live
update, source/project write, world mutation, or receipt. Dependencies,
metadata, version, engine-root exports, workflows, permissions, credentials,
release authority, jobs, and allocations remain unchanged. There is no
workflow allocation. RFC-0113 records the full boundary.

## M131 bounded in-memory asset plan execution boundary

M131 separates decoder execution from persistence. The focused asset package
accepts only an exact M129 plan and a tuple of frozen `AssetBuildInput` values
whose logical URI order exactly matches the plan. It preflights all source byte
counts, SHA-256 identities, per-source limits, and aggregate source limits
before invoking a decoder.

Decoder authority is closed to the existing built-in `AssetKind` values. PNG
reuses the bounded RGBA8 decoder; JSON uses the existing compact sorted
encoding; WGSL validates UTF-8; audio retains exact bytes. Settings remain
cache-key inputs and do not become a plugin or callback surface. Per-artifact
and aggregate decoded work are bounded. Payloads are local temporaries and are
not retained in the result.

The immutable `ludoweave.asset-build-result/1` document binds the canonical
plan hash, unchanged loader protocol, aggregate accepted/decoded byte counts,
and plan-ordered URI, kind, cache key, source byte count, artifact SHA-256, and
artifact byte count. No path or payload enters the result. Stable detached
inputs produce byte-identical result bytes.

The `source asset-build` composition performs M130 verification before it
acquires sources through the existing project-confined owned reader. The pure
executor owns no descriptor or filesystem object. No success bytes are emitted
before the complete result exists, and failures leave no partial external
state.

M131 performs no cache read, cache write, persisted artifact creation, project
write, atomic publication, scheduler, worker, process, thread, plugin or
decoder registration, discovery, watcher, import/reimport, live update,
renderer upload, world mutation, or receipt. Dependencies, metadata, version,
engine-root exports, workflows, permissions, credentials, release authority,
jobs, and allocations remain unchanged. There is no workflow allocation.
RFC-0114 records the full boundary.

## M132 verified local asset cache boundary

M132 makes payload retention and storage explicit. `materialize_asset_build_plan()`
uses the complete M131 preflight and decoder kernel but returns a frozen
`AssetBuildMaterialization` whose payload tuple exactly matches the result
entries. The unchanged `execute_asset_build_plan()` path still discards each
payload after hashing.

`AssetCacheStore` receives one caller-selected local root. Project composition
rejects equal, nested, or ancestor cache/project roots, so generated artifacts
cannot mutate or contain project state. The store retains only a resolved path;
it owns no persistent descriptor, thread, worker, or background lifecycle.

The layout separates content from action identity. `cas/HH/HASH` names payload
bytes by artifact SHA-256. `actions/HH/CACHE_KEY/entry.json` binds the existing
M4/M129 action key to exact canonical `ludoweave.asset-cache-entry/1` metadata.
Reads require an expected M131 result entry and recheck exact metadata, payload
size, and payload digest. A missing action is a miss; any observed partial,
aliased, malformed, or mismatched entry is corruption and is not repaired.

Publication flushes a destination-sibling staged CAS blob before replacement,
then stages canonical action metadata in a sibling directory. Atomic per-entry
action-directory replacement is the visibility point, so an action never
becomes visible before its blob. Equivalent existing content is verified and
reused without rewrite. Still-owned staging paths are cleaned on failure. A
late filesystem failure may retain only valid earlier entries or an inert
unreferenced CAS blob; M132 is not an atomic all-plan transaction.

The `source asset-cache` composition completes exact lock/plan verification,
detached source acquisition, and complete bounded materialization before cache
construction. Its `ludoweave.asset-cache-publish/1` result contains only plan,
logical artifact, and publication-status values; filesystem paths, staging
names, timestamps, and environment values are absent.

M132 has no remote cache, network, authentication, eviction, deletion, repair,
quota, discovery, watcher, reimport, scheduler, worker, process, thread, plugin,
decoder registration, renderer upload, world mutation, or receipt. There is no
project write, dependency, native/backend surface, engine-root export, version,
workflow, permission, credential, release authority, or CI change. RFC-0115
records the full boundary.

## M133 verified read-only asset cache lookup boundary

M133 separates cache read authority from M132 publication authority.
`AssetCacheStore(..., writable=False)` retains an explicit resolved root but
does not create it and rejects publication. A missing root is therefore an
empty read view rather than a filesystem effect. Project overlap rejection is
unchanged.

`load_action()` accepts one exact current `AssetBuildPlanEntry` and derives
only its action path from the already validated M4/M129 cache key. It never
discovers or enumerates unrelated actions. Missing action metadata is an exact
miss even when an unreferenced blob exists.

A present entry is untrusted bounded input. Its directory must contain exactly
one ordinary metadata file. Parsing uses strict UTF-8, rejects duplicate object
names and non-finite constants, requires the exact M132 field set and canonical
bytes, reconstructs the validated result entry, and matches URI, kind, cache
key, and source byte count to the current plan. The referenced ordinary CAS
file must match its declared byte count and SHA-256. Any present unreadable,
aliased, malformed, mismatched, or incomplete entry fails closed as corruption;
it is neither a miss nor a repair trigger.

`inspect()` applies that operation in canonical plan order and returns
`ludoweave.asset-cache-lookup/1` hit/miss evidence. Artifact identity appears
only for a verified hit. Cache paths, timestamps, staging names, and environment
values remain absent. Digest verification proves internal content integrity,
not provenance or authenticity of a malicious self-consistent local mapping.

The `source asset-cache-check` composition completes current lock and saved-
plan verification before opening the caller-selected cache read-only. It does
not acquire decoder inputs, materialize outputs, publish, delete, or modify the
project or cache. M133 has no cache-assisted execution, decoder bypass, remote
cache, network, authentication, eviction, repair, discovery, watcher, worker,
plugin, renderer upload, world mutation, receipt, dependency, version,
workflow, permission, credential, release authority, or CI change. RFC-0116
records the full boundary.

## M134 read-only cache-assisted asset realization boundary

`realize_asset_build_plan()` composes the unchanged M131 built-in decoder and
M133 exact-action lookup into one bounded in-memory result. It accepts only an
exact `AssetBuildPlan`, detached input tuple, `AssetCacheStore`, and tightening-
only execution limits. It owns no filesystem descriptor, worker, thread, or
background lifecycle.

The complete detached source tuple is validated for exact plan order, byte
count, SHA-256, and source limits before the first cache action read. The
realizer then resolves every plan action through M133 and verifies per-entry
and aggregate artifact limits for every hit before invoking any decoder. A
present corrupt later action therefore cannot cause an earlier miss to decode.

Only after that complete cache phase are exact misses decoded in canonical plan
order. Hit and decoded artifacts are merged into one immutable
`AssetBuildMaterialization`; its result remains byte-identical to uncached M131
materialization for the same verified inputs. Frozen
`ludoweave.asset-build-realization/1` evidence adds only `hit` or `decoded`
status and aggregate counts. It contains no payload, path, environment value,
or cache history.

The `source asset-realize` composition completes current lock and saved-plan
verification and project-confined source acquisition before opening the cache
read-only. A missing cache remains absent. Success writes only the canonical
report to stdout. A failure discards in-memory candidates and emits no success
bytes. There is no automatic cache publication, cache or project mutation,
remote cache, network, discovery, plugin, worker, renderer upload, world
mutation, receipt, dependency, version, workflow, permission, credential,
release authority, or CI change. RFC-0117 records the full boundary.

## M135 explicit post-realization cache population boundary

`populate_asset_build_cache()` composes the unchanged M134 realizer and M132
publisher without weakening either contract. It accepts an exact plan,
detached inputs, one explicit cache path, optional project root, and the
existing tightening-only execution limits. It owns no descriptor, worker,
thread, process, clock, random source, or background lifecycle.

The operation first constructs `AssetCacheStore` with `writable=False` and
completes all realization phases. Only after every exact source, cache action,
decoder, and active limit succeeds does it construct a separate writable store
for the same resolved root and publish the complete materialization. A missing
cache is therefore not created on any pre-publication failure. CLI composition
also completes current lock/plan verification and project-confined source
acquisition before entering this boundary.

Frozen `ludoweave.asset-cache-population/1` evidence pairs each M134
realization entry with its M132 publication entry and requires exact URI,
cache-key, artifact-hash, byte-count, plan-hash, and order agreement. Reports
contain no payload or path. Cache state can change the status fields while the
artifact identity remains deterministic for the exact plan and sources.

Publication retains M132's atomic per-entry visibility. It is not an all-plan
transaction: a later filesystem failure may leave an earlier valid action or
valid unreferenced CAS blob and returns no M135 success report. The read/write
transition does not pin a directory descriptor or create a filesystem snapshot;
hostile concurrent replacement and shared writers remain unsupported. M135
adds no implicit publication to M134, rollback, repair, deletion, eviction,
remote cache, network, plugin, scheduler, renderer upload, world mutation,
dependency, version, workflow, permission, release authority, or CI change.
RFC-0118 records the full boundary.

## M136 saved asset-cache population verification boundary

`AssetCachePopulationRecord.from_json()` reconstructs the path-free M135
document without reconstructing or retaining payloads. An exact tightening-
only envelope caps UTF-8 input at 8 MiB and entries at 4,096. Decoding rejects
duplicate JSON names, non-finite constants, field-set or exact-type drift,
unsupported protocols/statuses, invalid logical/output identities, duplicate
URIs, aggregate byte mismatches, and status-count mismatches. Canonical output
uses the unchanged `ludoweave.asset-cache-population/1` shape.

`verify_asset_cache_population()` first compares the complete record with the
exact current plan hash and plan-ordered URI, kind, cache-key, and source-byte
identity. Failure occurs before cache construction or action reads. Only after
preflight does it create `AssetCacheStore(..., writable=False)` and require
every action to exist, pass M133 metadata/CAS checks, and equal the saved full
result identity. Payloads are observed one at a time and discarded. Frozen
`ludoweave.asset-cache-population-verification/1` success retains only status,
protocol, plan hash, and entry count.

CLI composition recomputes and verifies current sources, lock, manifest, and
plan before reading the project-confined saved report and invoking read-only
cache verification. It neither reacquires sources for decoding nor invokes a
decoder. Missing/corrupt/mismatched actions have no fallback, repair, or write;
an absent cache remains absent.

The report has no signature, authenticated builder, root of trust, trusted
timestamp, or attestation envelope. Agreement with a locally observed cache is
not provenance or authenticity and cannot prove historical status events. M136
adds no cache mutation, remote transport, discovery, worker, plugin, renderer
upload, world mutation, dependency, version, workflow, permission, release
authority, or CI change. RFC-0119 records the full boundary.

## M137 bounded asset-cache inventory boundary

`inspect_asset_cache_inventory()` opens one explicit `AssetCacheStore` with
`writable=False`, then admits only ordinary non-reparse objects under the exact
engine-owned `actions/` and `cas/` namespaces. Incremental `os.scandir()` loops
enforce hard counts before retaining another action/blob. Aggregate metadata
and CAS-byte budgets are checked from no-follow metadata before file open and
again while reading.

Every action directory has one strict duplicate-free canonical `entry.json`.
Its decoded result cache key must match its sharded location. Every CAS filename
must match the SHA-256 streamed from its bytes, and every action artifact
reference must resolve to a same-sized blob. The exact current plan then
classifies matching current actions and their unique blobs; URI, kind, and
source byte count must agree.

Frozen path-free `ludoweave.asset-cache-inventory/1` evidence contains only the
plan hash plus current/missing/other action and metadata-byte totals, total/
current/other CAS counts and bytes, and no-observed-action-reference blob counts
and bytes. Stable bytes produce the same report independent of enumeration
order.

The operation is sequential, not an atomic filesystem snapshot. Detected size
drift fails, but hostile replacement remains outside the supported local
single-caller model. A blob with no action reference observed by the scan is
not deletion eligibility. M137 has no write, repair, deletion, eviction,
garbage collection, age/access-time policy, lease, generation, remote cache,
network, dependency, version, workflow, permission, release authority, or CI
change. RFC-0120 records the full boundary.

## M138 deterministic cache-observation fingerprint boundary

`fingerprint_asset_cache_observation()` performs the same exact plan preflight
and one `_observe_storage()` call as M137. That single bounded pass retains
M137's no-follow layout admission, canonical action reconstruction, streamed
CAS digest verification, action/blob closure, active limits, and read-only
authority. The aggregate inventory and fingerprint are derived from the same
verified in-memory identities; storage is not enumerated twice.

The SHA-256 stream begins with the ASCII
`ludoweave.asset-cache-fingerprint/1` domain and NUL separator. Actions follow
in cache-key order as tag `A`, unsigned eight-byte big-endian payload length,
and exact canonical action metadata. CAS records follow in artifact-digest
order as tag `C`, the same length framing, 32 raw digest bytes, and unsigned
eight-byte content length.

Frozen path-free `ludoweave.asset-cache-fingerprint/1` evidence nests the M137
inventory and adds only `observation_sha256`. The digest is independent of the
current plan; the nested inventory remains plan-relative. The public report
contains no URI, cache key, artifact digest, filename, path, payload, timestamp,
age, or environment value.

This is exact identity for one sequential observation, not an atomic snapshot,
diff, lease, last-use fact, retention root, provenance statement, or deletion
eligibility. M138 adds no write, cleanup, repair, eviction, garbage collection,
network, remote cache, dependency, version, workflow, permission, release
authority, or CI change. RFC-0121 records the full boundary.

## M139 saved cache-fingerprint verification boundary

`decode_asset_cache_fingerprint()` admits one exact canonical saved M138 record
under a tightening-only 65,536-byte limit. JSON decoding rejects duplicate
names and non-finite constants; reconstruction requires exact top-level and
nested fields, exact primitive types, supported protocol identifiers, valid
SHA-256 text, and internally consistent bounded inventory aggregates. The
admitted bytes must equal the reconstructed fingerprint's canonical bytes.

`verify_asset_cache_fingerprint()` requires exact plan and fingerprint values,
then hashes the current plan's canonical bytes and compares that identity with
the saved nested inventory before cache construction. Only after preflight does
it call the unchanged M138 fingerprint operation exactly once. The fresh
inventory and observation digest must both equal the saved values.

Frozen path-free `ludoweave.asset-cache-fingerprint-verification/1` success
contains valid status, fingerprint protocol, plan digest, and observation
digest. Failure context names only the rejected field; it publishes no cache
key, URI, artifact digest, filename, path, payload, or differing digest.

Digest agreement is local integrity equality, not authenticity. There is no
signature, key identity, root of trust, authenticated builder/channel, trusted
timestamp, attestation, or provenance envelope. Verification supplies no
ownership, lease, retention root, last-use fact, deletion authority, or atomic
snapshot claim. M139 adds no mutation, cleanup, remote cache, dependency,
version, workflow, permission, release authority, or CI change. RFC-0122
records the full boundary.

## M140 path-free cache-fingerprint comparison boundary

`compare_asset_cache_fingerprint()` requires exact plan and saved-fingerprint
values and binds the nested saved plan digest before the external cache is
constructed. It then invokes the unchanged bounded M138 observation exactly
once and subtracts each saved M137 aggregate from its current counterpart.

Frozen `ludoweave.asset-cache-fingerprint-comparison/1` evidence has a fixed
shape: equal/different status, fingerprint protocol, plan digest, one
`observation_equal` boolean, and signed integer deltas for exactly the twelve
existing inventory fields. Equality requires both the identity digest match and
all-zero deltas. Valid same-size object substitution therefore remains
detectable without publishing either observation digest.

The report is path-free and contains no cache key, URI, artifact digest, action
or blob identity, filename, path, payload, expected/current observation digest,
timestamp, or age. It is not a JSON Patch or extensible per-object diff.
Corruption and active-limit failure still fail closed rather than producing a
partial diagnostic.

The comparison remains one sequential read-only observation, not an atomic
snapshot. It is local change evidence, not authenticity or provenance, and
grants no ownership, retention, eviction, deletion, write, repair, or cleanup
authority. M140 adds no dependency, remote cache, backend/native surface,
version, workflow, permission, release authority, or CI change. RFC-0123
records the complete boundary.

## M141 offline cache-fingerprint comparison boundary

`compare_asset_cache_fingerprint_records()` accepts only one exact plan and two
exact admitted fingerprint values. Both nested plan digests preflight against
the supplied plan before a shared pure helper produces the unchanged M140
comparison value. Signed deltas remain `current - expected`; identity-only
change still produces `different` when all aggregate deltas are zero.

The pure operation has no cache-root parameter and performs no filesystem,
cache, source, environment, clock, or network access. It does not invoke M138's
observation function or M139's decoder. The CLI remains the composition root:
it verifies current inputs first, reads exactly two project-confined records
under the unchanged M139 bound, decodes both canonically, and passes the frozen
values to the pure comparison.

M141 reuses `ludoweave.asset-cache-fingerprint-comparison/1`; it adds no report
protocol. The output remains path-free and contains no cache key, URI,
action/blob/artifact identity, filename, record path, payload, or either
observation digest. Equal/different status does not infer chronology or trust.

Offline digest comparison is local integrity/change evidence, not authenticity
or provenance. It does not turn either original sequential observation into an
atomic snapshot and grants no ownership, retention, eviction, deletion, write,
repair, or cleanup authority. M141 adds no dependency, remote cache,
backend/native surface, version, workflow, permission, release authority, or CI
change. RFC-0124 records the complete boundary.

## M142 saved cache-fingerprint comparison verification boundary

`decode_asset_cache_fingerprint_comparison()` admits one exact canonical M140
report under a tightening-only 4,096-byte hard limit. JSON admission rejects
invalid UTF-8, duplicate names, non-finite values, overlong integer tokens,
missing/extra fields, wrong protocols or primitive types, inconsistent status,
and signed deltas outside the unchanged M137 aggregate bounds. Reconstructed
M140 canonical bytes must equal the supplied bytes.

`verify_asset_cache_fingerprint_comparison()` accepts only exact plan, two M138
fingerprint, and M140 comparison values. It invokes M141's pure comparison,
thereby binding both nested fingerprint plan digests, and requires every field
of the saved comparison to match the recomputed frozen value. The verifier has
no cache/filesystem/source/environment/clock/process/thread/network access and
does not mutate its inputs.

Frozen path-free
`ludoweave.asset-cache-fingerprint-comparison-verification/1` evidence contains
valid status, fingerprint and comparison protocols, plan digest, comparison
status, and SHA-256 of the exact canonical comparison report. A correctly
derived `different` comparison verifies successfully; verifier success is not
fingerprint equality.

The CLI verifies current inputs before two independently bounded fingerprint
reads and one independently bounded comparison read. It has no cache argument
or access. Neither success nor failure publishes a record filename, cache key,
URI, action/blob/artifact identity, payload, or saved observation digest.

Offline recomputation supplies local integrity evidence, not authenticity or
provenance. It adds no signature, key/root of trust, attestation, trusted
timestamp, atomic snapshot, record store/retention, cache mutation/cleanup,
remote cache, dependency, backend/native surface, version, workflow,
permission, release authority, or CI change. RFC-0125 records the complete
boundary.

## M143 path-free unreferenced-blob preview boundary

`preview_asset_cache_unreferenced_blobs()` accepts only exact plan and M138
fingerprint values. It recomputes the plan SHA-256, requires the fingerprint's
nested inventory to bind that plan, and copies the existing unreferenced-blob
count/bytes plus complete observation identity into one frozen value. The pure
function has no filesystem, cache, source, environment, clock, process, thread,
or network capability and mutates no input.

The CLI verifies current sources, lock, and exact regenerated plan before
resolving the cache. It invokes the unchanged M138 bounded read-only observation
exactly once. An absent cache remains absent. Output exposes no candidate
identity, cache/action key, URI, artifact/blob digest, filename, path, payload,
timestamp, age, or policy.

Frozen `ludoweave.asset-cache-unreferenced-preview/1` contains `observed`
status, M137/M138 protocols, plan and full-observation SHA-256 values, and the
two existing unreferenced aggregates. A nonzero count is neither a failure nor
deletion eligibility. A concurrently publishing writer could have created a
blob before its action reference; other projects or future plans may also need
it.

M143 therefore adds no retained roots, last-use tracking, grace/age or quota
policy, lease, pin, generation, lock, quiescence, atomic snapshot, candidate
list, cleanup, garbage collection, prune, repair, deletion, eviction,
compaction, rollback, remote cache, dependency, backend/native surface,
version, workflow, permission, release authority, or CI change. RFC-0126
records the complete boundary.

## M144 offline unreferenced-blob preview boundary

`source asset-cache-fingerprint-record-preview` is a composition root only. It
preflights current project sources, the saved source lock, and exact regenerated
asset-build plan before resolving one project-relative fingerprint record. The
read reuses M139's 65,536-byte hard limit, project-confinement/no-follow rules,
strict exact-schema decoder, aggregate bounds, and canonical-byte equality.

The command then calls the unchanged pure M143 function and emits the unchanged
`ludoweave.asset-cache-unreferenced-preview/1` bytes. There is no cache argument,
cache construction/access, or fresh observation; the originating cache may be
absent. No new runtime value, protocol, decoder, or engine-root API exists.

The saved fingerprint is unsigned local integrity evidence. Offline derivation
does not establish freshness, chronology, authenticity, provenance, writer
identity, or a trusted timestamp. Its fixed aggregate preview remains neither
a candidate list nor deletion eligibility.

M144 adds no path/payload/age disclosure, retention root, grace/quota policy,
lease, pin, generation, lock, quiescence, atomic snapshot, cleanup, garbage
collection, prune, repair, deletion, eviction, mutation, remote cache, network,
dependency, backend/native surface, version, workflow, permission, release
authority, or CI change. RFC-0127 records the complete boundary.

## M145 saved unreferenced-preview verification boundary

`source asset-cache-unreferenced-preview-verify` is a composition root only.
It preflights current project sources, the saved source lock, and the exact
regenerated asset-build plan before resolving either saved record. It reuses
M139's project-confined, no-follow, 65,536-byte fingerprint admission and adds
one tightening-only 2,048-byte strict decoder for the exact canonical M143
preview schema. Duplicate keys, non-finite numbers, non-UTF-8 input, extra or
missing fields, invalid protocols or aggregates, oversized input, and
noncanonical bytes fail closed.

The pure verifier accepts exact `AssetBuildPlan`, `AssetCacheFingerprint`, and
`AssetCacheUnreferencedPreview` values. It invokes unchanged M143 derivation
once and requires exact frozen-value equality. Success emits the fixed,
path-free
`ludoweave.asset-cache-unreferenced-preview-verification/1` record with plan,
observation, fingerprint-protocol, preview-protocol, and exact canonical-preview
SHA-256 bindings. It has no filesystem, cache, clock, thread, process, network,
or mutation capability.

This is integrity evidence over supplied bytes, not authenticity, provenance,
writer identity, chronology, freshness, a trusted timestamp, an atomic current
cache snapshot, or deletion eligibility. M145 adds no cache argument or access,
candidate identity, path/payload/age disclosure, retention policy, cleanup,
mutation, remote cache, dependency, backend/native surface, version, workflow,
permission, release authority, or CI change. RFC-0128 records the complete
boundary.

## M146 cache-cleanup readiness boundary

M137-M145 establish verified cache structure, complete sequential aggregate
observations, path-free fingerprints/previews, and strict offline evidence
admission. Those records intentionally omit blob identities. Equal aggregate
counts and bytes across observations therefore cannot establish that the same
objects persisted, and an offline record cannot establish current reachability
at mutation time.

Cache cleanup remains deferred. Reconsideration requires one coherent design
covering identity-bearing candidates, all retained roots and leases/pins,
atomic or generation-bound quiescence, explicit grace/quota policy and trusted
time, bounded dry-run plus mutation receipts, concurrent-writer exclusion,
crash recovery, no-follow/reparse safety, and restore/rollback behavior. The
design must preserve project/cache separation and fail closed before deletion.

M146 adds no runtime value, protocol, decoder, CLI composition, cache access,
candidate disclosure, cleanup authority, mutation, dependency, backend/native
surface, version, workflow, permission, release authority, or CI change.
RFC-0129 records the complete decision.

## M147 asset-cache cleanup threat boundary

M147 formalizes the security boundary that any later cache mutation must
satisfy. The [asset-cache cleanup threat
model](security/cache-cleanup-threat-model.md) treats the exact cache root,
content-addressed blobs, action metadata, retained roots, future candidates,
quarantine, receipts, and path privacy as protected assets. It treats existing
cache files and saved evidence as inputs rather than authority, and it includes
same-user concurrent processes and mutable filesystem namespaces in the trust
boundary.

The blocking design invariants require separate dry-run and mutation types,
identity-bearing candidates bound to an exact root/generation/policy, complete
retained roots, cross-process quiescence held through use, handle-relative
no-follow revalidation, bounded work, same-filesystem quarantine, durable typed
receipts, idempotent recovery, deterministic ordering, and safe refusal on an
unsupported platform. Adversarial Windows, macOS, and Linux evidence is
required for TOCTOU, symlink/junction/reparse and hard-link substitution,
concurrent readers/writers, stale records, trusted-time rollback, crash,
disk-full, replay, restore, and finalize phases.

M147 adds no runtime API, value, protocol, decoder, CLI composition, cache
access, candidate disclosure, cleanup authority, retention implementation,
locking, trusted time, quarantine, repair, mutation, remote cache, dependency,
backend/native surface, version, workflow, permission, release authority, or
CI change. RFC-0130 records the accepted threat model.

There is no candidate disclosure, no cleanup authority, no remote cache, no
dependency, no workflow, and no CI change.

## M148 cache-cleanup platform-capability boundary

M148 evaluates the platform primitive needed by M147 without implementing it.
The [platform-capability
decision](security/cache-cleanup-platform-capability-decision.md) requires one
engine-owned adapter lifecycle covering root acquisition, all-component
no-follow resolution, identity-at-use inspection, same-filesystem quarantine,
relative unlink/removal, deterministic close, backend-neutral outcomes, and
safe refusal. Native descriptors and handles remain private.

Current portable CPython does not satisfy that chain across supported
platforms. Exact Windows 3.12-3.14 evidence lacks directory-descriptor mutation
and symlink-attack-resistant `rmtree`. POSIX directory-relative APIs, Linux
`openat2`, macOS `O_NOFOLLOW_ANY`, and Win32 handle operations are promising
platform-specific primitives, not an admitted engine capability. Flags or
documentation alone cannot substitute for real-host adversarial proof.

M148 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, cache access, candidate disclosure, cleanup authority, platform adapter,
native code, `ctypes`, mutation, remote cache, dependency, backend/native
surface, version, workflow, permission, release authority, or CI change.
RFC-0131 records the accepted decision. There is no public probe, no cleanup
authority, no native code, no dependency, no workflow, no remote cache, and no
CI change.

## M149 Windows cache-cleanup probe boundary

M149 adds a test-only [Windows capability
probe](security/cache-cleanup-windows-capability-probe.md) to reduce one part
of M148's platform uncertainty. The module lives under `tests/integration`, is
excluded from the wheel, imports no engine code, and owns every native handle
until reverse-order close.

The probe admits only single relative components and uses retained directory
handles for native opens and quarantine. It refuses reparse attributes, binds
open-object identity to volume serial plus 128-bit file ID, observes hard-link
count, never replaces an occupied quarantine name, proves identity after
rename/reopen, and marks only the quarantined handle for deletion. All mutation
is confined to pytest-owned temporary storage.

This is not an adapter layer and does not establish Windows support. The
current host cannot execute the symbolic-link case without additional
privilege, and the probe does not cover filesystem variation, namespace races,
cross-process exclusion, oplocks, crash recovery, retained roots, policy,
trusted time, durable receipts, or independent installed hosts.

M149 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production `ctypes`, platform adapter, cache access, candidate
disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow, permission, release authority, or CI change.
RFC-0132 records the accepted test-only boundary.

## M150 Windows directory-junction probe boundary

M150 adds one Windows-only, test-only [directory-junction refusal
probe](security/cache-cleanup-windows-junction-probe.md). A fixed `mklink /j`
invocation runs from the trusted pytest fixture directory with fixed literal
component arguments; no absolute fixture path or input from an engine API,
command, project file, or external caller enters command parsing.

The test binds its observation to the already-open root handle through
`GetVolumeInformationByHandleW`, requiring NTFS and reparse-point support. It
then reuses M149's retained-handle relative open and attribute classification.
The junction handle is rejected and closed before it can become a traversal
root. Explicit junction-entry removal is followed by target-marker proof.

This is current-host feasibility evidence, not a platform adapter or admission.
The fixture does not represent symbolic links, mounted folders, arbitrary
reparse tags, other filesystems, ancestor substitution, concurrent mutation,
cross-process exclusion, crash recovery, policy, trusted time, receipts, or
independent hosts.

M150 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production `ctypes` or shelling, adapter, cache access, candidate
disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow, permission, release authority, or CI change.
RFC-0133 records the accepted test-only boundary.

## M151 Windows retained-parent substitution boundary

M151 adds one Windows-only, test-only [retained-parent substitution
probe](security/cache-cleanup-windows-retained-parent-substitution-probe.md).
It retains an ordinary directory handle, renames that directory, and then uses
a fixed `mklink /j` invocation to bind the former name to a distinct target.
No engine input or absolute fixture path enters command parsing.

A fresh root-relative open of the rebound name observes and refuses the
junction. An open relative to the retained parent remains bound to the renamed
original directory. Volume/file identity proves that result equals a fresh
open through the `displaced` name and differs from the same-named target file.
All handles close before pytest removes the ordinary directories, and explicit
junction-entry removal preserves both file contents.

This is deterministic same-process current-host evidence, not concurrent race
or platform-admission evidence. It does not cover cross-process exclusion,
oplocks/share stress, pre-acquisition substitution, mounted folders, arbitrary
reparse tags, other filesystems, identity reuse, crash recovery, policy,
trusted time, receipts, or independent hosts.

M151 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production `ctypes` or shelling, adapter, cache access, candidate
disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow, permission, release authority, or CI change.
RFC-0134 records the accepted test-only boundary.

## M152 Windows cross-process substitution boundary

M152 adds one Windows-only, test-only [cross-process substitution
probe](security/cache-cleanup-windows-cross-process-substitution-probe.md).
The parent process retains an ordinary directory handle. One child `cmd.exe`
receives no native handle and executes the fixed relative command
`ren live displaced && mklink /j live target` from a trusted pytest root.

After successful child exit, a fresh root-relative open observes and refuses
the junction. The retained parent remains bound to the renamed original
directory. Volume/file identity proves its candidate equals a fresh open through
`displaced` and differs from the same-named target candidate. All handles close
before pytest removes ordinary directories, and explicit junction-entry removal
preserves both file contents.

This is deterministic current-host cross-process namespace-change evidence,
not a controlled concurrency or platform-admission result. It does not cover a
race at a selected native call, cross-process exclusion, oplocks/share stress,
quiescence, inherited or duplicated handles, pre-acquisition substitution,
other reparse tags/filesystems, identity reuse, crash recovery, policy, trusted
time, receipts, or independent hosts.

M152 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production `ctypes` or subprocess invocation, adapter, cache access,
candidate disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow, permission, release authority, or CI change.
RFC-0135 records the accepted test-only boundary.

## M153 Windows share-delete exclusion boundary

M153 adds one Windows-only, test-only [share-delete exclusion
probe](security/cache-cleanup-windows-share-delete-exclusion-probe.md). The
parent opens one ordinary NTFS directory with read and write sharing while
omitting delete sharing. A non-inheriting child `cmd.exe` executes only the
fixed relative command `ren live displaced` from the trusted pytest root.

While the blocking handle remains open, the child returns nonzero and both the
original name and candidate bytes remain unchanged. The parent explicitly
closes that handle, retains only the opened root, and runs the identical child
command. It then succeeds, the original name is absent, and the candidate is
unchanged under `displaced`. The root closes deterministically to zero owned
handles.

This is one current-host share-mode denial and release observation. It is not
general cross-process exclusion, quiescence, a controlled race, a selected
native-call interleaving, direct native-error evidence, an oplock protocol,
descendant-activity safety, or platform admission. Competing actors, duplicated
handles, other filesystems, recovery, policy, receipts, and independent hosts
remain outside the result.

M153 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production `ctypes` or subprocess invocation, adapter, cache access,
candidate disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow, permission, release authority, or CI change.
RFC-0136 records the accepted test-only boundary.

## M154 Windows native sharing-violation boundary

M154 adds one Windows-only, test-only [native sharing-violation
probe](security/cache-cleanup-windows-native-sharing-violation-probe.md). The
parent retains M153's ordinary NTFS directory handle without delete sharing.
It launches the exact current interpreter with `-I -B` and a fixed trusted test
helper; no `-c`, argument-selected component, stdin command, environment-
selected behavior, or inherited native handle enters the child.

The helper calls `MoveFileExW` with fixed relative names and captures
`GetLastError` immediately only after failure. Its only output is a bounded
exact-schema JSON success/code pair. While the blocker is open, the child
returns false/32 and namespace/content remain unchanged. After explicit close,
the identical child returns true/0 and the candidate is unchanged under the
renamed directory. The root then closes to zero owned handles.

This is one direct current-host native error observation. It is not a universal
Windows/filesystem/driver error contract, general cross-process exclusion,
quiescence, a controlled race, a selected interleaving, an oplock protocol, or
platform admission. Competing actors, duplicated handles, other native APIs,
other filesystems, recovery, policy, receipts, and independent hosts remain
outside the result.

M154 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production `ctypes` or subprocess invocation, adapter, cache access,
candidate disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow, permission, release authority, or CI change.
RFC-0137 records the accepted test-only boundary.

## M155 Windows child-owned share-delete handshake boundary

M155 adds one Windows-only, test-only [child-owned share-delete
handshake](security/cache-cleanup-windows-child-owned-share-delete-handshake.md).
A fixed isolated child opens only ordinary `live` with M153's exact directory
access mask and read/write sharing without delete sharing. Its native handle is
non-inheritable. It emits one bounded exact-schema `ready` document and waits
for one fixed release byte.

While that distinct process remains alive, the unchanged M154 native rename
child returns false/32 and namespace/content remain unchanged. The parent then
sends the fixed byte. The owner closes in `finally`, emits bounded `closed`, and
exits zero. Only after that acknowledgement does the identical native rename
child return true/0 and place the unchanged candidate under `displaced`.

This is one explicit current-host acquisition/close ordering across process
ownership. It is not a concurrent race, an interleaving inside a native call,
general exclusion, quiescence, an oplock protocol, duplicated-handle behavior,
or platform admission. A metadata-only prototype did not block the rename, so
the accepted fixture retains M153's exact nonzero desired-access mask.

M155 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production `ctypes` or subprocess invocation, adapter, cache access,
candidate disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow, permission, release authority, or CI change.
RFC-0138 records the accepted test-only boundary.

## M156 Windows abrupt blocker-owner termination boundary

M156 adds one Windows-only, test-only [abrupt blocker-owner termination
probe](security/cache-cleanup-windows-abrupt-blocker-termination-probe.md).
It reuses M155's fixed child-owned blocker and readiness boundary unchanged,
proves M154's false/error 32 denial while that owner remains alive, then sends
no release token. The parent forces termination and performs a bounded wait
before the identical rename returns true/code zero with content preserved.

The process exit must be nonzero but is not promoted as a stable numeric
contract. No `closed` acknowledgement is accepted on the forced path. The
explicit process wait, rather than a sleep or retry loop, is the only ordering
boundary between termination and the post-termination rename.

This is one current-host ownership-termination observation, not crash or
restart recovery, a close-failure protocol, concurrent mutation safety,
general exclusion, duplicated-handle or oplock behavior, or Windows admission.
M156 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, helper, dependency, workflow, permission, release authority, or CI
change. RFC-0139 records the accepted test-only boundary.

## M157 Windows blocker control-pipe EOF boundary

M157 adds one Windows-only, test-only [blocker control-pipe EOF
probe](security/cache-cleanup-windows-control-pipe-eof-probe.md). It reuses
M155's fixed child-owned blocker and M154's native rename unchanged. After
bounded readiness and false/error 32 denial, the parent writes no control byte
and closes only its `Popen.stdin` writer.

The helper's existing invalid-control path closes the native handle in
`finally`, emits no `closed` acknowledgement, and returns fixture-specific exit
4. A bounded process wait, rather than a sleep or retry loop, is the only
ordering boundary before the identical rename returns true/code zero with
content preserved.

This is one current-host EOF-triggered cleanup observation, not arbitrary pipe
failure, cancellation, native close failure, crash/restart recovery, concurrent
mutation safety, general exclusion, duplicated-handle or oplock behavior, or
Windows admission. M157 adds no runtime API, value, protocol, decoder, CLI
composition, public probe, helper, dependency, workflow, permission, release
authority, or CI change. RFC-0140 records the accepted test-only boundary.

## M158 Windows blocker invalid-control-token boundary

M158 adds one Windows-only, test-only [blocker invalid-control-token
probe](security/cache-cleanup-windows-invalid-control-token-probe.md). It
reuses M155's fixed child-owned blocker and M154's native rename unchanged.
After bounded readiness and false/error 32 denial, the parent writes exactly
one repository-fixed `?` byte, requires the buffered write to accept it,
flushes it, and closes its `Popen.stdin` writer.

The helper's existing invalid-control path closes the native handle in
`finally`, emits no `closed` acknowledgement, and returns fixture-specific exit
4. A bounded process wait, rather than a sleep or retry loop, is the only
ordering boundary before the identical rename returns true/code zero with
content preserved.

This is one current-host fixed invalid-token cleanup observation, not arbitrary
malformed input, partial or multiple writes, broken-pipe behavior,
cancellation, native close failure, crash/restart recovery, concurrent
mutation safety, general exclusion, duplicated-handle or oplock behavior, or
Windows admission. M158 adds no runtime API, value, protocol, decoder, CLI
composition, public probe, helper, dependency, workflow, permission, release
authority, or CI change. RFC-0141 records the accepted test-only boundary.

## M159 Windows blocker broken-control-pipe boundary

M159 adds one Windows-only, test-only [blocker broken-control-pipe
probe](security/cache-cleanup-windows-broken-control-pipe-probe.md). It reuses
M155's fixed child-owned blocker and M154's native rename unchanged. After
bounded readiness and false/error 32 denial, the parent kills and boundedly
reaps the blocker, then confirms output EOF.

One direct test-only `WriteFile` passes the existing release byte through the
parent stream's Windows handle. It reports false, exact `ERROR_NO_DATA` 232,
and zero written bytes. The parent writer then closes normally. A bounded
process wait and output EOF, rather than a sleep or retry loop, are the only
ordering boundaries before the identical rename returns true/code zero with
content preserved.

This is one current-host late-write observation, not Python exception-mapping
or universal Windows error behavior, arbitrary pipe failure, retry or recovery,
cancellation, native close failure, crash/restart recovery, concurrent
mutation safety, general exclusion, duplicated-handle or oplock behavior, or
Windows admission. M159 adds no runtime API, value, protocol, decoder, CLI
composition, public probe, helper, dependency, workflow, permission, release
authority, or CI change. RFC-0142 records the accepted test-only boundary.

## M160 Windows live-blocker wait-timeout boundary

M160 adds one Windows-only, test-only [live-blocker wait-timeout
probe](security/cache-cleanup-windows-live-wait-timeout-probe.md). It reuses
M155's fixed child-owned blocker, readiness, graceful release, and cleanup plus
M154's native rename unchanged. After bounded readiness and false/error 32
denial, the parent calls `Popen.wait(timeout=0.0)` exactly once.

The immediate wait raises `TimeoutExpired` with the fixed child arguments and
timeout value. The return code remains unset, the child remains alive, and the
identical rename still returns false/error 32 with namespace/content
unchanged. M155's existing release/acknowledgement path then returns exact
`closed` and child exit zero before one final identical rename returns
true/code zero with content preserved.

This is one current-host immediate-wait observation, not timeout recovery,
nonzero timeout behavior, readiness or close-timeout behavior, cancellation,
kill policy, native close failure, crash/restart recovery, concurrent mutation
safety, general exclusion, duplicated-handle or oplock behavior, or Windows
admission. M160 adds no runtime API, value, protocol, decoder, CLI composition,
public probe, helper, dependency, workflow, permission, release authority, or
CI change. RFC-0143 records the accepted test-only boundary.

## M161 Windows acknowledged-release timeout boundary

M161 adds one Windows-only, test-only [acknowledged-release timeout
probe](security/cache-cleanup-windows-acknowledged-release-timeout-probe.md).
Its fixed child retains M155's no-delete-share native behavior but defines a
new two-token protocol: `!` acknowledges release intent as exact
`release-held`, while a distinct `.` orders actual handle close.

After bounded `ready` and M154's false/error 32 denial, the parent sends and
flushes only release intent and requires bounded `release-held`. One
zero-duration process wait raises exact `TimeoutExpired`, leaves the child
live, and leaves the identical native rename false/error 32 with namespace and
content unchanged. Only the close byte may order native handle close, exact
`closed`, child exit zero, output EOF, and one final identical rename returning
true/code zero with content preserved.

This is one current-host acknowledged-intent observation, not an actual
graceful-close timeout contract, timeout recovery, nonzero timeout behavior,
cancellation, kill policy, native close failure, crash/restart recovery,
concurrent mutation safety, general exclusion, duplicated-handle or oplock
behavior, or Windows admission. M161 adds no runtime API, value, protocol,
decoder, CLI composition, public probe, production dependency, workflow,
permission, release authority, or CI change. RFC-0144 records the accepted
test-only boundary.

## M162 Windows duplicated-handle retention boundary

M162 adds one Windows-only, test-only [duplicated-handle retention
probe](security/cache-cleanup-windows-duplicated-handle-probe.md). Its fixed
child opens one no-delete-share directory handle and creates one
noninheritable same-process duplicate with the same access before exact
`ready`.

Fixed byte `1` closes the original handle exactly once and orders exact
`original-closed`. The child remains live and M154's identical native rename
remains false/error 32 with namespace and content unchanged because the
duplicate remains owned. Fixed byte `2` closes that duplicate exactly once and
orders exact `closed`, child exit zero, output EOF, and one final identical
rename returning true/code zero with content preserved.

This is one current-host same-process duplicate observation, not
inherited-handle behavior, cross-process duplication or transfer, general
handle-count verification, native close-failure behavior, oplock or lease
behavior, crash/restart recovery, concurrent mutation safety, general
exclusion, or Windows admission. M162 adds no runtime API, value, protocol,
decoder, CLI composition, public probe, production dependency, workflow,
permission, release authority, or CI change. RFC-0145 records the accepted
test-only boundary.

## M163 Windows inherited-handle retention boundary

M163 adds one Windows-only, test-only [inherited-handle retention
probe](security/cache-cleanup-windows-inherited-handle-probe.md). The parent
opens one no-delete-share directory handle and creates a fixed child with an
explicit `STARTUPINFO` handle list containing only that handle,
`close_fds=True`, fixed pipes, and isolated interpreter flags. The handle is
temporarily inheritable only around process creation and restored to
noninheritable in `finally` before readiness is consumed.

Exact `ready` orders the first false/error 32 rename result. Closing the
parent's handle exactly once leaves the identical second rename false/error 32
while the child remains live. Fixed byte `!` closes the inherited child handle
exactly once and orders exact `closed`, child exit zero, output EOF, and one
final identical rename returning true/code zero with content preserved.

This is one serial current-host explicit-handle-list observation, not a
concurrency-safe inheritance contract, broad inheritance behavior,
cross-process duplication or transfer, leak-freedom under concurrent launches,
native close-failure behavior, crash/restart recovery, concurrent mutation
safety, general exclusion, or Windows admission. M163 adds no runtime API,
value, protocol, decoder, CLI composition, public probe, production dependency,
workflow, permission, release authority, or CI change. RFC-0146 records the
accepted test-only boundary.

## M164 Windows inherited-handle launch-failure boundary

M164 adds one Windows-only, test-only [inherited-launch failure
probe](security/cache-cleanup-windows-inherited-launch-failure-probe.md). The
parent opens one no-delete-share directory handle, puts only that handle in a
`STARTUPINFO` explicit handle list, and temporarily marks it inheritable around
one fixed missing-executable `Popen` call with `close_fds=True`, `shell=False`,
explicit executable selection, and `DEVNULL` standard streams.

The real process-creation failure returns exact current-host
`FileNotFoundError`/`ENOENT`/Windows error 2 without a process owner. A
`finally` boundary restores noninheritability. Parent owned count remains one
and M154's identical native rename remains false/error 32 until the parent
closes its handle exactly once; only then does the identical second rename
return true/code zero with content preserved.

This is one serial current-host missing-executable rollback observation, not
restoration-failure injection, arbitrary process-creation failure coverage,
concurrent-launch leak-freedom, a concurrency-safe inheritance contract,
invalid-handle behavior, child-crash recovery, general exclusion, or Windows
admission. M164 adds no runtime API, value, protocol, decoder, CLI composition,
public probe, production dependency, workflow, permission, release authority,
or CI change. RFC-0147 records the accepted test-only boundary.

## M165 Windows inherited-handle restoration-failure boundary

M165 adds one Windows-only, test-only [inherited-handle restoration-failure
probe](security/cache-cleanup-windows-inherited-restore-failure-probe.md). It
uses M163's unchanged successful-child launch helper and injects one fixed
exception before the first native noninheritability restore for the exact
parent blocker handle.

The real fixed child is created with the one explicitly allowlisted handle.
M163's existing failure branch delegates to the unchanged close-and-reap
function before re-raising the identical injected exception. The test requires
no returned process, one terminal captured child, closed child pipe streams,
and the parent handle still inheritable. That last observation preserves the
distinction between process reclamation and parent-flag repair.

The caller uses the captured original setter in `finally` to restore the parent
handle to noninheritable. Parent owned count remains one and M154's unchanged
native rename remains false/error 32 until exact parent close, after which the
identical second rename returns true/code zero with content preserved.

This is one serial current-host injected restoration-failure ownership
observation, not a real native restoration failure, arbitrary failure coverage,
concurrent-launch leak-freedom, a concurrency-safe inheritance contract,
native-close behavior, recovery, general exclusion, or Windows admission. M165
adds no runtime API, value, protocol, decoder, CLI composition, public probe,
production dependency, workflow, permission, release authority, or CI change.
RFC-0148 records the accepted test-only boundary.

## M166 Windows concurrent broad-inheritance leak boundary

M166 adds one Windows-only, test-only [concurrent broad-inheritance leak
probe](security/cache-cleanup-windows-concurrent-inheritance-leak-probe.md).
It preserves M163's helper and fixture byte-for-byte while a module-local
subprocess proxy pauses the exact explicit-list `Popen` call after the parent
blocker becomes inheritable and before its intended child is created.

During that bounded event-controlled window, the caller uses the captured real
`Popen` class to start the same fixed child with `close_fds=False`, fixed
executable/path arguments, `shell=False`, trusted pytest cwd, and owned pipes.
After the broad child emits exact `ready`, the intended launch proceeds and
M163's unchanged `finally` restores parent noninheritability.

M154's unchanged native rename remains false/error 32 while the parent and
both children are live, after the parent closes, and after the intended child
acknowledges close and exits zero while the broad child remains live. Only the
broad child's acknowledged close and zero exit allow the identical fourth
rename to return true/code zero with content preserved. The third denial is
the distinguishing proof that the concurrently created broad child acquired
the temporarily inheritable blocker.

This is one controlled current-host hazard observation, not a concurrency-safe
inheritance contract, a general leak census, a runtime launch coordinator,
arbitrary process-creator or failure coverage, recovery, general exclusion, or
Windows admission. M166 adds no runtime API, value, protocol, decoder, CLI
composition, public probe, production dependency, workflow, permission,
release authority, or CI change. RFC-0149 records the accepted test-only
boundary.

## M167 Windows concurrent explicit-list isolation boundary

M167 adds one Windows-only, test-only [concurrent explicit-list isolation
probe](security/cache-cleanup-windows-concurrent-explicit-inheritance-probe.md).
It preserves M163's helper and fixture plus M166's complete boundary byte-for-
byte. Two worker threads each target a distinct no-delete-share handle and
pytest-owned root through M163's exact one-handle-list helper.

A module-local inheritability proxy requires both parent handles true before
either worker continues. A separate subprocess proxy validates each exact
list, `close_fds=True`, `shell=False`, corresponding trusted root, and owned
pipes, then delegates to the captured real `Popen`. Both real creations must
complete while both flags remain true. Both helpers then reach restoration
before either exact flag reset is released, after which both threads settle,
both flags are false, and both fixed children are ready/live.

M154's unchanged native rename remains false/error 32 for both roots before
and after both parent handles close. Parameterized A-to-B and B-to-A child
release orders require the released child's root to become renameable while
the other remains denied, then require the second root to succeed after its
child closes. This ordered result proves pairwise isolation for the controlled
overlap.

It is not a concurrency-safe process-creation contract, general leak-freedom,
coverage of every creator, handle, failure, cancellation, or reentrant
interleaving, a runtime coordinator, recovery, general exclusion, or Windows
admission. M167 adds no runtime API, value, protocol, decoder, CLI composition,
public probe, production dependency, workflow, permission, release authority,
or CI change. RFC-0150 records the accepted test-only boundary.

## M168 Windows concurrent explicit-list launch-failure boundary

M168 adds one Windows-only, test-only [concurrent explicit-list launch-failure
probe](security/cache-cleanup-windows-concurrent-explicit-launch-failure-probe.md).
It preserves M163's successful helper, M164's real missing-executable helper,
M167's complete boundary, and the fixed child fixture byte-for-byte.

Two threads assign success and failure roles to distinct handles and roots in
both orientations. Module-local proxies require both handles inheritable and
both launch boundaries ready before releasing the real `Popen` calls. The
successful process owner and exact `FileNotFoundError` are captured before
either wrapper returns. Both helpers then wait at restoration while both flags
remain true, after which both resets and threads settle.

Both roots return M154's false/error 32 result before parent close. After both
parents close, the failed-launch root returns true/code zero while the
successful root remains false/error 32 and its fixed child remains live. Only
the child's acknowledged close and zero exit permit the successful root's
true/code-zero rename. The mixed ownership result proves the successful child
did not acquire the failed launch's distinct blocker.

This is not a concurrency-safe process-creation contract, arbitrary launch-
failure, cancellation, restoration-failure, or reentrancy coverage, general
leak-freedom, a runtime coordinator, recovery, exclusion, or Windows
admission. M168 adds no runtime API, value, protocol, decoder, CLI composition,
public probe, production dependency, workflow, permission, release authority,
or CI change. RFC-0151 records the accepted test-only boundary.

## M169 Windows concurrent explicit-list restoration-failure boundary

M169 adds one Windows-only, test-only [concurrent explicit-list restoration-
failure probe](security/cache-cleanup-windows-concurrent-explicit-restore-failure-probe.md).
It preserves M163's successful helper, M165's failure type and boundary, M168's
complete boundary, and the fixed child fixture byte-for-byte.

Two threads assign survivor and injected-failure roles to distinct handles and
roots in both orientations. Module-local proxies require both handles
inheritable, release two real exact-list `Popen` calls, capture both returned
processes, and hold both outcomes and both restoration entries while both
flags remain true. One exact setter raises the injected M165 error while the
other performs its native reset.

M163 closes and reaps only the failed side's child before propagating the same
error. The survivor emits exact `ready` and remains live. After explicit repair
of the failed parent flag, both roots remain false/error 32 until both parents
close. The failed-restoration root then returns true/code zero while the
survivor root stays denied and its child remains live. Only the survivor's
acknowledged close and zero exit permit that root's true/code-zero rename. Both
payloads survive.

This is not a real native restoration failure, not a concurrency-safe process-
creation contract, arbitrary launch/restoration failure, cancellation, or
reentrancy coverage, general leak-freedom, a runtime coordinator, recovery,
exclusion, or Windows admission. M169 adds no runtime API, value, protocol,
decoder, CLI composition, public probe, production dependency, workflow,
permission, release authority, or CI change. No hosted check is added.
RFC-0152 records the accepted test-only boundary.

## M170 Windows concurrent explicit-list abrupt-termination boundary

M170 adds one Windows-only, test-only [concurrent explicit-list abrupt-
termination probe](security/cache-cleanup-windows-concurrent-explicit-abrupt-termination-probe.md).
It preserves M156's forced-termination boundary, M163's helper and fixture,
M167's pairwise isolation boundary, and M169's complete boundary byte-for-byte.

Two threads start real fixed children with distinct handles and roots. Module-
local proxies require both handles inheritable, capture both processes, and
hold both restoration entries while both flags remain true. Both exact native
resets complete, both children emit `ready`, and both parent handles close.
Both roots remain false/error 32.

The assigned abrupt child receives `kill()` and a bounded wait. Its nonzero
status, EOF after the consumed `ready` document, and empty stderr prove no
graceful `closed` phase. Only that root then returns true/code zero while the
survivor remains live and its root remains denied. The survivor's existing
acknowledged close and zero exit then permit its root's true/code-zero rename.
Both payloads survive.

This is not crash recovery, cancellation semantics, arbitrary termination-
timing or native-close-failure coverage, a concurrency-safe process-creation
contract, general leak-freedom, a runtime coordinator, recovery, exclusion, or
Windows admission. M170 adds no runtime API, value, protocol, decoder, CLI
composition, public probe, production dependency, workflow, permission,
release authority, or CI change. No hosted check is added. RFC-0153 records the
accepted test-only boundary.

## M171 Windows exclusive-root acquisition boundary

M171 adds one Windows-only, test-only [exclusive-root acquisition
probe](security/cache-cleanup-windows-exclusive-root-acquisition-probe.md).
It preserves M149's capability chain, M153's share-delete boundary, M155's
fixed child/handshake, and M170's complete boundary byte-for-byte.

The private parent opens an ordinary NTFS directory with list/read-attribute/
synchronize access, sharing mode zero, backup semantics, open-reparse-point
behavior, and null security attributes. It rejects reparse identity, owns the
handle, and proves it noninheritable. One fixed isolated child all-sharing open
returns exact false/error 32 while that owner remains live and exact true/error
zero after deterministic close.

For the reverse direction, M155's unchanged child emits exact `ready` while it
owns `live`. The parent zero-sharing acquisition returns the existing native
error with exact code 32, adopts no handle, leaves the child live, and preserves
content. After exact `closed` and zero exit, the same acquisition succeeds,
remains noninheritable, and closes once.

This is not a complete quiescence protocol, lock API, general exclusion,
attribute-only/open-mode coverage, oplock or lease contract, recovery, or
Windows admission. M171 adds no runtime API, value, protocol, decoder, CLI
composition, public probe, production dependency, workflow, permission,
release authority, or CI change. No hosted check is added. RFC-0154 records the
accepted test-only boundary.

## M172 Windows descendant non-exclusion boundary

M172 adds one Windows-only, test-only [descendant non-exclusion
probe](security/cache-cleanup-windows-descendant-non-exclusion-probe.md). It
preserves M149's capability chain, M155's bounded handshake, and M171's
complete boundary byte-for-byte.

One fixed isolated child opens only `live/candidate.bin` for generic read with
read/write/delete sharing and null security attributes. The handle is
noninheritable. Exact bounded `ready` and `closed` documents frame one fixed
release byte, deterministic native close, and zero exit.

The current NTFS host permits that child and M171's zero-sharing `live`
directory owner to coexist in both acquisition orders. The late child becomes
ready without releasing the earlier directory owner; the earlier child remains
live while the directory owner is acquired. Either owner closes independently,
and content remains exact.

Share-mode exclusion is therefore object-specific in this observation, not a
recursive subtree lock. A future quiescence boundary must bind every relevant
participant or generation and revalidate complete retained roots through use;
M171's primitive alone cannot become cleanup authority.

M172 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production dependency, adapter, workflow, permission, release authority,
or CI change. Writes, deletes, mappings, descendants, multiple participants,
oplocks, leases, recovery, policy, receipts, Windows admission, and independent-
host proof remain open. No hosted check is added. RFC-0155 records the accepted
test-only boundary.

## M173 Windows cooperative-lock boundary

M173 adds one Windows-only, test-only [cooperative-lock
probe](security/cache-cleanup-windows-cooperative-lock-probe.md). It preserves
M172, runtime, examples, scripts, dependencies, and workflows byte-for-byte.

One fixed ordinary `live/coordination.lock` and byte range zero/length one act
as a cooperative participation object. Two isolated children open only that
file with generic read and all sharing, prove their handles noninheritable, and
hold overlapping shared fail-immediate `LockFileEx` locks. A private parent
uses the same access/share/range with the exclusive and fail-immediate flags.

The current NTFS host permits both shared owners concurrently. Parent-exclusive
acquisition fails with native error 33 while both are live and again after the
first closes; it succeeds only after the last exact child unlock/close. In the
reverse order, the exclusive owner makes a late shared child report error 33;
after exact release, a fresh shared child acquires and closes normally. All
bytes and ownership counts remain exact.

This is positive evidence for one cooperative same-object barrier, not general
filesystem exclusion or cleanup authority. An actor can ignore the
coordination object, and M173 does not bind its identity to a retained root or
generation. Complete participant admission, retained roots, mapped views,
substitution resistance, cancellation, abrupt-exit settlement, native failure,
filesystem variation, recovery, policy, receipts, Windows admission, and
independent-host proof remain open.

M173 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production dependency, adapter, workflow, permission, release authority,
or CI change. No hosted check is added. RFC-0156 records the accepted test-only
boundary.

## M174 Windows cooperative-lock substitution boundary

M174 adds one Windows-only, test-only [cooperative-lock substitution
probe](security/cache-cleanup-windows-cooperative-lock-substitution-probe.md).
It preserves M173, runtime, examples, scripts, dependencies, and workflows
byte-for-byte.

One unchanged M173 child holds a shared lock on
`live/coordination.lock`. A fixed isolated namespace child renames that object
to `live/coordination.displaced` and creates a new ordinary file with the exact
original bytes at the old pathname. Parent-held `FILE_ID_INFO` observations
prove the retained original and displaced handles share one identity while the
replacement has a different identity.

A second unchanged M173 child can hold a shared lock on the replacement while
the original child remains live. Each independently refuses exclusive
ownership of its own object. Closing the replacement child permits exclusive
ownership of the replacement while the original child still blocks the
displaced original; only closing the original permits exclusive ownership
there.

The result is negative capability evidence: path equality and content equality
do not bind participants to the same coordination generation. A future design
must bind a trusted root identity, coordination identity, and generation and
revalidate those relationships around namespace mutation. M174 does not define
that protocol or establish cleanup authority.

M174 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production dependency, adapter, workflow, permission, release authority,
or CI change. Windows remains unadmitted and no hosted check is added.
RFC-0157 records the accepted test-only boundary.

## M175 Windows live substitution-exclusion boundary

M175 adds one Windows-only, test-only [live substitution-exclusion
probe](security/cache-cleanup-windows-cooperative-lock-live-substitution-exclusion-probe.md).
It preserves M174, runtime, examples, scripts, dependencies, and workflows
byte-for-byte.

Two fixed isolated participants open `live/coordination.lock` for generic read
with read/write sharing but deliberately omit delete sharing. They retain
M173's shared fail-immediate lock over byte zero/length one. M174's unchanged
native substitution child returns sharing violation 32 while both participants
remain live and again after one closes. M173's unchanged exclusive range owner
returns lock violation 33 in both states.

After the final protected participant closes, exact exclusive acquire/release
succeeds. The unchanged substitution child then renames and replaces the file.
Retained `FILE_ID_INFO` evidence proves the displaced original keeps the old
identity and the replacement has another.

The result protects identity only across one continuous live-ownership
interval. It does not bind processes that start after a quiescent gap to the
same generation. Trusted placement, root/file identity, generation issuance,
participant admission, revalidation, recovery, policy, and receipts remain
unresolved.

M175 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production dependency, adapter, workflow, permission, release authority,
or CI change. Windows remains unadmitted and no hosted check is added.
RFC-0158 records the accepted test-only boundary.

## M176 Windows cooperative-lock abrupt-settlement boundary

M176 adds one Windows-only, test-only [cooperative-lock abrupt-settlement
probe](security/cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe.md).
It preserves M175, runtime, examples, scripts, dependencies, and workflows
byte-for-byte.

Two unchanged protected participants first refuse M174 pathname substitution
with error 32 and M173 exclusive range ownership with error 33. The first is
killed and waited for through Python's bounded Windows process path. Its
nonzero exit and stdout EOF after `ready` occur without a graceful `closed`
record. The survivor remains live and preserves both refusals.

After the survivor is killed and reaped identically, exact exclusive acquire/
release and M174 substitution succeed without polling. Retained `FILE_ID_INFO`
evidence proves the displaced original keeps the old identity and the
replacement differs. All bytes and owners settle.

The result is one current-host abrupt-settlement observation, not crash
recovery or a portable release deadline. The operating system may delay range-
lock release, and the zero-participant identity gap remains. Trusted placement,
identity/generation binding, complete admission, recovery, policy, and receipts
remain unresolved.

M176 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production dependency, adapter, workflow, permission, release authority,
or CI change. Windows remains unadmitted and no hosted check is added.
RFC-0159 records the accepted test-only boundary.

## M177 Windows protected guardian-handoff boundary

M177 adds one Windows-only, test-only [protected guardian-handoff
probe](security/cache-cleanup-windows-protected-guardian-handoff-probe.md). It
preserves M176, runtime, examples, scripts, dependencies, and workflows
byte-for-byte.

One private noninheritable guardian opens M173's coordination file for generic
read with read/write sharing while omitting delete sharing. With only the
guardian live, M174 substitution fails with error 32 while M173 exclusive
range acquire/release succeeds. The guardian therefore protects namespace
identity without owning the cooperative byte range.

M175's unchanged participant joins and closes while the guardian remains.
During the resulting participant-free interval, substitution still fails while
exclusive range ownership succeeds. A second unchanged participant joins the
same observed identity. Closing the guardian while that participant remains
live preserves substitution error 32 and exclusive-range error 33. Only the
participant's final close permits exact exclusive acquire/release and M174
substitution with the retained original and distinct replacement identities.

The result is one current-host continuous protection chain, not generation
authority, trusted-root placement, complete admission, startup/crash recovery,
or cleanup authority. Guardian failure, hostile prior handles, mapped views,
filesystem variation, durable generation issuance, revalidation, policy,
receipts, and independent hosts remain unresolved.

M177 adds no runtime API, value, protocol, decoder, CLI composition, public
probe, production dependency, adapter, workflow, permission, release authority,
or CI change. Windows remains unadmitted and no hosted check is added.
RFC-0160 records the accepted test-only boundary.

## Deferred architecture

Persistent commands/receipts, snapshots/hashes, replay/branches,
project-confined workflow CLI, the isolated M3 Null/wgpu 2D vertical slice, the
bounded M4 gameplay contracts, the local M5 typed agent/stdio MCP interface,
the M6 community-alpha distribution contract, the M7 native-code decision, and
the M8 gamepad contract/SDL3 deferral, the M9 Box2D deferral, the M10 owned
local semantic inspector, the M11 rich 2D authoring records, the M12 inert
plugin manifest contract, and the M13 offline rollback-readiness decision now
exist. M14 records the retained layered-2D boundary and defers constrained 3D
without changing the runtime package. M15 retains the headless inspector and
defers visual-editor implementation. M16 retains data-only plugins and defers
WASM runtimes, guest execution, WASI, and host calls. M17 adds one explicit
installed render-device baseline without admitting or discovering providers.
M18 adds one explicit installed agent-tool baseline without discovering a
transport or admitting an adapter. M19 adds one explicit installed WorldStore
baseline without discovering an implementation or adding a storage backend.
M20 retains experimental command/receipt stability after a bounded installed
readiness audit; it adds no reader, operation, format, or runtime export.
M21 then adds only that bounded reader and frozen single-version fixtures; it
does not change receipt/1, promote stability, or satisfy the cross-version gate.
M22 adds only the exact built-in operation/version argument policy and
same-version evidence; it does not add handlers or promote stability. M23 adds
only the exact receipt-v1 semantic-diff/diagnostic policy and same-version
evidence. M24 adds only offline cross-version admission readiness and retains
that gate as false. M25 adds only offline external-consumer-feedback admission
readiness and retains that gate as false. M26 adds only offline supported-
release-channel admission readiness and retains that gate as false. M27 adds
only offline external-contributor rehearsal admission readiness and retains
its empty-record result as false. M28 adds only offline external sample-game
adoption admission readiness and retains its zero count. M29 adds only offline
external contributor-retention admission readiness and retains its zero count.
M30 adds only offline installation-matrix admission readiness and retains its
zero-record result. M31 adds only offline issue-response and pull-request-review
latency admission readiness, retains its empty-manifest result, and defines no
SLA. M32 adds only offline CI replay-divergence-rate admission readiness,
retains its empty-manifest result, and exposes no measured rate. M33 adds only
offline benchmark-regression-rate admission readiness, retains its empty-
manifest result, and exposes no measured rate. M34 adds only offline agent-tool
recovery-rate admission readiness, retains its empty-manifest result, and
exposes no measured rate. M35 adds only offline third-party conformance-
adoption admission readiness, retains its reviewed zero result, and discovers
or executes no provider. M36 preserves those product boundaries and only
consolidates CI runner ownership without deleting any validation slice. None
supplies actual cross-
version history, external-consumer feedback, or a
supported release channel; no project-owned document or synthetic fixture is
treated as an independent human contribution.
M6
does not add a plugin loader or dynamic
data-selected code: adapter discovery remains explicit trusted composition.
Scene file loading, nested prefab composition/live updates, production audio,
rigid-body physics, network
transports, visual editor tooling, international text shaping, automatic
device recovery, and constrained/general 3D remain deferred to future
assigned, exercised slices. Native acceleration is
specifically deferred under RFC-0001's measurable revisit gate rather than
generally authorized by the recorded target misses.

## Python 3.15 prerelease boundary

M118 retains Python 3.15 outside the supported range. One exact Windows CPython
3.15.0b1 pure-wheel probe used an explicit metadata override and preserved only
serial headless behavior: version discovery, 120 virtual ticks and frames in
2,000,000,000 nanoseconds, orderly close, and `engine.wrong_thread`.
`doctor` correctly rejected the unsupported interpreter.

This is an unsupported prerelease compatibility observation, no support
promise. It changes no dependency direction, ownership rule, runtime branch,
public API, package metadata, workflow, allocation, provider boundary, or
release authority and is not a real public release observation. The supported
architecture baseline remains standard CPython 3.12-3.14.
