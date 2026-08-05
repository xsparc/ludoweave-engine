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

## Dependency direction

The active packages follow these rules:

```text
composition roots  ludoweave.tools, examples
                          |
inspector parent   tools.inspector --stdio--> tools.mcp child

agent service      ludoweave.agent ----> world/runtime   ludoweave.world
                         |
                         +--------------> core contracts ludoweave.core

application        ludoweave.app ----> world/runtime   ludoweave.ecs
                         |                    |
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
- `ludoweave.world` may depend on core and public ECS contracts but not application, rendering, tools, or backend packages.
- `ludoweave.agent` may depend on core and world contracts but not application, rendering, tools, samples, or concrete backends.
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
installed render-device baseline without admitting or discovering providers. M6
does not add a plugin loader or dynamic
data-selected code: adapter discovery remains explicit trusted composition.
General scene importers, production audio, rigid-body physics, network
transports, visual editor tooling, international text shaping, automatic
device recovery, and constrained/general 3D remain deferred to future
assigned, exercised slices. Native acceleration is
specifically deferred under RFC-0001's measurable revisit gate rather than
generally authorized by the recorded target misses.
