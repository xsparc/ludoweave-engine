# ADR-0013: Presentation extraction and render-resource ownership

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

M3 must render deterministic worlds without making GPU state canonical or
placing wgpu objects in components, commands, snapshots, or public APIs. Both
the validation and production backends need the same inputs. GPU work also
outlives Python submission calls, so deleting a Python handle cannot imply
immediate native destruction.

## Decision

Rendering uses frozen engine-owned descriptors, commands, capabilities,
captures, and scoped generational handles. `RenderDevice` is single-thread
owned and injected by a composition root. No global mutable device exists.

Simulation values cross into immutable `PresentationFrame` records. Previous
and current transforms may be interpolated there. Frames identify the latest
completed simulation tick but remain outside world resources, canonical JSON,
snapshots, receipts, replay, and hashes. Deterministic extraction groups by
texture and sorts instances by layer, z, and entity identity.

Handle retirement is immediate and generation-checked. The device records the
last referencing logical fence and defers physical destruction until that
fence completes. Explicit `destroy()` and idempotent `close()` own cleanup;
Python finalizers are not authoritative resource management.

Every draw command list names one explicit render target and carries a
backend-neutral camera matrix. Provider objects never cross this boundary.

## Consequences

- Null and wgpu devices consume equivalent immutable presentation commands.
- Presentation interpolation and GPU completion cannot alter authoritative
  state.
- Foreign, wrong-kind, retired, closed-device, and wrong-thread operations
  have stable typed failures.
- Asset hot reload can later swap handles at safe points without changing the
  public identity model.
- Application integration remains explicit; M3 does not create an ambient
  renderer or merge presentation data into `WorldSession`.

## Alternatives considered

Storing provider objects in components was rejected because it leaks unstable
APIs into authority state. Reference-count/finalizer cleanup was rejected
because GPU completion is asynchronous. Numeric global handles were rejected
because cross-device and reused-slot mistakes would be ambiguous. Rendering
directly from private ECS tables was rejected because it couples storage to a
backend and makes presentation ordering authoritative by accident.
