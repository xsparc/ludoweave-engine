# RFC-0016: Benchmark-regression-rate admission readiness

- **Status:** Accepted
- **Date:** 2026-08-08

## Context

The design plan lists benchmark regression rate after replay-divergence rate in
its ordered longer-term metrics. LudoWeave has M1-M4 `perf_counter_ns`
benchmarks and M7 cProfile diagnostics, but it has no reviewed controlled
base/candidate benchmark cohort. A local measurement, an absolute target, a
passing smoke, or a profiling document cannot establish a historical
regression rate. Selecting only completed comparisons would also bias the
denominator.

M33 must define evidence admission without changing benchmarks, optimizing the
runtime, adding a runner/workflow, querying GitHub, or authorizing native code.

## Decision

Adopt the versioned
`ludoweave.performance.benchmark-regression-rate/1` reviewed manifest and the
explicitly invoked offline evaluator described in the
[readiness guide](../benchmark-regression-rate-readiness.md).

The manifest:

1. uses bounded chronological non-overlapping windows and a later observation
   cutoff;
2. requires a complete reviewed controlled-runner comparison census rather
   than successful-result selection;
3. restricts timing evidence to registered M1-M4 `time.perf_counter_ns`
   workloads and exact `p95_ns` values;
4. excludes M7 cProfile attribution documents from timing comparison;
5. binds distinct base/head revisions, both exact benchmark sources, candidate
   workflow source, a frozen runner profile, and frozen comparison artifacts;
6. fixes eligibility and an integer basis-point tolerance before outcome
   review;
7. preserves each eligible comparison as stable, regressed, or not-executed;
8. classifies the result with exact integer multiplication and treats equality
   at the tolerance boundary as stable;
9. requires reviewed eligibility, comparability, threshold predeclaration,
   outcome, provenance, validation, and census completeness;
10. rejects duplicate comparison and artifact identities and noncanonical
    order; and
11. preserves accepted history through an executable mandatory prefix before
    exposing an exact numerator/denominator rate.

A non-executed comparison remains counted but blocks rate publication. Human
review, not evaluator logic, establishes runner control and base/candidate
comparability.

## Current result

The reviewed manifest contains no evaluation windows. Its deterministic report
is `not-ready`, contains zero comparisons, and exposes no regression rate.
Existing benchmark files, local runs, profiling output, hosted smokes, and
synthetic populated fixtures do not establish the longer-term metric.

## Consequences

- A future admitted rate is exact and auditable without exposing per-run data
  in the report.
- Cancellation, early failure, skipping, and missing evidence cannot be
  silently removed from the cohort.
- A zero numerator can be reported only after at least one complete reviewed
  comparison cohort is admitted.
- No project-wide threshold, quality verdict, release gate, performance
  guarantee, reliability promise, SLA, native decision, or support promise is
  introduced.
- No engine/benchmark source, public export, workflow job, dependency, lock,
  version, provider, telemetry path, network behavior, Rust, PyO3, or WASM
  implementation changes.

## Alternatives considered

Treating existing absolute-target results as historical regressions was
rejected because they are not paired base/head evidence. Comparing cProfile
output was rejected because profiler attribution is not the benchmark timer.
Using a floating-point percentage was rejected because exact integer ratios
are deterministic. Adding a benchmark workflow or live telemetry was rejected
because M33 is an admission contract, not measurement infrastructure.
