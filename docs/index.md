# LudoWeave Engine

**Build worlds humans can play and agents can operate.**

LudoWeave is a community-alpha release candidate for deterministic, headless-first Python 2D and layered-2D worlds. M0 established the repository contract and lifecycle skeleton. M1 added the deterministic world/application core. M2 added typed persistent commands, atomic transactions and receipts, canonical authority snapshots and hashes, deterministic random streams, verified replay/checkpoints, immutable branches, and a data-only headless CLI workflow. M3 added isolated Null and wgpu 2D rendering. M4 added provider-neutral input, content-addressed assets, bounded collision/audio contracts, and Clockwork Arena. M5 added typed capability-gated agent control through Python, CLI, and local stdio MCP. M6 added deterministic release artifacts, explicit API status, contribution guides, and release provenance staging. M7-M10 recorded native/SDL3/Box2D deferrals and added a bounded semantic inspector. M11 adds headless rich 2D authoring records. M12 adds preview data-only plugin manifests and deterministic compatibility checks without a plugin loader. M13 evaluates offline correction branches, records the replay input-history gap, and defers network rollback. M14 retains layered 2D and defers constrained 3D after an installed-surface audit. M15 confirms the command/inspector foundation but defers a visual editor until the authoring and support contract is complete. M16 retains the inert plugin boundary and defers executable WASM mods behind a complete security gate. M17 adds an explicit installed render-device conformance profile without provider discovery or admission. This is not yet a complete game runtime; most APIs remain experimental and the M12 plugin surface is preview.

## Current capabilities

- Explicit engine initialization, fixed-tick run, shutdown, and close behavior.
- Monotonic real time and deterministic virtual time behind one protocol.
- A backend-neutral rendering boundary with a null validation backend.
- Structured errors, JSON diagnostics, and a headless example.
- Tested architecture rules and a pure-Python wheel.
- Deterministic generational entity allocation with checked stale-handle failures.
- Explicit immutable component schemas and forward migration paths without global registration.
- Canonical dense/sparse world storage checked against an independent dictionary model.
- Storage-neutral queries with stable-order, changed-epoch, and explicit writeback contracts.
- Atomic local command buffers whose deferred entity tokens are exact buffer identities.
- Copy-owned typed resource singletons and input-order-independent conflict-aware schedule planning.
- Exact fixed-step application pumping with immutable input and declaration-enforcing system contexts.
- Canonical versioned commands, atomic staged application, semantic diffs, and machine receipts.
- Complete snapshots and engine-owned deterministic named random streams.
- Self-contained verified replay/checkpoint files and immutable parent-referenced branches.
- Project-confined `apply`, `snapshot`, `replay`, and `diff` command workflows.
- Backend-neutral render resources, immutable extraction, explicit render graphs, and deferred generational-handle destruction.
- An optional wgpu/rendercanvas/GLFW adapter with instanced atlas sprites, tiles, orthographic cameras, debug fixtures, resize, and offscreen capture.
- Immutable platform events/action snapshots, validated `asset://` content, deterministic 2D collision, minimal Null audio, and an ECS-authoritative playable sample.
- A transport-independent agent service with 12 typed tools, default read-only capabilities, bounded/redacted data, serialized safe-point mutations, and canonical receipts.
- A local MCP `2025-11-25` stdio adapter and Agent World Builder acceptance loop with no network listener or arbitrary code execution.
- Exact-tick sprite animation, bitmap text layout, immutable tilemaps,
  fixed-point particles, and a Null-audio mix graph through existing render
  records.
- Canonical inert plugin manifests, deterministic environment/dependency
  compatibility reports, and an explicitly invoked local checker with no
  discovery or code execution.
- Deterministic constrained-3D decision evidence that leaves the public and
  provider-neutral runtime surfaces layered-2D-only.
- Deterministic visual-editor admission evidence that confirms the existing
  semantic foundation while leaving GUI/editor runtime surfaces absent.
- Deterministic WASM-mod security evidence that confirms the inert plugin
  boundary while leaving runtimes, guest execution, WASI, and host calls absent.
- Versioned, sanitized render-device conformance evidence over explicitly
  supplied trusted factories, with no adapter discovery or certification.
- A pure-wheel community-alpha candidate with a deterministic sample bundle, checksums, SPDX SBOM, notices, explicit stability metadata, and cross-platform release smoke.

Start with the [community-alpha user guide](user-guide.md), then read the [architecture overview](architecture.md), [runtime contract](runtime-contract.md), [entity identity contract](ecs.md), [headless command workflow](cli-workflows.md), [rendering contract](rendering.md), [render-device conformance guide](render-device-conformance.md), [rich 2D presentation guide](presentation.md), [plugin compatibility guide](plugins.md), [constrained 3D decision](constrained-3d-decision.md), [visual-editor admission decision](visual-editor-decision.md), [WASM-mod security decision](wasm-mod-security-decision.md), [gameplay guide](gameplay.md), [agent control interface](agent-control.md), [API status](api-status.md), and [accepted decisions](adr/index.md) before building on the experimental and preview APIs.

## Quick check

```console
uv sync --frozen --all-groups
uv run ludoweave doctor
uv run python examples/hello_headless.py --ticks 120
uv run python examples/clockwork_arena.py --ticks 600
uv run python examples/rich_2d_showcase.py --ticks 6
uv run python examples/constrained_3d_decision.py
uv run python examples/visual_editor_decision.py
uv run python examples/wasm_mod_security_decision.py
uv run python examples/render_device_conformance.py
uv run ludoweave plugin check examples/example.plugin.json
uv run python examples/alpha_acceptance.py
uv run ludoweave mcp --sample agent-world-builder
```

None of these commands needs a display, GPU, native compiler, or network listener.

The optional GPU slice has a separate locked install and smoke:

```console
uv sync --frozen --all-groups --extra graphics
uv run --frozen --extra graphics python examples/hello_sprite.py
uv run --frozen --extra graphics python examples/agent_world_builder.py
uv run --frozen --extra graphics python examples/render_device_conformance.py --backend wgpu
```
