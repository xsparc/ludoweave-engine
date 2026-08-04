# ADR-0004: Canonical world storage, ownership, and epochs

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

The world store becomes canonical simulation state in M1-03. Mutable component aliases outside the world could bypass validation and change tracking. Dense row order changes during swap removal and therefore cannot be a stable public contract. A production storage algorithm also needs an independent behavioral oracle rather than tests that repeat its implementation details.

M2 will define persistent snapshots and hashes, and M1-04 will define query borrowing and deferred structural mutation. M1-03 must not pre-empt either contract.

## Decision

`WorldStore` is a storage-neutral protocol. `World` owns an `EntityAllocator` and one private pure-Python dense/sparse table for every type in an immutable `ComponentRegistry`. Sparse locations are keyed by entity index, while dense rows retain the full generational `EntityId`. Removal uses swap removal and repairs the moved row's sparse location. `StorageHint` remains advisory; all hints have identical behavior in this slice.

The world owns canonical component instances. Public insertion, replacement, retrieval, removal, enumeration, and cloning copy the schema's validated scalar fields. Mutating a submitted or returned mutable dataclass cannot change canonical state. Future systems that require controlled mutable access must add a private borrow/write-tracking design without weakening these safe public boundaries.

Public entity inspection is sorted by `(index, generation)`. Public component inspection is sorted by entity ID, and component types are enumerated by registry UUID. Dense offsets and row order are never public.

`epoch` begins at zero and advances once for every successful logical mutation. `structural_epoch` advances for entity or component membership changes. Each component table records its last membership-change epoch, and each live component row records its last add, replace, or patch epoch. A multi-component spawn or destroy advances the world once and assigns that shared epoch to every affected table or row. Relocating a row during swap removal does not change the moved component's epoch. Failures leave all state and epochs unchanged. Empty patches are rejected; accepted same-value replacements and patches count as writes.

`clone()` creates independent in-memory state, including allocator generations and free-list order, so both worlds make the same next allocation. It is not a snapshot, serialization, or hash contract.

`ReferenceWorld` is an intentionally simple dictionary model. It duplicates allocation, copying, patching, epoch, and cloning logic. It may share public entity values, schemas, the registry, and structured error types, but it does not import or use the production allocator, dense table, world, sparse locations, or production helpers.

## Consequences

- Canonical mutation cannot occur through ordinary Python aliases returned by public APIs.
- Storage layout may change without breaking the public world contract.
- Deterministic inspection and explicit epochs make model comparison and future query-cache invalidation possible.
- Field-by-field scalar copying costs more than borrowing; benchmark evidence and M1-04's controlled access rules will determine whether a separate internal fast path is justified.
- The reference model is deliberately redundant, increasing maintenance work while reducing the chance that production and oracle share the same storage defect.
- No persistent snapshot format, canonical byte encoding, world hash, query-order guarantee, or cross-thread mutation guarantee is created by this decision.
