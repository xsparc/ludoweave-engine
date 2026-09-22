# Replay-owned input history

`ludoweave.app.replay.InputReplay` is an experimental immutable artifact combining
a replay-v1 timeline and the exact input snapshots consumed over its tick range.
It needs no audio, graphics or external dependency.

Run these as separate processes from the repository root:

```console
uv run --frozen python examples/input_replay.py record recording.json --ticks 120
uv run --frozen python examples/input_replay.py replay recording.json
```

Recording refuses to overwrite an existing file. Both commands print identical
versioned summaries with the final world hash, complete artifact hash and verified
checkpoint count. Playback creates an empty-input game composition, then supplies
only the artifact's owned inputs to the trusted tick executor. The input generator
is not called during playback.

## Contract and ownership

### Record a play session

The Clockwork Arena play loop can capture the snapshots it actually consumes:

```console
uv run --frozen python examples/clockwork_arena.py --ticks 120 --record play.json
uv run --frozen python examples/input_replay.py replay play.json
```

For keyboard/mouse or gamepad play, add `--renderer wgpu --window --interactive`
to the recording command (requires the graphics extra). Optional `--audio device`
does not enter the recording. Headless verification needs neither extra nor the
original device. Compare its `state_hash` and `ticks` with the play summary's
`arena` fields; all embedded checkpoints are checked.

Recording is opt-in and limited to 3,600 requested ticks. Closing the interactive
window early saves only completed ticks, including a valid zero-tick session.
Inputs are sampled once by the tick executor, not polled again when saving.
The sample uses the existing M239 envelope and unchanged world transactions;
it adds no engine API or persistent protocol. Normal play output is unchanged.

The destination must not exist. Publication uses exclusive creation after the
loop and both device closes succeed; transaction, rendering, audio or close
failure does not publish a successful recording. File write failures may leave
a partial new file; saving is not crash-atomic and provides no hostile-filesystem
isolation. Keep valuable recordings elsewhere before retrying. Recording retains
bounded committed batches in memory; complete timeline validation and serialization
run at save time, not over the growing history on every tick. It is not a latency
guarantee or streaming recorder. Simulated event tests are not evidence of human
device provenance.

The envelope protocol is `ludoweave.input-replay/1`; embedded replay-v1 bytes,
checkpoints and hashes are unchanged. Every tick in `[initial_tick, final_tick)`
must appear exactly once in order. Nonzero start ticks support independent branch
artifacts. Empty histories are valid only for zero-tick timelines. Out-of-range
lookup refuses rather than generating empty actions.

Bounds: 60,000 ticks; 256 actions or names per transition list; 128 characters per
name; 250,000 aggregate action/transition entries; 64 MiB canonical bytes; JSON
depth 100, four million nodes and 100,000 items per collection. Input names,
finite analog values, exact booleans and edge transitions use existing validation.
The canonical codec preserves signed zero and does not conflate booleans/floats.
Decoded values and direct construction share the budgets.

`artifact.replay(runner, executor_factory)` verifies composition compatibility
before calling the explicitly trusted factory with the embedded input source.
The document selects no Python code or import. The caller owns any resources
created by its factory; execution is synchronous and not concurrently safe.
State hashes and checkpoints are always checked.
Unsupported embedded replay engine/determinism versions retain the existing
`IncompatibleReplayError`, distinct from malformed-input `InputError` failures.
Changed inputs can still decode, but cause replay divergence when they change
recorded world outcomes. Hashes are
not signatures and do not prove that an input history came from a human device.

Old replay-v1 files and their APIs continue to work as before. The new artifact
does not make arbitrary game code portable or admit networking/live rollback.
See [ADR-0035](adr/0035-replay-owned-input-history.md).

## Installed verification

### Display a verified recording

```console
uv run --frozen python examples/play_input_replay.py play.json
uv run --frozen --extra graphics python examples/play_input_replay.py play.json --renderer wgpu --window
```

The default Null renderer exercises the same presentation path without a GPU or
window. Omit `--window` for an unpaced offscreen wgpu run. Window playback uses
60-Hz tick deadlines; presentation timing never changes canonical state.

This bounded sample first verifies the entire artifact headlessly before opening
any renderer. A second pass applies the same recorded transactions and checks
their hashes, tick boundaries and checkpoints while drawing an initial frame and
one frame per batch. No growing-prefix replay runs per frame. Limits are 3,600
ticks and batches; initial snapshots preserve nonzero-start branches and stress
settings. Live gameplay input is ignored. Resize/close events affect presentation;
optional playback keys below never supply world input. Audio and arbitrary
game composition are not provided.

### Pause and single-step playback

The viewer displays a high-contrast status panel by default: current and final
tick, PLAYING/PAUSED/COMPLETE state, and hints for the enabled controls. It updates
on every displayed or paused frame, including after seeks. `--no-status` hides
the panel without changing replay summaries, frame counts, inputs or hashes.
The panel uses built-in diagnostic glyphs, not a downloaded font. Its fixed
logical screen layout scales with the surface; very small windows reduce text
legibility. It overlays the top of the game view rather than reserving world space.
The final COMPLETE frame does not change the existing automatic-exit behavior.

```console
uv run --frozen --extra graphics python examples/play_input_replay.py play.json --renderer wgpu --window --controls --paused
```

`--controls` opts into Space to pause/resume and Right Arrow to advance one tick
while paused. Omit `--paused` to start playing. A held key does not repeat; release
and press again for another step. Multiple step edges in one event drain coalesce
into at most one tick, and Right Arrow while playing is ignored. Close takes
priority over stepping. Gameplay keys and gamepads never alter recorded input.

Controlled playback requires a window and exactly one tick per recorded batch,
as produced by the sample recorder. Other batch spans are refused before replay
or device creation rather than splitting atomic transactions. Ordinary playback
and headless verification remain unchanged. Paused redraws keep resize/close
responsive with bounded polling sleeps, while canonical world ticks remain fixed.
Resume starts fresh 60-Hz presentation deadlines; paused time is not caught up.
Redraws count toward `frames`, so controlled frame counts need not equal ticks
plus one. Playback exits at the end, including an empty recording started paused;
it does not hold the final frame open. Window focus is needed for keyboard input.

### Seek and resume

```console
uv run --frozen python examples/play_input_replay.py play.json --seek-tick 60
uv run --frozen --extra graphics python examples/play_input_replay.py play.json --seek-tick 60 --renderer wgpu --window --controls --paused
```

`--seek-tick` is an absolute recorded tick, including for nonzero-start branches.
It must be an existing boundary between the initial and final ticks, inclusive;
invalid targets fail before provider creation. The earliest batch boundary at
that tick is selected if zero-tick transactions share a boundary. Full artifact
verification is still performed, including history before and after the target.
The chosen state is rebuilt using a verified replay prefix, drawn once, and then
the suffix plays normally. For the sample's one-tick batches, seeking to the final
tick displays that state and exits. Any zero-tick transactions after the selected
boundary still play; an empty recording accepts only its initial tick.

With `--controls`, paused Left Arrow rewinds one tick and Home returns to the
artifact's initial tick. Both stay paused; Space resumes. Held key repeats are
ignored, seeks at the initial boundary are no-ops, and close takes priority. A
seek discards pending forward stepping. These keys do nothing while playing.
Every actual seek reconstructs a fresh world session through existing verified
replay, without changing the artifact or reversing world commands. The renderer
stays owned by the viewer and closes on replay failure. Pacing is rebased on
resume, so neither skipped history nor pause time creates a catch-up burst.

Seeking is bounded by the viewer's 3,600 ticks/batches, but reconstruction is
synchronous and may briefly delay window handling. It replays from the initial
snapshot; hashes are not seekable state snapshots. No latency guarantee, saved
seek cache or per-frame prefix replay is provided.

When `--seek-tick` is supplied or a backward seek occurs, the existing JSON
summary additionally includes `start_tick`, `seek_count` (successful in-window
position changes only), and `position_batch` (current artifact cursor).
`played_batches` counts transactions applied for playback, excluding reconstruction;
rewatching history may make it exceed the artifact's batch count. `frames` includes
seek-state and paused redraws. Default output fields remain unchanged when no
seeking is requested or performed.

The JSON summary uses `ludoweave.input-replay-playback/1`. `verification: pass`
describes the full preflight; `playback: complete` or `interrupted` describes the
display pass separately. Closing early reports only played batches and their
current arena state; it does not claim the entire recording was displayed.
Device errors still close owned resources and fail instead of printing success.
The input file and persistent replay formats remain unchanged. Preflight adds
startup work; this is not a hard real-time guarantee or a physical-play attestation.

```console
uv run --frozen python scripts/smoke_input_replay_wheel.py .tmp/dist-first
```

This installs one built wheel with no dependencies into a temporary environment,
copies the examples outside the checkout, and compares separate recording/replay
processes plus the actual Null play and recorded-presentation loops under Python isolated mode. It makes no
physical-device claim and uses the existing CI smoke step without another job.
