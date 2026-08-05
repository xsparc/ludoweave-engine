# Runtime contract

The M0 API is experimental, but its behavior is explicit so tests and later milestones have a reliable starting point.

## Lifecycle

```text
CREATED -> INITIALIZING -> READY -> RUNNING -> STOPPED -> CLOSED
                         \ failure -> FAILED -> CLOSED
```

- `initialize()` is valid once from `CREATED` and initializes the owned render backend.
- `run(ticks)` is valid once from `READY`, accepts a non-negative integer, executes exactly that many fixed ticks, and ends in `STOPPED` even when tick execution raises.
- `shutdown()` moves `READY` or `RUNNING` to `STOPPED`. Other public calls are rejected with a `LifecycleError`.
- `close()` may be called from any non-closed state, is idempotent, and attempts owned-resource cleanup once.
- Context entry initializes. If entry fails, partial backend state is closed before the initialization error is re-raised.
- Context exit always calls `close()` and does not suppress an exception from the context body.

The engine records its creating thread. Lifecycle methods from another thread fail rather than racing. M0 does not promise thread safety or free-threaded CPython support.

## Time

The `Clock` protocol exposes `now_ns()` and `wait_until_ns(deadline_ns)` using monotonic nanoseconds.

- `MonotonicClock` delegates to the operating system's monotonic clock and sleeps until a deadline. Wall-clock timestamps are never read.
- `VirtualClock` advances instantly to a deadline and rejects movement into its past.
- For one-based tick `n`, the engine waits for `start_ns + floor(n * 1_000_000_000 / fixed_hz)`. Deadlines are derived independently, so integer rounding does not accumulate.

Virtual time makes headless acceptance tests fast and deterministic. Monotonic scheduling validates the shape of the future interactive loop but is not authoritative state.

## Rendering

The backend-neutral `RenderDescriptor` contains only width, height, and a diagnostic label. Dimensions must be positive integers and the label must contain non-whitespace text.

`RenderBackend` has explicit initialize, per-tick render, and close operations. `NullRenderBackend` accepts no native resource, counts validated frames, rejects calls out of order, and allows repeated close calls.

## Errors and failure behavior

All expected engine failures derive from `LudoWeaveError` and provide:

- stable machine-readable `code`;
- `subsystem` and optional lifecycle `phase`;
- immutable, JSON-compatible contextual fields;
- `as_dict()` for diagnostic adapters;
- normal Python exception chaining for the underlying failure.

Diagnostics avoid environment variables, user paths, and exception messages from unknown adapters. Unexpected backend failures are identified by exception type while the original exception remains available through `__cause__`.

## Compatibility

Version `0.1.0a1` is community alpha. Every M0 runtime export remains
experimental under the [API policy](api-status.md). Persistent commands,
receipts, snapshots, and replay were added in M2 with independent versioned
protocols; their existence does not make the M0 Python symbols stable.
