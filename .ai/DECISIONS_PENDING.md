# Decisions Pending

No architecture decision is currently blocked.

RFC-0001 resolves the M7 first-native-kernel question by deferring Rust/PyO3
until its quantified cross-platform, buffer/GIL, ownership, build, fallback,
fuzz, and maintenance-owner gate is satisfied.

ADR-0023 resolves the M8 SDL3 question by using the already-pinned GLFW gamepad
surface and deferring SDL3 until a stable Python binding, auditable offline
binary delivery, explicit lifecycle ownership, cross-platform conformance, and
maintenance owner are evidenced.

ADR-0024 resolves the M9 Box2D question by deferring the preview binding until
the complete CPython/OS wheel and provenance matrix, stable API, lifecycle and
stale-object soak, documented GIL/thread ownership, cross-platform
snapshot/replay classification, copied engine adapter conformance, and a named
maintenance owner are evidenced.

ADR-0025 resolves the M10 inspector boundary with one isolated, owned local
MCP child, detached semantic observations, explicit receipted writes, exact
hash continuity, and no arbitrary process, network, remote-attach, or editor
surface.

RFC-0002 resolves the M12 plugin boundary with canonical inert manifests,
explicit environment/policy/dependency checks, and no discovery, import,
execution, installation, or ambient global registry.

ADR-0027 resolves the M13 rollback/network-snapshot question by admitting only
a bounded offline correction-branch proof and deferring transport/live rollback
until canonical tick-input history, protocol/security, cross-platform network
simulation, resource budgets, lifecycle ownership, and maintenance gates are
complete.

ADR-0028 resolves the M14 constrained-3D question by retaining layered 2D and
deferring any 3D runtime until a bounded product slice, provider-neutral
spatial/render/asset contracts, canonical agent/replay semantics, equivalent
Null behavior, cross-platform installed conformance, measured resource
budgets, lifecycle ownership, and a named maintainer are evidenced together.

ADR-0029 resolves the M15 visual-editor question by retaining the finite
headless inspector and deferring GUI/editor implementation until public
compatibility, document/scene, selection/hierarchy, undo/conflict, property,
viewport, asset, recovery, accessibility/usability, cross-platform packaging,
resource-budget, and maintenance-owner gates are evidenced together.

Operational follow-ups outside repository implementation:

- Verify and reserve the `ludoweave` package name before the first publication.
