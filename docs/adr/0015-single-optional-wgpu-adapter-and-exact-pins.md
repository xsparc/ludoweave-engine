# ADR-0015: Single optional wgpu adapter and exact dependency pins

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

M3 requires a production 2D renderer on Windows, macOS, and Linux while the
base engine must remain installable without a GPU, display, or native compiler.
wgpu-py and its native provider evolve quickly, and window/canvas integration
must not spread through the package.

## Decision

The only M3 production adapter is
`ludoweave.render.backends.wgpu.WgpuRenderDevice`, using wgpu-py through
rendercanvas with its GLFW window backend and explicit offscreen canvas. It is
available through the optional `graphics` extra with exact pins:

- `wgpu==0.32.0`
- `rendercanvas==2.7.2`
- `glfw==2.10.2`

Only that exact module may import wgpu, rendercanvas, or GLFW. It is not
re-exported by package or render roots. NumPy remains forbidden in engine
source; offscreen provider arrays are converted immediately to immutable RGBA
bytes. The adapter owns built-in WGSL, layouts, samplers, buffers, textures,
surfaces, and deferred cleanup behind engine records.

Dependency upgrades require cross-platform clear/sprite/capture/resize/loss
conformance, strict quality checks, example execution, capture review, and
before/after benchmark evidence.

## Consequences

- Base installs and headless CI have no graphics dependency or compiler
  requirement.
- Graphics installs use provider binary wheels and one deliberately narrow
  churn boundary.
- Missing adapters and provider failures become structured engine errors.
- M3 includes a private provider completion workaround for the pinned Windows
  queue-callback ABI issue; it must be re-evaluated on upgrade.
- Device recovery is not promised. Simulated and provider operation loss make
  the device unusable until the owner closes and replaces it.

## Alternatives considered

Making wgpu mandatory was rejected because headless is first-class. Adding
ModernGL as a fallback was rejected because two production backends multiply
conformance and maintenance. `rendercanvas.auto` was rejected because backend
selection would become ambient. Exposing native wgpu types was rejected due to
provider churn and architecture leakage.
