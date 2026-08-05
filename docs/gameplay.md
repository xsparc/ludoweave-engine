# M4 gameplay vertical slice

M4 adds the first playable composition without changing the engine's canonical
state rule. Clockwork Arena stores transforms, player/enemy/projectile state,
and metrics in an authoritative `WorldSession`. Every tick is a versioned
`world.tick` transaction with a receipt. Its injected tick executor sees only a
staged world, staged resources, staged random streams, and one immutable input
snapshot; failed ticks cannot partially enter the live session.

## Run Clockwork Arena

The dependency-free Null device runs the same simulation and presentation
extraction used by the graphical path:

```console
uv run --frozen python examples/clockwork_arena.py --ticks 600
```

Install the locked graphics extra for an offscreen wgpu run:

```console
uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 600 --renderer wgpu --render-every 10
```

An interactive GLFW window uses engine-owned events only:

```console
uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 36000 --renderer wgpu --window --interactive
```

Use WASD or arrows to move, the pointer to aim, the primary mouse button to
fire, and R to restart after game over. Closing the window ends the loop. The
wgpu adapter translates provider events before returning them; no rendercanvas
dictionary, GLFW key, or native window enters the application API.

The automated action stream uses the same `InputSnapshot` representation. A
fixed seed and 3,600 snapshots reproduce an exact checked-in metrics/state-hash
fixture. A `RecordedInputSource` run reaches the same hash, and a shorter
`ReplayTimeline` test verifies transaction checkpoints through the M2 replay
service.

## Input contract

`InputSnapshot` is an immutable, tick-indexed sorted action collection. Digital
lookups expose `pressed`, `just_pressed`, and `just_released`; `axis2d("move")`
reads `move.x` and `move.y`. Virtual and recorded sources copy their inputs.
`MappedInputSource` is a single-owner accumulator that must be sampled at
sequential ticks.

`ludoweave.platform` owns key, mouse-button, pointer, focus, resize, and close
records. Pointer positions use logical surface dimensions and normalize to
[-1, 1]. Focus loss releases held controls. Platform processing, timestamps,
and window size are not authoritative until an application deliberately maps
an event to a recorded action snapshot.

## Asset identity and cache

`AssetUri` accepts normalized `asset://` identities with no traversal, query,
fragment, or platform separator. `AssetManifest` loads the exact
`ludoweave.assets/1` JSON schema and confines every source beneath the selected
project root, including after path resolution. The shipped example manifest is
`examples/clockwork_arena.assets.json`.

`AssetPipeline` hashes source bytes, logical URI, kind, loader version,
canonical scalar settings, and direct dependency artifact keys. Artifacts are
immutable files addressed by SHA-256. A content change invalidates that asset
and its dependents while unrelated keys stay stable.

The standard-library PNG loader is deliberately bounded: it accepts 8-bit,
non-interlaced RGB/RGBA images, verifies every chunk CRC, bounds source,
compressed, decompressed, and dimension sizes, applies filters 0-4, and emits
immutable RGBA8 bytes. `TextureSlot` swaps CPU revisions while retaining the
old revision until the renderer reports a completed safe-point fence. GPU
handles are never stored in asset manifests or canonical state.

## Collision and movement

M4 collision is a deterministic narrow slice, not a physics engine. `Aabb` and
`Circle` implement strict-area box/box, circle/circle, and mixed overlap. Edge
touching alone is not overlap. `SpatialGrid` indexes each collider into all
covered cells, returns sorted IDs, and exact-filters broad-phase candidates.
Hypothesis compares generated grid results with a brute-force reference.

Kinematic box movement resolves X and then Y against static AABBs sorted by
collider ID. Each axis detects crossings and clamps at first contact. There is
no impulse, mass, rotation, rigid-body solver, or Box2D integration. Clockwork
Arena uses the grid for projectile/enemy candidates and the axis policy for
arena bounds.

## Audio ownership

`AudioBackend` defines initialize, immutable clip load, play, stop,
master/category volume, looping, and close. `NullAudioBackend` validates this
lifecycle and opaque handle ownership while producing no sound. The owner
closes an injected backend; close is idempotent and invalid/foreign handles are
typed failures. No Python real-time audio callback or provider dependency is
introduced in M4.

## Stress evidence and limits

Clockwork Arena bounds active enemies and supports stress levels 1-16. The M4
benchmark records raw tick durations and p50/p95/p99 for stress 1, 4, and 8,
plus fixed seed, final metrics/hash, CPython/GIL metadata, commit, and dirty
state:

```console
uv run --frozen python benchmarks/benchmark_m4.py --samples 300 --warmups 60 --output .tmp/m4-benchmark.json
uv run --frozen python benchmarks/validate_m4_results.py .tmp/m4-benchmark.json
```

The 60 Hz baseline target is an observation in the artifact, not a release
gate. Higher stress workloads intentionally declare no target. A local miss is
profiling evidence and does not authorize native code.

M4 does not add MCP, networking, editor tooling, Box2D, a production audio
provider, arbitrary project Python, Rust, PyO3, or native compilation.
