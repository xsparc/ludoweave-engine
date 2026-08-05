# Adapter and extension guide

LudoWeave community alpha supports explicit dependency injection, not a plugin
loader. Project data cannot name Python modules or callables. There is no entry
point discovery, hot-loaded code, sandbox, compatibility resolver, or promise
that a third-party adapter is safe merely because it satisfies a protocol.

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

Adding another official renderer/platform backend, introducing plugin
discovery, or changing a security/compatibility boundary requires an RFC. A
small adapter should not become a route to networking, arbitrary evaluation,
global mutable registries, or duplicate world state. See the
[architecture overview](architecture.md), [API policy](api-status.md), and
[first-contribution guide](first-contribution.md).
