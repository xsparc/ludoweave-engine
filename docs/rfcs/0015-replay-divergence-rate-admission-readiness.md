# RFC-0015: Replay-divergence-rate admission readiness

- **Status:** Accepted
- **Date:** 2026-08-08

## Context

The design plan lists replay-divergence rate in CI as the next longer-term
metric after response and review latency. LudoWeave already has canonical
replay verification and CI exercises, but a passing workflow is not a complete
historical replay-execution cohort. Jobs can be cancelled, fail before replay,
skip cases, or lose result evidence. Selecting only successful executions would
bias the denominator and could manufacture a zero rate.

M32 must define evidence admission without changing replay behavior, collecting
telemetry, querying GitHub, or modifying the CI topology.

## Decision

Adopt the versioned `ludoweave.ci.replay-divergence-rate/1` reviewed manifest
and the explicitly invoked offline evaluator described in the
[readiness guide](../replay-divergence-rate-readiness.md).

The manifest:

1. uses bounded chronological non-overlapping execution windows and a later
   observation cutoff;
2. requires a complete reviewed public CI census rather than successful-run
   selection;
3. defines eligibility before outcomes as CI replay-verification cases expected
   to reproduce canonical state with hash verification enabled, excluding
   intentionally divergent negative fixtures and verification-disabled
   diagnostics;
4. preserves every eligible replay case as verified, diverged, or
   not-executed, including an actual divergence in an eligible case with the
   runtime's stable `world.replay.diverged` diagnostic;
5. binds executions to canonical public run/job locations, exact workflow and
   case sources, frozen result evidence, UTC timestamps, and SHA-256 identities;
6. requires reviewed eligibility, outcome, provenance, validation, and census
   completeness;
7. rejects duplicate execution/result identities and noncanonical order;
8. preserves complete accepted history through an executable mandatory prefix;
   and
9. emits only sanitized aggregate counts plus an exact numerator/denominator
   rate after complete admission.

A non-executed case remains counted but blocks rate publication. Human review,
not evaluator logic, establishes which CI replay executions were eligible,
whether the census is complete, and whether frozen outcome evidence is valid.

## Current result

The reviewed manifest contains no evaluation windows. Its deterministic report
is `not-ready`, contains zero executions, and exposes no divergence rate.
Passing project tests, hosted jobs, release smokes, and synthetic populated
fixtures do not establish the longer-term metric.

## Consequences

- A future admitted rate is exact and auditable without revealing per-run data
  in the report.
- Cancellation, early failure, skipping, and missing result evidence cannot be
  silently removed from the cohort.
- A zero numerator can be reported only after at least one complete reviewed
  execution cohort is admitted.
- No threshold, quality verdict, release gate, reliability guarantee, or
  service-level promise is introduced.
- No engine module, replay protocol, public export, workflow job, dependency,
  lock, version, provider, telemetry path, or network behavior changes.

## Alternatives considered

Treating every green CI run as zero divergence was rejected because a workflow
conclusion is not a complete replay-execution census. Counting only replay tests
that reached an assertion was rejected because cancellation and pre-replay
failure would disappear. A floating-point percentage was rejected because an
exact integer ratio is simpler and deterministic. Adding live telemetry or a
GitHub client was rejected because this evidence can be reviewed and frozen
offline.
