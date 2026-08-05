# Adapter and extension guide

LudoWeave supports explicit dependency injection plus M12 data-only plugin
manifests, not a plugin loader. Project data and manifests cannot name Python
modules or callables. There is no entry-point discovery, hot-loaded code,
sandbox, package resolver, or promise that a third-party adapter is safe merely
because its manifest and protocol checks pass. See the
[plugin compatibility guide](plugins.md) and RFC-0002.

## Choose the correct boundary

- Implement `RenderBackend` for the M0 lifecycle-only frame boundary.
- Implement `RenderDevice` for M3 resources, submissions, fences, capture, and
  optional provider-neutral surface events.
- Implement `AudioBackend` for clip/playback ownership; the alpha ships only the
  Null adapter.
- Implement `AgentCaptureProvider`, `AgentTelemetryProvider`, or
  `AgentTestProvider` only in a trusted application composition root.
- Use resource copy adapters and tick executors only for trusted deterministic
  application code under their stricter documented contracts.

Protocols and descriptors belong to engine packages. Concrete adapters depend
on them; engine contracts never import the adapter. Application/CLI/example
composition roots select implementations explicitly.

## Required adapter properties

1. Accept and return engine-owned descriptors, values, events, and handles.
2. Never expose wgpu, GLFW, NumPy storage, foreign pointers, or provider objects
   through an engine public API.
3. Validate lifecycle ordering and make `close()` explicit and idempotent.
4. Document ownership of every injected and returned resource, including close
   order and failure behavior.
5. Translate provider errors to structured engine failures without copying
   secrets, environment values, personal paths, or untrusted exception text.
6. Keep platform time, telemetry, capture pixels, and presentation state out of
   canonical authority and future state hashes.
7. Bound allocations/work driven by external descriptors and reject unsupported
   capability combinations before partial initialization.
8. Remain usable on normal GIL CPython; do not imply concurrent/free-threaded
   safety unless separately tested and documented.

The Null render/audio implementations are executable contract references. The
wgpu adapter demonstrates the permitted concrete-backend dependency exception
and provider-to-engine normalization.

## External physics admission

There is no supported physics-plugin protocol in the alpha. Do not implement a
provider by storing native bodies beside ECS entities and treating both as
authoritative. A future external solver must consume copied engine-owned values
at an explicit safe point, return copied observations or command proposals,
and reconcile complete failure without partially advancing the canonical
world. Native bodies, contacts, callbacks, allocators, pointers, and snapshots
must stay behind the adapter.

Physics is D0 unless an exact provider version passes cross-platform
snapshot/restore, replay, hash, contact-order, lifecycle, and worker-count
conformance. Same-binary repeated traces are only smoke evidence. Dependency
wheels/provenance, GIL and thread ownership, headless use, explicit idempotent
close, provider upgrades, and a named maintenance owner are separate admission
gates. The evaluated Box2D binding does not meet them; see
[ADR-0024](adr/0024-defer-box2d-v3-plugin-after-admission-review.md).

## Conformance checklist

An adapter contribution needs focused tests for:

- valid and invalid descriptors;
- initialize/use/close ordering and idempotent cleanup;
- initialization and mid-operation failure cleanup with exception chaining;
- stale/foreign handles and use after close;
- bounded capture/result shapes and provider-neutral types;
- the matching Null-versus-production semantic fixtures;
- missing optional dependencies with a typed diagnostic;
- installed-wheel behavior outside the source tree;
- every supported OS and CPython family in hosted CI.

Rendering providers additionally need clear, resource, capture, resize/minimize,
device-loss, batching, camera/layer, and deferred-destruction coverage. Exact
dependency upgrades follow the gates in the rendering guide and ADR-0015.

## Publishing and compatibility

Third-party adapters should be separately distributed packages that require a
bounded compatible LudoWeave version and document their own stability, licenses,
native requirements, and support matrix. Do not use the reserved `ludoweave`
top-level namespace without maintainer agreement.

They may publish a `ludoweave.plugin-manifest/1` document containing only inert
compatibility metadata. Applications must still select and import the package
explicitly. A positive report does not replace adapter conformance, trust,
ownership, provenance, or provider-admission review.

Adding another official renderer/platform/physics backend, introducing plugin
discovery/loading, or changing a security/compatibility boundary requires an RFC. A
small adapter should not become a route to networking, arbitrary evaluation,
global mutable registries, or duplicate world state. See the
[architecture overview](architecture.md), [API policy](api-status.md), and
[first-contribution guide](first-contribution.md).
