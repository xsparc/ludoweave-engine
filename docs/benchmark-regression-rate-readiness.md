# Benchmark-regression-rate readiness

M33 defines how LudoWeave may report benchmark-regression rate without
reclassifying ad-hoc local timings, cProfile diagnostics, or isolated green
jobs as controlled performance history. The evaluator is an explicitly
invoked offline evidence reader; neither the engine nor CI loads it during
normal operation.

Run the current reviewed evidence:

```console
uv run python examples/benchmark_regression_rate_readiness.py
```

The committed manifest is exactly 199 bytes with SHA-256
`720ae794e2a4ba76303196cd43d6ba0f3b21f81cffd4fa8584f526e2a0d48dca` and
contains no evaluation windows. The exact result is `not-ready` with reason
`benchmark-regression-rate-evidence-absent`, zero admitted comparisons, and no
regression rate. Existing M1-M4 benchmark artifacts, M7 cProfile output, CI
smokes, local measurements, and synthetic fixtures do not establish a
controlled paired historical cohort.

## Eligible comparisons

A future admitted window must enumerate the complete reviewed cohort of
eligible controlled benchmark comparisons started in its half-open interval.
Eligibility is fixed before outcomes. A comparison must:

1. run the same registered M1, M2, M3, or M4 workload at a base and candidate
   revision;
2. use that workload's `time.perf_counter_ns` `p95_ns` result;
3. bind both exact benchmark source files, the candidate workflow source, a
   frozen runner profile, and frozen baseline/candidate artifacts;
4. use the same reviewed environment profile and workload parameters for both
   sides; and
5. declare its integer basis-point tolerance before the candidate outcome is
   reviewed.

M7 `ludoweave.profile.m7/1` cProfile documents are diagnostic attribution
evidence and are not eligible timing comparisons. Human review owns runner
control, parameter equality, isolation, warmup/sample adequacy, eligibility,
comparability, threshold predeclaration, provenance, and artifact validation.
The evaluator verifies only the frozen bounded contract.

Every eligible comparison remains present as exactly one of:

- `stable`, with complete positive p95 evidence at or below its predeclared
  tolerance;
- `regressed`, with complete positive p95 evidence above that tolerance; or
- `not-executed`, with no baseline/candidate timing artifacts and an exact
  cancellation, pre-benchmark failure, skip, or unavailable-evidence reason.

The last state prevents cancellations and early failures from disappearing
from the cohort. It remains counted but blocks rate publication.

## Exact rate semantics

All classification uses integer arithmetic. A candidate is regressed exactly
when:

```text
candidate_p95_ns * 10_000 > baseline_p95_ns * (10_000 + tolerance_bps)
```

Equality is stable. Only an admitted non-empty cohort with no `not-executed`
comparison exposes `regression_rate`. Its numerator is the regressed count and
its denominator is the stable-plus-regressed count. No floating-point percent,
project-wide performance target, quality verdict, release gate, reliability
promise, service level, or native-acceleration decision is defined.

## Admission and history

Admission requires the exact reviewed whole-manifest SHA-256; bounded
chronological non-overlapping windows; a strictly later observation cutoff;
canonical project run/job and immutable source/evidence locations; exact UTC,
Git, and SHA-256 identities; unique comparison and artifact identities; all
required human review flags; and a mandatory prefix equal to the complete
accepted history.

The sanitized report contains only aggregate counts, the exact rational rate
when admitted, policy/schema identities, and admission reasons. It never
returns runs, jobs, revisions, workload names, timestamps, tolerances, timings,
runner/environment values, artifact locations, local paths, raw logs, or
provider objects.

## Boundary

M33 changes no runtime or benchmark implementation, optimization, public API,
export, persistent format, workflow, CI job, dependency, lockfile, package
version, provider, telemetry path, native/WASM boundary, release, publication,
or support policy. The empty reviewed manifest is readiness machinery, not a
measured zero-regression result.
