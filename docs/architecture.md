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
                         |                    |
core contracts     ludoweave.core <----------+

concrete adapters  ludoweave.render.backends.null[_device]
                   ludoweave.render.backends.wgpu (optional exact module)

focused contracts  ludoweave.platform, assets, collision, audio

sample composition ludoweave.samples.clockwork_arena
                   ludoweave.samples.agent_world_builder
```

- `ludoweave.core` imports only the Python standard library.
- `ludoweave.ecs` may depend on core errors but not application, rendering, tools, or concrete backends.
- `ludoweave.world` may depend on core and public ECS contracts but not application, rendering, tools, or backend packages.
- `ludoweave.agent` may depend on core and world contracts but not application, rendering, tools, samples, or concrete backends.
- Render contracts, handles, extraction, and graphs may depend on core errors but not application, tools, world, ECS storage, or concrete backends.
- Platform, asset, collision, and audio contracts depend only on their own package and core errors. Render adapters may emit engine-owned platform events.
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

## Deferred architecture

Persistent commands/receipts, snapshots/hashes, replay/branches,
project-confined workflow CLI, the isolated M3 Null/wgpu 2D vertical slice, the
bounded M4 gameplay contracts, the local M5 typed agent/stdio MCP interface,
the M6 community-alpha distribution contract, the M7 native-code decision, and
the M8 gamepad contract/SDL3 deferral, the M9 Box2D deferral, and the M10 owned
local semantic inspector now exist. M6 does not add a plugin loader or dynamic
data-selected code: adapter discovery remains explicit trusted composition.
General scene importers, production audio, rigid-body physics, network
transports, visual editor tooling, rich text, automatic device recovery, and 3D
remain deferred to future assigned, exercised slices. Native acceleration is
specifically deferred under RFC-0001's measurable revisit gate rather than
generally authorized by the recorded target misses.
