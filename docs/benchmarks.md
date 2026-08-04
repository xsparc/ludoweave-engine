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
