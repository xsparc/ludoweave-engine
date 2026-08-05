# LudoWeave community-alpha samples

These samples run against an installed `ludoweave` wheel. Start with the
dependency-free headless paths:

```console
python hello_headless.py --ticks 120
python fixed_step_world.py --ticks 6
python clockwork_arena.py --ticks 600
python rich_2d_showcase.py --ticks 6
python alpha_acceptance.py
```

`rich_2d_showcase.py` exercises animation, bitmap text, chunked tilemaps,
fixed-point particles, Null-audio mixing, and Null rendering without a display
or audio device. `alpha_acceptance.py` checks engine lifecycle, stale entity generations,
Clockwork Arena, typed agent operations, replay evidence, provider ownership,
and registered Agent World Builder tests without a display, network listener,
or native compiler.

For optional WebGPU presentation, install the exact release's `graphics` extra
and run:

```console
python hello_sprite.py
python agent_world_builder.py
python clockwork_arena.py --ticks 600 --renderer wgpu
```

Add `--window --interactive` to the final command for the desktop Clockwork
Arena controls. The bundle is example source, not a plugin/project loader; read
the version-matched user and adapter guides before reusing experimental APIs.
