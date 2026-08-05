# ADR-0023: provider-neutral gamepads and SDL3 adapter deferral

- Status: Accepted
- Date: 2026-08-05

## Context

The post-alpha sequence calls for gamepad input and an SDL3 adapter-maturity
evaluation. Gamepad state must reach the same immutable tick-indexed action
snapshot used by keyboard, pointer, virtual, and recorded input. Provider IDs,
objects, timestamps, native libraries, and polling order cannot become
canonical world state or leak through public APIs.

SDL 3.4.14 is stable and its gamepad API supplies standardized locations,
hotplug events, mappings, and optional capability discovery. SDL explicitly
requires applications to support hotplugging. Its current language-binding
inventory lists PySDL3 for Python. As evaluated on 2026-08-05, PySDL3's latest
PyPI release is `0.9.11b1`, is classified Beta, and downloads required native
binaries on first use by default. Rendercanvas 2.7.2 does not define gamepad
events or an SDL backend. Adding SDL now would therefore introduce a second
global event/library lifecycle and a runtime binary download outside the uv
lock and release inventory.

The already-pinned GLFW 2.10.2 dependency exposes standardized Xbox-like
gamepad buttons and axes, uses SDL-compatible mapping data, supports slots 0-15,
and polls state without provider objects crossing its boundary. GLFW reports
`0.0` both for an unavailable gamepad axis and for a legitimate half-pressed
trigger, so it cannot safely distinguish those trigger states.

## Decision

Add frozen engine-owned connection, button, and axis events for logical player
slots 0-15. Buttons and axes use closed `StrEnum` identities. Stick axes are
finite exact floats in `[-1.0, 1.0]`; triggers are normalized to `[0.0, 1.0]`.
`GamepadProvider` returns copied current states for supported controls in
ascending slot, button, and axis order and has explicit idempotent close
semantics. A provider omits a control when its availability or neutral value is
ambiguous; it never synthesizes active input.

`RenderDevice` implements this platform protocol. The Null device returns no
events. The exact optional wgpu adapter polls GLFW only while a GLFW window
surface is active, converts every provider value immediately, emits connection
changes, and never exposes GLFW state. It emits all standardized buttons and
four stick axes, but deliberately omits GLFW's ambiguous trigger axes. Provider
failure produces a chained structured platform error without marking the GPU
device lost. The adapter also samples GLFW window focus and emits the
engine-owned focus transition before queued input is drained.

`ActionBinding` accepts standardized gamepad button and axis controls. Axis
bindings require an explicit finite nonzero scale and may declare an axial
deadzone in `[0.0, 1.0)`. The mapper removes the deadzone and linearly rescales
the remaining magnitude to the full range before clamping combined actions.
Focus loss clears and suppresses live state; current supported-control polling
restores held controls after focus returns. Disconnect clears every control for
that slot. Only the resulting `InputSnapshot` may affect simulation or replay.

Defer an SDL3 adapter. Reconsider it only when all of these gates have evidence:

1. a non-prerelease maintained Python binding supports CPython 3.12-3.14;
2. every supported OS/architecture has auditable, checksum-pinned binary
   delivery with no default runtime download;
3. initialization, event pumping, hotplug, shutdown, and main-thread ownership
   coexist with or deliberately replace the rendercanvas window lifecycle;
4. gamepad conformance passes on Windows, macOS, and Linux with no provider
   value in public APIs or canonical state;
5. the base wheel remains pure Python with no mandatory native compiler or
   SDL dependency; and
6. a named maintainer accepts the adapter and binary-update burden.

## Consequences

- Keyboard, pointer, virtual, recorded, Null, and GLFW gamepad input converge
  on one action-snapshot boundary.
- Headless installs remain dependency-free and deterministic.
- Clockwork Arena can use standardized sticks and buttons in its existing
  interactive GLFW composition.
- The alpha does not promise haptics, LEDs, sensors, touchpads, raw joysticks,
  remapping UI, downloaded mapping databases, background input, or SDL windows.
- SDL3 remains a measured future adapter decision rather than an ambient
  dependency or a second production platform stack.

## Evidence sources

- [SDL current release and language bindings](https://www.libsdl.org/languages.php)
- [SDL3 gamepad API and hotplug guidance](https://wiki.libsdl.org/SDL3/CategoryGamepad)
- [PySDL3 package status and binary-loading model](https://pypi.org/project/PySDL3/)
- [GLFW standardized gamepad input](https://www.glfw.org/docs/latest/input)
- [rendercanvas event surface](https://rendercanvas.readthedocs.io/stable/api.html)
