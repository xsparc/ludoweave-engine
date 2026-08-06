# LudoWeave community-alpha samples

These samples run against an installed `ludoweave` wheel. Start with the
dependency-free headless paths:

```console
python hello_headless.py --ticks 120
python fixed_step_world.py --ticks 6
python clockwork_arena.py --ticks 600
python rich_2d_showcase.py --ticks 6
python rollback_readiness.py --ticks 120 --branch-tick 60
python constrained_3d_decision.py
python visual_editor_decision.py
python wasm_mod_security_decision.py
python render_device_conformance.py
python world_store_conformance.py
python world_store_conformance.py --backend reference
python agent_tool_conformance.py
python alpha_acceptance.py
ludoweave plugin check example.plugin.json
```

`rich_2d_showcase.py` exercises animation, bitmap text, chunked tilemaps,
fixed-point particles, Null-audio mixing, and Null rendering without a display
or audio device. `alpha_acceptance.py` checks engine lifecycle, stale entity generations,
Clockwork Arena, typed agent operations, replay evidence, provider ownership,
and registered Agent World Builder tests without a display, network listener,
or native compiler.

`example.plugin.json` is inert compatibility metadata for the preview M12
manifest protocol. The checker validates it against the current engine,
CPython, and desktop platform without importing or executing plugin code.

`rollback_readiness.py` proves bounded offline replay branching with corrected
future input, records the still-external input-history dependency, and emits a
deferred networking decision. It opens no listener and implements no transport
or live rollback service.

`constrained_3d_decision.py` audits the installed public render and built-in
world-operation surfaces. It emits a deterministic deferred decision and adds
no 3D API, provider, asset loader, or runtime implementation.

`visual_editor_decision.py` audits the installed command, receipt, agent-tool,
MCP, and inspector foundation. It records a deterministic deferred admission
decision and adds no GUI, editor runtime, public API, dependency, or project
format.

`wasm_mod_security_decision.py` audits the installed data-only plugin boundary,
proves that executable manifest fields remain rejected, and records a deferred
WASM-mod decision. It does not compile, instantiate, or execute guest code.

`render_device_conformance.py` runs the versioned baseline profile against an
explicitly selected trusted adapter. The dependency-free default validates the
Null device; `--backend wgpu` validates the optional production adapter. It
does not discover, import by name, install, sandbox, or certify third-party
code.

`world_store_conformance.py` runs the versioned storage-neutral baseline against
an explicit built-in `World` or `ReferenceWorld` factory. It validates entity
generations, epochs, copy isolation, queries, atomic command buffers, cloning,
and structured failures without discovery, persistence, provider imports, or an
external-resource lifecycle.

`agent_tool_conformance.py` runs the versioned 12-tool baseline against an
explicit built-in direct-service factory and a fresh clean authority. It does
not accept a module name, discover a transport, install code, start a process,
open a network connection, sandbox, or certify third-party code.

For optional WebGPU presentation, install the exact release's `graphics` extra
and run:

```console
python hello_sprite.py
python agent_world_builder.py
python clockwork_arena.py --ticks 600 --renderer wgpu
```

Add `--window --interactive` to the final command for the desktop Clockwork
Arena controls. The bundle is example source, not a plugin/project loader; read
the version-matched user, plugin, and adapter guides before reusing experimental
or preview APIs.
