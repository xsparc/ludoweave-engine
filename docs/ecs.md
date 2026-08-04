# ECS contracts

M1 begins the deterministic world core with generational entity identity, explicit component schemas, canonical world storage, storage-neutral queries, local deferred structural changes, typed resources, and deterministic serial schedule planning. System invocation remains the final M1 slice.

## Entity IDs

`EntityId` is an immutable, slotted pair of non-negative integers:

```python
from ludoweave.ecs import EntityId

entity_id = EntityId(index=0, generation=0)
assert entity_id.as_tuple() == (0, 0)
```

The pair is the canonical serialization-friendly form. A raw array index is not a public entity ID and allocator operations reject one with `InvalidEntityIdError`.

## Allocation and retirement

`EntityAllocator.create()` returns a live ID. `destroy()` retires that exact allocation generation and advances the slot generation before the slot can be reused. Freed slots are reused in deterministic last-in, first-out order.

Generations are unbounded Python integers. They do not wrap, so repeated reuse cannot make an earlier handle valid again. `is_alive()` provides a non-raising check for well-formed IDs; `validate()` and `destroy()` raise `StaleEntityError` when an ID is unknown, already retired, or carries the wrong generation.

The allocator is single-owner mutable simulation state. It is not thread-safe, does not use wall-clock time or randomness, and does not expose its internal arrays. A `World` owns its allocator; there is no global allocator or world singleton.

## Failure behavior

Entity failures extend the engine's structured `LudoWeaveError` hierarchy. They provide stable codes, phases, and immutable details through `as_dict()`. Expected failures do not silently allocate, destroy, or revive an entity.

## Component declarations

Components are slotted dataclasses with an explicit persistent UUID:

```python
from dataclasses import dataclass
from uuid import UUID

from ludoweave.ecs import DeterminismTier, component


@component(
    type_id=UUID("f385a8b1-eb56-4bc7-a505-802a7e36bd78"),
    version=1,
    authoritative=True,
    determinism=DeterminismTier.D2,
)
@dataclass(slots=True)
class Transform2D:
    x: float = 0.0
    y: float = 0.0
```

Decorator order matters: `@component` wraps an already-created slotted dataclass. It attaches an immutable `ComponentSchema` but does not register it globally or replace the Python class.

The UUID is persistent identity and must never be reused or changed for the same released component. `module.qualname` is a diagnostic alias and must also be unique within one registry. Schema versions are positive exact integers.

M1-02 accepts `bool`, `int`, finite `float`, `str`, and optional forms. Defaults must be matching literal scalar values. `default_factory`, `init=False`, dataclass inheritance, local classes, arbitrary objects/containers, and postponed string annotations are rejected until their canonical serialization behavior is defined.

Schema metadata declares:

- authoritative versus presentation-only state;
- canonical or excluded serialization;
- D0, D1, or D2 determinism tier;
- backend-neutral automatic, row, or column storage preference;
- immutable scalar inspection metadata on the component and its fields.

Authoritative components must use canonical serialization and tier D1 or D2.

## Explicit registries

`ComponentRegistry((Transform2D, ...))` validates the complete type set atomically and indexes schemas by UUID, qualified name, and Python class. Duplicates fail rather than overwrite. `schemas` is always sorted by UUID bytes, independent of caller order.

Registries are immutable and isolated. There is no process-global mutable component registry, no decorator-time registration, and no unregister or replacement operation in M1-02. Build a new registry to compose a different schema set.

## Migrations

A current version greater than one declares a complete ordered chain of adjacent `ComponentMigration` records. For version three, the chain is exactly `1→2`, then `2→3`. Gaps, duplicates, downgrades, skip edges, extra edges, and unordered declarations fail before a component class is created.

Migration callables are named module-level functions. They receive a read-only copy of scalar raw values and return a new mapping. `ComponentRegistry.migrate()` preflights the full path, executes it in ascending order, preserves caller input, validates final field names and values, and chains author-code exceptions into `ComponentMigrationError`.

The framework cannot prove that trusted migration code avoids time, randomness, I/O, or mutable globals. Such callables must be deterministic and side-effect free. Snapshot encoding and broader migration compatibility arrive in M2.

## Canonical world storage

`World` implements the storage-neutral `WorldStore` protocol using private pure-Python dense component rows and sparse entity-index locations:

```python
from ludoweave.ecs import ComponentRegistry, World

registry = ComponentRegistry((Transform2D,))
world = World(registry)
entity_id = world.spawn(Transform2D(x=1.0, y=2.0))

world.patch(entity_id, Transform2D, x=3.0)
assert world.get(entity_id, Transform2D) == Transform2D(x=3.0, y=2.0)
```

The world is the canonical owner of stored components. It validates and copies scalar fields when values enter or leave a public API. Mutating an original mutable component after `spawn()` or `add()`, or mutating a value returned by `get()`, `remove()`, or `components()`, cannot change world state. Whole-value `replace()` and partial `patch()` construct validated replacements instead of mutating stored objects in place. An empty patch is an error; a same-value patch is still an intentional write.

`add()` requires the component to be absent. `replace()`, `remove()`, `get()`, and `component_epoch()` require it to be present. All entity-scoped operations validate the full generational ID first. Duplicate, missing, stale, unknown-type, malformed-value, and failed-patch errors are structured, contain no dense offsets or component values, and leave the world unchanged.

The backend's dense order is not observable. `entities()` sorts by entity index and generation, and `components(Type)` sorts by entity ID. Registry component types are already UUID-sorted. These inspection methods are deterministic conformance surfaces, not the M1-04 query API and not a persistent snapshot format.

## Change epochs

`world.epoch` starts at zero and advances exactly once for every successful `spawn`, `destroy`, `add`, `remove`, `replace`, or `patch`. `world.structural_epoch` advances only when entity or component membership changes. Per-type structural epochs record the most recent membership change in that table, while `component_epoch()` records the add or last value write for a live row.

A multi-component spawn or destroy uses one shared world epoch. Moving the last dense row during swap removal preserves the moved component's change epoch. Failed operations advance nothing.

## Ownership, cloning, and threading

`clone()` makes independent in-memory state while preserving allocator generations and free-list order, component values, and epochs. The original and clone therefore choose the same next ID when given the same next spawn. This is not M2 snapshot serialization and makes no canonical-byte or hash promise.

World mutation is single-owner and not concurrently safe. Normal CPython remains the baseline, but the GIL is not an ownership mechanism. Callers must serialize lifecycle and world operations explicitly.

`ReferenceWorld` provides the same public storage behavior through a deliberately simple dictionary model. It independently implements allocation, values, epochs, patching, and cloning and is used as a property-test oracle. It is useful for conformance, not as an optimized gameplay backend.

## Queries

`World.query()` preserves the caller's component order and returns an immutable builder. Included types are conjunctive and `without()` excludes an entity when any named type is present:

```python
rows = world.query(Transform2D).stable().rows()
for entity_id, transform in rows:
    print(entity_id, transform)
```

Strict static row inference is precise for zero through four included component types. Larger runtime queries remain supported through a storage-neutral variadic `object` fallback; callers that need more precise annotations can split the query or narrow the returned values explicitly.

Zero included types are valid and produce entity-only rows. `stable()` orders rows by ascending generational `EntityId`; without it, iteration order is an implementation detail. Duplicate types, include/exclude overlap, unregistered types, and non-type values fail during builder construction.

`changed_since(epoch, *types)` matches when any watched included type changed strictly after the non-negative epoch. Omitting types watches all included types. A changed filter with no included type, a non-included watched type, or an epoch later than query activation is invalid.

Rows own detached copies. Mutating a read-only row is discarded. Controlled writeback declares mutable included types and uses a context manager:

```python
with world.query(Transform2D).writes(Transform2D).stable().rows() as rows:
    for _entity_id, transform in rows:
        transform.x += 1.0
```

Only mutable dataclass component types can be declared writable; `.writes()` rejects frozen component schemas at builder construction. The cursor validates every changed writable value in one row before storing any of that row. Changed values share one new epoch; an unchanged row advances nothing. Earlier rows remain committed if a later row fails. A context exception discards the current row and preserves earlier completed rows. Stored values are copied again, so retaining and mutating a row value after close cannot affect canonical state.

Writable cursors must use a context manager. Read-only cursors can nest, but any overlap involving a writable cursor fails. All direct world mutators, `clone()`, and `flush()` fail while a cursor is active; this ownership guard runs before those operations inspect their other arguments. Breaking early keeps that guard until `close()` or context exit; no finalizer is used as a correctness mechanism. Queries and worlds remain single-owner and are not concurrently safe.

## Local deferred structural commands

`world.commands()` creates a reusable local buffer bound to that exact world:

```python
commands = world.commands()
pending = commands.spawn(Transform2D(x=1.0, y=2.0))
commands.remove(pending, Transform2D)
result = world.flush(commands)
spawned_id = result.resolve(pending)
```

Spawn, destroy, add, and remove operations are invisible until `flush()`. Submitted components are validated and copied at enqueue time. A deferred entity token can target later operations only in the same buffer generation. Tokens from another buffer or world, forged tokens, and tokens invalidated by `clear()` are rejected.

A non-empty flush applies operations in enqueue order to private staged state. Complete success adopts the result, preserves the direct-operation epoch and allocator behavior, clears the buffer, and returns a `FlushResult`. Failure chains the original cause, reports the failing operation index and kind, retains the queue for identical retry or explicit clear, and leaves entity state, component state, epochs, and allocator order unchanged. Empty flushes are no-ops.

These buffers coordinate local structural mutation only. `FlushResult` is not a persistent command receipt, and neither buffers nor deferred tokens have a serialization, replay, authority, transaction, or stable cross-process identity contract. Those features remain M2 scope. Two independent worlds can produce equal `EntityId` values; M1 cannot infer that an ordinary ID came from a different world.

Chunk iteration, NumPy views, and storage-vector APIs are not part of M1-04; adding them later must preserve the same public ownership and conformance rules without exposing backend storage.

## Typed resources

`ResourceSpec[T]` is a stable named key for one exact value type. It carries deterministic eligibility and an explicit adapter that copies the value into and out of canonical storage. `ResourceRegistry` is immutable and name-sorted; it owns the exact key objects passed at composition time. Multiple names may use the same Python value type, but a reconstructed or foreign key is not interchangeable.

`ResourceStore` provides singleton `insert`, `require`, `replace`, and `remove` operations. Mutable adapters must return a distinct exact-type instance; immutable scalar identity is safe because no mutable alias can escape. Store cloning copies every present resource through its adapter. Copy and type failures are structured and chain application exceptions where available.

An adapter receives its input as read-only trusted application data. It must not mutate the input or nested state, perform I/O, consult time or randomness, retain aliases, or return a mutable alias. With a compliant adapter, a failed copy preserves the previous store state. Python cannot roll back arbitrary mutation performed by adapter code; a violating adapter invalidates the copy-ownership guarantee and must not be registered. Service objects that cannot satisfy this rule do not belong in deterministic resource storage.

Resources are world/application data, not service locators. Renderer, backend, network, filesystem, tool, and native objects do not belong in deterministic resource registries.

## Systems and schedule planning

The `@system` decorator attaches immutable metadata to a synchronous module-level Python function without registering or invoking it:

```python
from ludoweave.ecs import SystemContext, SystemPhase, system


@system(
    name="movement.integrate",
    phase=SystemPhase.SIMULATE,
    component_reads=(Velocity,),
    component_writes=(Transform2D,),
)
def integrate(context: SystemContext, delta: float) -> None:
    del context, delta
```

Declarations identify component and resource reads/writes, fixed phase, explicit same-phase `before` and `after` relationships, deterministic eligibility, and execution class. M1 accepts only ordinary Python systems and plans them serially. It does not infer concurrency from read/write metadata.

`Scheduler.build()` validates the complete set and returns an immutable plan without running a function. Deterministic-required plans reject ineligible systems, resources, and D0 components. Fixed phase order is `pre_simulate`, `simulate`, then `post_simulate`. Inside a phase, any relationship containing a writer must have an explicit direct or transitive precedence path; an ambiguous write conflict fails. Independent ready systems use lexical name ordering, so input registration order cannot influence the plan. Unknown, self, duplicate, and cross-phase dependencies fail, while cycles report a deterministic closed path with edge origins.

`SystemContext` is implemented by the M1-06 application runner as an invocation-scoped facade. Context queries default to stable order and validate include, exclude, changed, and explicit write access. Resource writes are staged per system and committed in a copied batch after successful return. Structural commands validate component writes and share one per-tick buffer across PRE/SIMULATE; it flushes before POST_SIMULATE, where further structural enqueue is rejected. Retained contexts and open writable cursors fail explicitly. The scheduler itself remains a planner and never invokes systems.
