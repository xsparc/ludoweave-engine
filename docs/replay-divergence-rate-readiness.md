# Replay-divergence-rate readiness

M32 defines how LudoWeave may report replay-divergence rate in CI without
turning passing jobs into an unsupported zero-rate claim. The evaluator is an
explicitly invoked offline evidence reader; neither the engine nor CI workflow
loads it during normal operation.

Run the current reviewed evidence:

```console
uv run python examples/replay_divergence_rate_readiness.py
```

The committed manifest is exactly 175 bytes with SHA-256
`cff8a32428ac8dcd18029be4f70e9d359b4c9d70fd411ffe2f36d35704d68aa7` and
contains no evaluation windows. The exact result is therefore `not-ready` with
reason `replay-divergence-rate-evidence-absent`, zero admitted executions, and
no divergence rate. Existing replay tests, passing workflow runs, and synthetic
fixtures prove engine behavior but do not establish a complete historical CI
cohort.

## Cohort and outcomes

A future admitted window must enumerate the complete reviewed public cohort of
eligible CI replay executions that started within its half-open time interval.
An eligible execution is a CI replay-verification case whose declared expected
result is exact reproduction of canonical state with hash verification enabled.
Intentionally corrupted negative fixtures, cases whose expected result is
divergence, and diagnostic runs with verification disabled are not eligible;
the reviewed census must exclude them before outcomes are known. An actual
divergence in an eligible verification case remains in the cohort and counts in
the numerator.
Every intended execution remains present as exactly one of:

- `verified`, with equal expected and actual state hashes;
- `diverged`, with distinct hashes, the first divergent tick, and the stable
  `world.replay.divergence` code; or
- `not-executed`, with no replay hashes or tick and an exact cancellation,
  pre-replay failure, skip, or unavailable-result reason.

The last state prevents cancelled and early-failing jobs from disappearing from
the denominator. A cohort containing any non-executed case is retained in
admitted counts but cannot publish a rate.

Each execution binds a canonical project workflow run and job, exact head
revision, immutable `ci.yml` source, replay-case source, and frozen result
artifact. Human review owns cohort completeness, eligibility, outcome,
provenance, and validation; the evaluator verifies only the frozen contract.

## Admission and history

Admission requires:

1. the exact reviewed whole-manifest SHA-256;
2. canonical sequential windows that are chronological and non-overlapping;
3. a positive execution interval of at most 366 days and an observation cutoff
   strictly after, but no more than 366 days after, it closes;
4. canonical project workflow-run, job, workflow-source, test-source, census,
   review, and result locations;
5. exact reviewed UTC timestamps, Git revisions, and SHA-256 identities;
6. unique run/job/case and frozen result identities;
7. canonical chronological execution order;
8. reviewed complete public CI census, eligibility, outcome, provenance, and
   validation; and
9. an executable mandatory prefix equal to the complete reviewed window
   history.

## Rate semantics

Only a complete admitted cohort with at least one execution and no
`not-executed` cases exposes `divergence_rate`. The rate is an exact rational
object: `numerator` is the divergent execution count and `denominator` is the
total verified-plus-diverged execution count. No rounded float, threshold,
quality verdict, release gate, reliability promise, or service level is
defined.

The sanitized report contains only counts, the exact rational rate when
admitted, policy/schema identities, and admission reasons. It never returns
run or job locations, timestamps, commit IDs, case names, state hashes, result
artifacts, paths, environment values, raw logs, or provider objects.

## Boundary

M32 changes no replay/runtime behavior, public API or export, persistent format,
workflow or job, dependency, lockfile, package version, stability label, tag,
release, publication, telemetry, networking, discovery, provider, or support
policy. The empty reviewed manifest is readiness machinery, not replay-history
evidence and not a measured zero-divergence result.
