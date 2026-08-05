# ADR-0028: retain layered 2D and defer constrained 3D

- Status: Accepted
- Date: 2026-08-06

## Context

The post-alpha plan asks whether layered 2D should expand into constrained 3D.
It does not pre-authorize that expansion. LudoWeave's differentiated product
scope is deterministic, headless-first 2D and layered 2D that humans can play
and agents can operate through the same semantic world contracts.

The installed rendering surface remains intentionally two-dimensional:
`Camera2D` is orthographic, render capabilities expose only a 2D texture
limit, texture descriptors have width, height, array layers, and four color
formats, pipelines describe only a color target, and the built-in sprite
shader presents every vertex at a fixed clip-space depth. The command registry
has no perspective, mesh, model, or 3D operation.

WebGPU can represent 3D clip coordinates and optional depth/stencil state, and
wgpu-py mirrors that provider API. Those capabilities do not define
LudoWeave-owned camera, geometry, asset, material, authority, lifecycle, Null
backend, or agent semantics. Provider breadth is therefore not product
evidence. WebGPU is also a developing specification and wgpu-py documents its
API as subject to breaking changes.

## Decision

Retain the layered-2D scope and defer constrained 3D. M14 adds no runtime
module, public export, persistent format, dependency, or provider path.

`examples/constrained_3d_decision.py` inspects only the installed public render
contracts and built-in world-operation registry. It emits deterministic,
versioned `ludoweave.evaluation.constrained-3d/1` JSON. Source, isolated-wheel,
and release-bundle smoke require exact public exports/fields/operations,
positive orthographic camera and canonical layer/z ordering evidence, the
decision to remain deferred, and every admission gate to remain false. The
evidence includes no path, environment, host, provider, timing, or credential
field.

A future assigned proposal must supersede this ADR and satisfy every gate:

1. an accepted, playable product vertical slice whose value cannot be met by
   orthographic layered 2D;
2. engine-owned coordinate, transform, perspective-camera, projection, and
   precision conventions;
3. bounded mesh/index/vertex and asset contracts with validated limits and no
   provider-native object leakage;
4. explicit depth/stencil, ordering, culling, clipping, and 3D-texture
   semantics through provider-neutral descriptors;
5. bounded material and lighting semantics, with deliberate exclusions rather
   than an implicit general-purpose renderer;
6. canonical-versus-presentation classification plus versioned commands,
   receipts, queries, observations, and deterministic replay rules for every
   externally initiated 3D world mutation;
7. equivalent lifecycle, ownership, failure, and validation behavior through
   the headless Null backend before a GPU is required;
8. same-build Windows, macOS, and Linux conformance for both installed
   artifacts and the optional wgpu adapter; and
9. measured CPU, GPU, memory, asset-size, and startup budgets with a named
   maintenance owner and explicit recovery/close rules.

Perspective rendering, general mesh import, PBR, skeletal animation, terrain,
3D physics, scene graphs, picking, and editor tooling remain outside the
accepted scope.

## Consequences

- Layered depth sorting, parallax, array texture layers, and orthographic
  presentation remain 2D features and do not imply a 3D compatibility promise.
- Architecture tests allow only the standard library and engine-owned imports,
  with the exact existing wgpu/rendercanvas/GLFW adapter exception, and lock
  the exact current public render exports and descriptor boundary until an
  intentional decision changes them.
- The evidence is a scope decision, not a claim that WebGPU lacks 3D features
  or that constrained 3D can never be proposed.
- No benchmark is added because M14 introduces no runtime workload. A future
  admission proposal must supply its own measurable budgets.

## References

- [WebGPU specification](https://gpuweb.github.io/gpuweb/)
- [wgpu-py API reference](https://wgpu-py.readthedocs.io/en/stable/wgpu.html)
