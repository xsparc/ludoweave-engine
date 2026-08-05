# M1 and M2 benchmarks

The M1 suite records correctness-first pure-Python baselines for entity lifecycle,
10,000-entity read and writable queries, deterministic scheduler planning, staged
command flush, a 3,600-tick headless run, and a representative 10,000-entity
simulation tick.

Run it from the repository root after syncing the frozen environment:

```console
uv run --frozen python benchmarks/benchmark_m1.py --samples 30 --seed 1 --json-out .tmp/m1-benchmark.json
uv run --frozen python benchmarks/validate_m1_results.py .tmp/m1-benchmark.json
```

Setup is outside each measured interval where the workload is specifically an
operation over an existing world or application. Warmups precede the retained raw
samples. Percentiles use the nearest-rank method and are recomputed by the validator.
The output records sanitized OS, processor architecture, CPython debug/release and
GIL/free-threaded build/runtime status, package/tool,
commit, dirty-tree, seed, workload count, warmup, raw-sample, and target-observation
metadata. It intentionally records no paths, usernames, hostnames, environment
values, or credentials.

The 4 ms simulation-tick and 5x-real-time headless values are local engineering
observations, not release promises. The validator checks that observations agree
with the raw data; it does not turn one machine's result into a universal pass/fail
claim. A missed target is evidence for ordinary Python profiling and algorithmic
work, not authorization to add native code.

The M2 suite is informational and has no timing target. It records duration and
`tracemalloc` peak-memory samples for canonical 100-command round trips, atomic
100-command apply, 1,000-entity snapshot round trips, and verified 100-batch
replay:

```console
uv run --frozen python benchmarks/benchmark_m2.py --samples 30 --seed 1 --json-out .tmp/m2-benchmark.json
uv run --frozen python benchmarks/validate_m2_results.py .tmp/m2-benchmark.json
```

The M2 validator requires exact versioned fixture parameters, raw-sample counts,
nearest-rank p50/p95/p99 durations, p95 peak bytes, sanitized environment/commit
metadata, and a null target for every workload. Results are profiling baselines,
not a release gate or native-acceleration justification.
