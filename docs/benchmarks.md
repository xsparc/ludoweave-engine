# Benchmark discipline

M1 closes with an executed pure-Python baseline, not a universal performance
claim. The suite covers entity create/destroy/reuse, 10,000-entity read and
writable queries, a seeded 100-system DAG plan, a 1,000-command staged flush,
a 3,600-tick headless run, and one representative 10,000-entity application tick.

```console
uv run --frozen python benchmarks/benchmark_m1.py --samples 30 --seed 1 --json-out .tmp/m1-benchmark.json
uv run --frozen python benchmarks/validate_m1_results.py .tmp/m1-benchmark.json
```

The raw JSON records every sample plus nearest-rank p50/p95/p99 values, workload
version and counts, warmups, seed, sanitized OS/architecture/processor and CPython
debug/release plus GIL/free-threaded build/runtime metadata, package/tool versions,
commit, and dirty-tree state. It deliberately
omits paths, usernames, hostnames, environment values, and credentials. Setup is
outside the timer where the named workload is an operation on an existing world.

The validator recomputes distributions and target observations. It does not fail
solely because a local machine misses an engineering target: the design's 4 ms
p95 representative simulation tick and 5x-real-time headless values are starting
optimization signals, not compatibility or release promises. A miss authorizes
profiling and ordinary Python/algorithm work only. Native acceleration still
requires the later RFC and multi-platform evidence gate.

## M2 informational protocol workloads

M2 adds measurements for canonical transaction encoding/decoding, atomic
transaction application, complete snapshot encode/decode, and verified replay:

```console
uv run --frozen python benchmarks/benchmark_m2.py --samples 30 --seed 1 --json-out .tmp/m2-benchmark.json
uv run --frozen python benchmarks/validate_m2_results.py .tmp/m2-benchmark.json
```

Each workload retains raw `perf_counter_ns` durations and `tracemalloc` peak
bytes plus nearest-rank duration p50/p95/p99 and peak-memory p95. Fixtures and
workload versions are exact, setup/warmup counts are explicit, and metadata
excludes paths, usernames, hostnames, environment values, and credentials.

No M2 timing or memory budget is defined. The validator therefore requires
`target: null` and checks only artifact integrity. These measurements support
future profiling; they do not constitute a performance pass, cross-platform
claim, or evidence for native acceleration.

## M3 renderer workloads

M3 records extraction plus 64-byte instance packing and CPU submission through
both the Null and wgpu devices at 1,000 and 10,000 visible sprites:

```console
uv run --frozen --extra graphics python benchmarks/benchmark_m3.py --samples 30 --output .tmp/m3-benchmark.json
uv run --frozen --extra graphics python benchmarks/validate_m3_results.py .tmp/m3-benchmark.json
```

Every workload records raw `perf_counter_ns` samples and nearest-rank
p50/p95/p99, exact visible-sprite and draw counts, warmups, dependency
versions, sanitized machine metadata, engine version, commit/dirty state, and
engine-owned render capability limits. The normal 1k and 10k workloads must
report one draw, proving that results are not produced with per-sprite draws.

The validator recomputes all distributions and the design's 3 ms p95 starting
targets for 10k extraction/packing and wgpu CPU submission. It records whether
each target was observed and validates that boolean against measured data; it
does not turn an honest local miss into an artifact failure or a performance
pass. Cross-platform timing claims require controlled runners.

## M4 Clockwork Arena stress workloads

M4 measures canonical transaction-backed Arena ticks after one deterministic
wave has been composed, at stress levels 1, 4, and 8:

```console
uv run --frozen python benchmarks/benchmark_m4.py --samples 300 --warmups 60 --output .tmp/m4-benchmark.json
uv run --frozen python benchmarks/validate_m4_results.py .tmp/m4-benchmark.json
```

Each workload records every raw duration, nearest-rank p50/p95/p99, the fixed
seed and stress level, final exact gameplay metrics and state hash, sanitized
CPython/GIL/platform metadata, and commit/dirty state. The baseline stress-1
workload records whether its p95 was below one 60 Hz frame (16.666667 ms).
Stress 4 and 8 deliberately have no target. Validation checks evidence
integrity; an honest target miss remains profiling evidence rather than a
release failure or native-code authorization.

## M7 profiling and native-code decision

M7 profiles the exact representative 10,000-entity simulation tick and
10,000-sprite extraction/packing workloads. With the graphics extra it also
profiles the exact 10,000-sprite wgpu CPU-submission workload:

```console
uv run --frozen python -m benchmarks.profile_m7 --repeats 5 --output .tmp/m7-profile-base.json
uv run --frozen python -m benchmarks.validate_m7_profile .tmp/m7-profile-base.json
uv run --frozen --extra graphics python -m benchmarks.profile_m7 --repeats 5 --include-wgpu --output .tmp/m7-profile-graphics.json
uv run --frozen python -m benchmarks.validate_m7_profile .tmp/m7-profile-graphics.json
```

Profile setup and warmup occur before `cProfile` begins. `profiled_repeats`
states exactly how many workload operations are aggregated. Profile time
includes deterministic instrumentation overhead and is diagnostic only: do not
compare it directly with benchmark p50/p95/p99 values or report it as frame
time.

Schema `ludoweave.profile.m7/1` stores exact workload parameters, total calls,
and the top 25 cumulative hotspots. Paths are normalized to module identities,
raw memory addresses are removed, and the artifact excludes usernames,
hostnames, environment values, and credentials. The validator enforces exact
fields, workload order, parameters, result invariants, sanitized metadata, and
canonical hotspot order.

The associated [native-code RFC](rfcs/0001-defer-first-native-kernel.md)
records the final 30-sample measurements and explains why M7 improves the
ordinary Python paths but does not admit Rust/PyO3.
