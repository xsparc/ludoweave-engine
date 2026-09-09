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
bounded history in memory and adds serialization overhead; it is not a latency
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

```console
uv run --frozen python scripts/smoke_input_replay_wheel.py .tmp/dist-first
```

This installs one built wheel with no dependencies into a temporary environment,
copies both examples outside the checkout, and compares separate recording/replay
processes plus the actual Null play loop under Python isolated mode. It makes no
physical-device claim and uses the existing CI smoke step without another job.
