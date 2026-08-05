# 2D rendering contract

M3 adds a backend-neutral render-device API, a deterministic validation
device, and one optional production adapter built on wgpu-py. Rendering is a
presentation concern: it can observe copied simulation values but cannot
mutate or participate in the canonical world hash.

## Install and select a backend

Headless simulation and the Null devices remain dependency-free. Install the
locked graphics extra only when GPU rendering is needed:

```console
uv sync --frozen --all-groups --extra graphics
uv run --frozen --extra graphics python examples/hello_sprite.py
```

The engine contracts and Null devices are available from `ludoweave.render`.
The production class is deliberately selected only by a composition root:

```python
from ludoweave.render.backends.wgpu import WgpuRenderDevice

device = WgpuRenderDevice()
try:
    print(device.capabilities)
finally:
    device.close()
```

`WgpuRenderDevice` is not re-exported from `ludoweave`,
`ludoweave.render`, or `ludoweave.render.backends`. Importing those public
packages does not import wgpu, rendercanvas, GLFW, or NumPy.

## Descriptors, handles, and ownership

Descriptors, commands, capabilities, captures, and handles are immutable
engine-owned records. They contain no provider enums, GPU objects, arrays, or
window objects. Resource handles combine a device UUID, slot index, and
generation. A handle from another device, the wrong resource kind, or a
retired generation fails with a structured `RenderError`.

A render device is single-owner and single-thread-affine. The constructing
thread creates, submits, resizes, destroys, polls, and closes it. Python object
collection never releases a critical GPU resource. `destroy(handle)` retires
the logical identity immediately. Physical destruction waits until the latest
referencing fence completes. `close()` is idempotent and releases every live
or deferred native resource.

Application composition owns the device. The older M0 `RenderBackend`
lifecycle remains the engine-loop boundary; M3's `RenderDevice` is the
resource/submission boundary and does not make a global device singleton.

## Presentation extraction and commands

`RenderExtractor` consumes immutable copied `SpriteExtractionSource` values.
It interpolates previous/current transforms, sorts by layer, z, and entity
identity, and groups by texture handle. `PresentationFrame` records the latest
completed simulation tick and interpolation alpha, but none of these records
can be encoded by the authoritative canonical serializer.

Every draw `CommandList` carries an explicit surface or render-texture target
and a sixteen-float orthographic camera matrix. A list may begin with one
clear. Sprite and tile batches identify only engine pipeline/texture handles.
Texture-atlas regions are normalized UV rectangles, so sprites sharing one
atlas form one normal instanced draw rather than one draw per sprite.

`RenderExtractor.build_command_list()` translates the same presentation frame
for either device. The Null and wgpu paths therefore validate equivalent
targets, handles, pipeline formats, batches, camera data, and counters.

## Sprite, tile, and debug behavior

The built-in wgpu pipeline draws six shader-generated quad vertices per
instance. One batch packs each sprite into a 64-byte provider-independent
record and performs one instanced draw. Alpha, additive, and opaque pipeline
blend modes are supported. A pipeline's color format must match its target.

Tile batches expand to sprite instances inside one draw. Layer/z/entity order
is deterministic before submission. Basic debug lines become white-texture
quads. Minimal diagnostic text uses an uppercase built-in 5x7 glyph set with a
question-mark fallback; it is intended for diagnostics, not game typography.
M11 bitmap atlas layout and glyph-sprite extraction are documented in the
[rich 2D presentation guide](presentation.md). Font parsing, international
shaping, and rich markup remain deferred.

## Surfaces, capture, and failure behavior

`SurfaceDescriptor` selects an offscreen or GLFW window surface. Resize uses
two positive integer dimensions. `(0, 0)` represents a minimized/suspended
surface and skips presentation until a positive extent is restored. Mixed
zero/nonzero dimensions are invalid. Destroying the surface closes its native
canvas after outstanding references complete.

Offscreen wgpu surfaces return `CaptureImage`: tightly packed immutable
RGBA8-unorm bytes with no NumPy or provider object. Capture before the first
frame, while minimized, from an onscreen surface, or after destruction fails
with a typed error. The Null device advertises no pixel-capture capability
because it validates semantics without inventing presentation pixels.

Adapter request, device creation, surface creation, unsupported capability,
stale handle, and device-loss failures use stable engine error codes and
bounded context. M3 treats provider operation loss as fatal for that device;
`simulate_device_loss()` exists on the exact adapter for deterministic
conformance testing. Automatic recovery and asset re-upload are deferred.

## Render graph and determinism

`RenderGraph.compile()` validates unique resources/passes, explicit transient
first/last use, dependency paths, writer-before-reader ordering, cycles, and
unordered read/write hazards. Declaration order does not affect the stable
topological result. The Null device can submit a compiled graph to exercise
the same command validation without a GPU.

GPU scheduling, rasterization, timestamps, raw window events, interpolation, and
captures are non-authoritative. They must never affect simulation commands,
receipts, snapshots, replay hashes, or random streams. Render ordering is
stable for equivalent extraction data; byte-identical captures across
different GPU implementations are not promised, so fixtures inspect tolerant
interior colors and semantic counters.

M4 adds `drain_surface_events(surface)`. Null devices return an empty tuple.
The optional wgpu adapter converts key, pointer, resize, and close data into
immutable `ludoweave.platform` records before returning. Provider dictionaries,
GLFW codes, native windows, and event timestamps do not cross the public
boundary. The Clockwork Arena example demonstrates action mapping; see
[the gameplay guide](gameplay.md).

M3 benchmark artifacts use CPU submission timing. Although some adapters
report native timestamp-query support, the engine capability remains false
until an engine-owned query/result lifetime is implemented.

## Exact dependency pins and upgrades

M3 pins `wgpu==0.32.0`, `rendercanvas==2.7.2`, and `glfw==2.10.2` in the
`graphics` extra and lockfile. The adapter contains a documented provider
workaround for wgpu-py 0.32 queue completion on Windows. A graphics dependency
upgrade must:

1. change all compatible pins together and regenerate `uv.lock`;
2. run the complete base and graphics quality suites;
3. run clear, sprite, resize, capture, and loss conformance on Windows,
   macOS, and Linux;
4. inspect tolerant capture fixtures and execute the 1k/10k benchmark before
   and after the change;
5. review the exact adapter for provider API changes, update this document and
   the changelog, and record an ADR if engine semantics change.

Do not add a second production renderer during this phase. ModernGL, 3D, PBR,
skeletal animation, a visual editor, and native acceleration are outside M3.
