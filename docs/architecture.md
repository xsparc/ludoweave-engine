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
General scene importers, production audio, rigid-body physics, network
transports, visual editor tooling, international text shaping, automatic
device recovery, and constrained/general 3D remain deferred to future
assigned, exercised slices. Native acceleration is
specifically deferred under RFC-0001's measurable revisit gate rather than
generally authorized by the recorded target misses.
