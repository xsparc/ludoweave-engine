# Constrained 3D scope decision

M14 retains LudoWeave's layered-2D scope. It does not add a 3D camera, mesh,
material, light, depth buffer, 3D texture, asset importer, physics adapter, or
editor feature.

Run the dependency-free installed-surface evidence from a source checkout or
the version-matched sample bundle:

```console
python examples/constrained_3d_decision.py
```

The command accepts no options and prints one canonical-shape JSON document
with schema `ludoweave.evaluation.constrained-3d/1`. It records:

- the current render descriptor and capability field names;
- the exact public render exports, color texture formats, and export count;
- positive orthographic `Camera2D` fields/matrix behavior, canonical
  sprite `(layer, z, entity)` ordering, and the tile-layer field;
- the built-in versioned world-operation names;
- nine Boolean admission gates; and
- the explicit `retain-layered-2d` / `deferred` decision.

`layered_2d_confirmed` is true only when those positive installed contracts
match the accepted layered-2D boundary; all nine 3D admission gates remain
false. The output is deterministic for one installed version. It deliberately omits
paths, host and environment values, provider identity, timing, credentials,
and native objects. It is repository decision evidence, not a new public
Python API or persistent world format.

## Why provider capability is insufficient

WebGPU supports 3D coordinates and optional depth/stencil pipeline state. The
current LudoWeave contracts expose orthographic `Camera2D`, color-only pipeline
and texture formats, 2D texture limits, sprite/tile/debug extraction records,
and a fixed-depth sprite shader. The engine has no provider-neutral semantics
for perspective projection, mesh ownership, depth, materials, 3D assets, or
agent-visible 3D mutations.

Adding provider calls first would make the optional adapter define the public
engine and would leave Null/headless execution unable to validate the same
world. That would violate the dependency and headless contracts in ADR-0002.

## Revisit gate

A future proposal must provide a bounded product slice; engine-owned spatial,
camera, geometry, asset, depth, texture, material, and lighting contracts;
canonical/agent/replay semantics; headless Null conformance; installed
cross-platform wgpu evidence; explicit ownership and close behavior; measured
resource budgets; and a maintainer. Every gate must be satisfied together.

The authoritative rationale and full exclusions are in
[ADR-0028](adr/0028-retain-layered-2d-and-defer-constrained-3d.md).
