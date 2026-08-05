# Fixed-step application runtime

`FixedStepApplication` composes a world, resources, a validated serial schedule, immutable input, an injected clock, and an engine-owned render backend. It is additive: the M0 `Engine` and root exports retain their original behavior.

## Exact time and catch-up

`ApplicationConfig(fixed_hz=60, catch_up_limit=4)` uses exact positive integers. Each pump adds:

```text
accumulator_units += elapsed_nanoseconds × fixed_hz
```

One simulation tick consumes exactly 1,000,000,000 units. This avoids drift at rates such as 60 Hz. At most `catch_up_limit` ticks execute per pump; excess whole ticks remain as backlog and can be drained by later pumps even when the clock does not advance. Time is never silently dropped.

`FrameSummary.interpolation_alpha` and frame count are presentation diagnostics. Alpha is clamped to 1 while whole-tick backlog remains. Neither value may affect input, systems, resources, world epochs, or future authoritative hashes.

`run_ticks(count)` is a deterministic headless convenience using absolute deadlines. It cannot be mixed with `pump()` on one application instance.

## Immutable input

Actions are exact bool or finite-float values with unique stable names. Snapshots are lexically ordered, frozen, and indexed by zero-based tick. Equality and hashing preserve the exact value kind and `float.hex()` representation, so digital `True` differs from analog `1.0` and `-0.0` differs from `0.0`. Missing ticks produce an empty snapshot for all built-in sources.

```python
from ludoweave.app import InputSnapshot, VirtualInputSource

source = VirtualInputSource({0: {"jump": True}, 5: {"move.x": -0.5}})
assert source.snapshot_for_tick(1) == InputSnapshot(1)
```

`RecordedInputSource` is an owned in-memory sequence for repeatability tests. It is not an M2 replay file, codec, or event log.

The application registry must include the exact `INPUT_SNAPSHOT_RESOURCE` key. The runner publishes one detached snapshot before PRE_SIMULATE. A system that reads input declares that key in `resource_reads`; schedules declaring it writable are rejected because the timeline is application-owned.

## System context and access

A context is active only during its system call:

```python
@system(
    name="movement.integrate",
    component_writes=(Transform2D,),
    resource_reads=(INPUT_SNAPSHOT_RESOURCE,),
)
def integrate(context: SystemContext, delta: float) -> None:
    input_snapshot = context.resource(INPUT_SNAPSHOT_RESOURCE)
    with context.query(Transform2D).writes(Transform2D).rows() as rows:
        for _entity_id, transform in rows:
            if input_snapshot.value("move.right") is True:
                transform.x += delta
```

- Query include, exclude, changed, and write access must be declared.
- Zero-component entity-set queries are rejected because M1 has no structural-read declaration.
- Context queries default to stable entity order.
- Write-declared resource values are committed after successful system return; read-only detached mutations are discarded.
- Spawn/add/remove command component types require declared component writes. Empty spawn and entity destruction are rejected by the M1 context because their entity-set effects cannot yet be represented in scheduler conflict metadata; direct world/local-command APIs remain available outside scheduled systems.
- POST_SIMULATE cannot enqueue structural commands.
- Retained contexts, query builders, rows, and command facades fail after invocation.
- An open writable cursor at return is aborted and fails the system rather than being committed implicitly.

These checks are practical guardrails, not a Python sandbox. System code marked deterministic must still avoid wall time, global randomness, I/O, mutable globals, hidden backend state, and retained aliases.

## Tick and failure order

For each tick the runner publishes input, executes PRE_SIMULATE then SIMULATE, flushes their shared local commands once, executes POST_SIMULATE, and only then increments the completed tick count. Post systems see the structural flush.

M1 does not roll back an entire failed tick. Unflushed commands are cleared and an incomplete tick is not counted. Earlier committed row/resource writes or a structural flush that completed before a later POST failure remain. Structured errors chain the cause and identify available tick, phase, system, or flush operation context. Persistent transactions, receipts, rollback, state hashes, and replay arrive in M2.

The application revalidates an injected schedule against a freshly built canonical deterministic plan before execution, so directly forged order/conflict metadata is rejected. The application owns and closes its render backend exactly once. The world and resource store remain inspectable after stop/close. All application lifecycle and pump calls must run on the constructing thread. Invocation cleanup and transition to `STOPPED` also run when a system raises `KeyboardInterrupt`, `SystemExit`, or another `BaseException`; those control-flow exceptions remain unwrapped.
