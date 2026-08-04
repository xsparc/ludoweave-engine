# Architecture overview

## Product boundary

LudoWeave is designed around deterministic world operations. The future ECS/world store will be the only canonical runtime state. Human tools, tests, CLI adapters, replay, and software-agent adapters must eventually submit the same versioned, validated world commands and receive receipts.

M0 does not implement that world. It establishes lifecycle, time, error, rendering, packaging, and dependency contracts that later milestones must preserve.

## Dependency direction

The active M0 packages follow these rules:

```text
composition roots  ludoweave.tools, examples
        |
application        ludoweave.app
        |
service contract   ludoweave.render.api
        |
core contracts     ludoweave.core

concrete adapter   ludoweave.render.backends.null
        -> implements ludoweave.render.api
```

- `ludoweave.core` imports only the Python standard library.
- `ludoweave.render.api` may depend on core errors but not application or tools.
- Concrete render backends may import the render API and core contracts.
- `ludoweave.app` depends on core contracts and the `RenderBackend` protocol, never a concrete backend.
- `ludoweave.tools` and examples are composition roots and may select `NullRenderBackend`.
- The package root may re-export the deliberately small application API but never a concrete backend or third-party native object.
- wgpu, GLFW, NumPy storage objects, and future native extension objects are forbidden from M0 public APIs.

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

M0 has no canonical gameplay state. Tick number and virtual time are deterministic control values used to validate the future loop contract. Presentation frame counts, monotonic samples, diagnostics, logs, and platform metadata are not authoritative simulation state and must not become inputs to future state hashes.

Fixed deadlines are derived from the initial time and tick number rather than accumulated rounded deltas. This makes a virtual run repeatable and prevents rounding error from compounding.

## Backend isolation

`RenderBackend` is owned by the engine, while concrete implementations live behind it. The M0 `NullRenderBackend` validates descriptors and lifecycle ordering without graphics libraries. A future wgpu backend must implement the same engine-owned boundary; wgpu objects may not appear in application configuration, components, commands, snapshots, examples, or root exports.

## Deferred architecture

The following remain design constraints rather than packages in M0: ECS storage, component schemas, scheduling, world commands and receipts, snapshots/replay, scenes, assets, input, audio, collision/physics, WebGPU, MCP, networking, editor tooling, and native acceleration. They will be added only with exercised milestone slices.
