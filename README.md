# LudoWeave Engine

**Build worlds humans can play and agents can operate.**

LudoWeave is an experimental, headless-first Python engine for 2D and
layered-2D games. Humans and software agents operate the same world through
typed, validated commands with receipts. Simulation state lives in the world
store; rendering and audio are optional presentation layers.

## What you can build

- Deterministic fixed-tick worlds with entities, components and typed resources.
- Recorded simulations with snapshots, checkpoints and replay-owned input history.
- 2D games with input mapping, sprites, tilemaps, animation and optional audio.
- Local agent-controlled worlds using the Python service, CLI or stdio interface.
- Data-only scenes and prefab fragments with explicit asset validation workflows.

**Status:** community-alpha release candidate. Most APIs are experimental;
the plugin manifest surface is preview. This is not a stable or complete game
runtime. Network transports, a visual editor, 3D, executable plugins and native
acceleration remain deferred. See [API compatibility](API_COMPATIBILITY.md)
and the [roadmap](ROADMAP.md) before depending on a feature.

## Quick start

From a checkout of this repository, install [uv](https://docs.astral.sh/uv/)
0.11.x and use standard CPython 3.12–3.14 on Windows, macOS or Linux.
The headless path needs neither a GPU nor a native compiler.

```console
uv sync --frozen --all-groups
uv run --frozen ludoweave --version
uv run --frozen ludoweave doctor
uv run --frozen python examples/hello_headless.py --ticks 120
```

The headless example runs 120 virtual ticks, closes its resources and prints
a JSON summary. It opens no window and does not wait for real-time ticks.

## Try a game

Run Clockwork Arena with deterministic scripted input and no window:

```console
uv run --frozen python examples/clockwork_arena.py --ticks 600
```

For a playable window, use the optional graphics extra and a supported GPU:

```console
uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 36000 --renderer wgpu --window --interactive
```

Use WASD/arrows to move, the pointer to aim, the primary mouse button to fire,
and R to restart. Gamepad slot 0 supports sticks, A and Start.
See the [gameplay guide](docs/gameplay.md) for details.

Optional sound uses `--extra audio` with `--audio device`; it opens your default
audio output and plays quiet synthesized effects. Linux also needs system
PortAudio (for example, `libportaudio2` on Debian/Ubuntu). See the
[audio contract](docs/rfcs/0220-optional-blocking-audio.md).

## Learn and extend

- [User guide](docs/user-guide.md): engine setup and existing workflows.
- [Command workflows](docs/cli-workflows.md): operate a world from the CLI.
- [Input replay](docs/input-replay.md): record and verify in separate processes.
- [Agent control](docs/agent-control.md): typed local observation and commands.
- [Architecture](docs/architecture.md) and [runtime contract](docs/runtime-contract.md):
  state ownership, lifecycle, threading and determinism boundaries.
- [Adapter guide](docs/adapter-guide.md): backend isolation and extension contracts.
- [Documentation index](docs/index.md): detailed guides and reference material.

## Contribute

Start with the [contribution guide](CONTRIBUTING.md) and
[first-contribution walkthrough](docs/first-contribution.md).
The [quality guide](docs/quality.md) contains checks, package smoke tests and
benchmark procedures. Detailed historical validation notes are preserved in the
[historical README reference](docs/readme-history.md),
[changelog](CHANGELOG.md) and [test evidence](.project/TEST_EVIDENCE.md).

Contributions use DCO sign-off, not a CLA. Read the
[code of conduct](CODE_OF_CONDUCT.md), [security policy](SECURITY.md),
[governance model](GOVERNANCE.md) and [maintainer contract](MAINTAINERS.md).
Licensed under [Apache-2.0](LICENSE).
