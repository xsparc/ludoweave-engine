# Architecture overview

## Product boundary

LudoWeave is designed around deterministic world operations. The ECS/world store is the only canonical runtime state as its M1 slices are introduced. Human tools, tests, CLI adapters, replay, and software-agent adapters must eventually submit the same versioned, validated world commands and receive receipts.

M0 established lifecycle, time, error, rendering, packaging, and dependency contracts. M1-01 adds generational entity identity, M1-02 adds immutable component schemas and registries, M1-03 adds canonical world storage plus an independent reference model, M1-04 adds storage-neutral queries and local deferred structural commands, and M1-05 adds typed resources plus conflict-aware serial schedule planning.

M2 introduces `ludoweave.world` as the simulation-protocol layer. It may
depend on core and public ECS contracts, while application and tools may depend
on it. Persistent command envelopes are explicitly distinct from M1 local ECS
command buffers; see [the command protocol](commands.md) and ADR-0008.

## Dependency direction

The active packages follow these rules:

```text
composition roots  ludoweave.tools, examples

application        ludoweave.app ----> world/runtime   ludoweave.ecs
                         |                    |
service contract   ludoweave.render.api      |
                         |                    |
core contracts     ludoweave.core <----------+

concrete adapter   ludoweave.render.backends.null
        -> implements ludoweave.render.api
```

- `ludoweave.core` imports only the Python standard library.
- `ludoweave.ecs` may depend on core errors but not application, rendering, tools, or concrete backends.
- `ludoweave.world` may depend on core and public ECS contracts but not application, rendering, tools, or backend packages.
- `ludoweave.render.api` may depend on core errors but not application or tools.
- Concrete render backends may import the render API and core contracts.
- `ludoweave.app` composes core contracts, public ECS/runtime contracts, and the `RenderBackend` protocol, never a concrete backend. ECS never imports application implementations.
- `ludoweave.tools` and examples are composition roots and may select `NullRenderBackend`.
- The package root may re-export the deliberately small application API but never a concrete backend or third-party native object.
- wgpu, GLFW, NumPy storage objects, and future native extension objects are forbidden from public APIs.

The M2 CLI keeps filesystem policy in `ludoweave.tools`. Its data-only
headless-project manifest cannot name Python modules or callables, and every
artifact path is resolved beneath the explicitly selected project root before
bounded I/O. World, snapshot, replay, ECS, and application packages remain
path- and transport-agnostic.

These rules are enforced by an AST-based test over the source tree. The test also analyzes a generated invalid fixture so a broken checker cannot silently pass.

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
runtime values from influencing M2 replay. Canonical per-tick input recording
and application-runtime composition remain M4 work. Snapshot load replaces
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

`RenderBackend` is owned by the engine, while concrete implementations live behind it. The M0 `NullRenderBackend` validates descriptors and lifecycle ordering without graphics libraries. A future wgpu backend must implement the same engine-owned boundary; wgpu objects may not appear in application configuration, components, commands, snapshots, examples, or root exports.

## Deferred architecture

Persistent command envelopes, canonical JSON, typed atomic application,
receipts/diffs, state hashes, canonical snapshots, verified replay, checkpoints,
immutable branch timelines, and project-confined workflow CLI adapters now
exist. Platform device input, scenes, assets, audio, collision/physics, WebGPU, MCP, networking,
editor tooling, and native acceleration remain deferred to their assigned
exercised slices.
