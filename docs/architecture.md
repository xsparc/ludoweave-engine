# Architecture overview

## Product boundary

LudoWeave is designed around deterministic world operations. The ECS/world store is the only canonical runtime state as its M1 slices are introduced. Human tools, tests, CLI adapters, replay, and software-agent adapters must eventually submit the same versioned, validated world commands and receive receipts.

M0 established lifecycle, time, error, rendering, packaging, and dependency contracts. M1-01 adds generational entity identity, M1-02 adds immutable component schemas and registries, M1-03 adds canonical world storage plus an independent reference model, M1-04 adds storage-neutral queries and local deferred structural commands, and M1-05 adds typed resources plus conflict-aware serial schedule planning.

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
- `ludoweave.render.api` may depend on core errors but not application or tools.
- Concrete render backends may import the render API and core contracts.
- `ludoweave.app` composes core contracts, public ECS/runtime contracts, and the `RenderBackend` protocol, never a concrete backend. ECS never imports application implementations.
- `ludoweave.tools` and examples are composition roots and may select `NullRenderBackend`.
- The package root may re-export the deliberately small application API but never a concrete backend or third-party native object.
- wgpu, GLFW, NumPy storage objects, and future native extension objects are forbidden from public APIs.

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

Resource keys are explicit composition-owned identities; registries and stores are never global. Resource stores copy values through per-key adapters at every public boundary. Adapters are trusted read-only-input copy functions; objects that cannot be copied without mutation, I/O, external state, or retained aliases are excluded from deterministic storage. System declarations are immutable metadata on module-level synchronous functions. The scheduler validates registered component/resource access, deterministic eligibility (including rejection of D0 component access in deterministic-required plans), same-phase dependencies, and write conflicts, then produces an input-order-independent serial plan without invoking application code. Fixed phases resolve cross-phase conflicts; same-phase conflicts require an explicit direct or transitive path. Python concurrency and non-Python execution classes are rejected in M1.

`FixedStepApplication` is the single active mutation owner of its injected world and resources. Integer accumulator units preserve rational tick boundaries, catch-up backlog is retained, and immutable tick-indexed input is published as an explicit resource. Invocation-scoped query, resource, and command facades enforce declared access for normal system code. PRE/SIM commands share one buffer flushed before POST. Presentation occurs once per pump and cannot feed authoritative state. Tick failure is nontransactional until M2.

Entity slot reuse is deterministic for a given operation sequence, generation counters never wrap, and registry enumeration is UUID-sorted. Tick number and virtual time remain deterministic control values. Presentation frame counts, monotonic samples, diagnostics, logs, and platform metadata are not authoritative simulation state and must not become inputs to future state hashes.

Fixed deadlines are derived from the initial time and tick number rather than accumulated rounded deltas. This makes a virtual run repeatable and prevents rounding error from compounding.

## Backend isolation

`RenderBackend` is owned by the engine, while concrete implementations live behind it. The M0 `NullRenderBackend` validates descriptors and lifecycle ordering without graphics libraries. A future wgpu backend must implement the same engine-owned boundary; wgpu objects may not appear in application configuration, components, commands, snapshots, examples, or root exports.

## Deferred architecture

The following remain design constraints rather than implemented subsystems: persistent world commands and receipts, snapshots/replay files and rollback, platform device input, scenes, assets, audio, collision/physics, WebGPU, MCP, networking, editor tooling, and native acceleration. They will be added only with exercised milestone slices.
