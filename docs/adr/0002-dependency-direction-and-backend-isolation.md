# ADR-0002: Dependency direction and backend isolation

- **Status:** Accepted
- **Date:** 2026-08-04

## Context

Rendering, platform, storage, and future native dependencies evolve at different rates. Letting concrete backend objects enter public APIs would couple canonical state and application code to those dependencies and make headless testing unreliable.

## Decision

Engine-owned contracts define subsystem boundaries. Core contracts do not import application, tools, or adapters. Application code accepts protocols through dependency injection. Concrete adapters may depend on the contracts they implement, but those contracts and the application do not import concrete adapters.

CLI modules and examples are composition roots: they may choose and construct a concrete backend, then inject it into the application. The package root may re-export the small application API but not concrete adapters.

Public APIs, descriptors, commands, receipts, snapshots, scenes, and canonical components may never contain wgpu, GLFW, NumPy storage, or future native extension objects. Automated source-import tests enforce the active dependency graph and banned dependency rules.

## Consequences

- The null renderer can validate application behavior without a GPU or window system.
- A future wgpu implementation can change behind the protocol without becoming canonical state.
- Composition roots intentionally know concrete adapters; this exception is narrow and documented.
- Some wiring is explicit rather than hidden behind global registries or mutable singletons.
