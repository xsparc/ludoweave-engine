# Response and review latency readiness

M31 makes the design plan's issue-response and pull-request-review time metric
mechanically admissible without adding telemetry or treating project automation
as community-support evidence. The reviewed manifest is empty, so no response
or review latency measurement is currently admitted.

Run the deterministic source-tree evaluator with:

```console
uv run python examples/response_review_latency_readiness.py
```

The current report is `not-ready`, has zero windows and measurements, and uses
reason code `response-review-latency-evidence-absent`. The exact 199-byte
manifest has SHA-256
`bc40bbcc1636229fa2c78aed5f71854d1221fd3c0d33169edc1321dd07e69d4f`.
The same evaluator and manifest are exercised from an isolated wheel and the
release sample bundle.

## What a future window means

A future admitted measurement window covers every reviewed eligible public
issue and pull request opened during one bounded interval. Manual reviewers
must establish that:

- each subject was opened by an external human rather than a maintainer, bot,
  service account, or project-directed automation;
- the frozen census includes every eligible subject, including items that still
  have no qualifying action at the observation cutoff;
- an observed issue action is the first qualifying public response by a human
  maintainer;
- an observed pull-request action is the first qualifying substantive public
  review by a distinct human maintainer;
- public resource/action locations, frozen source snapshots, review records,
  timestamps, outcomes, and provenance agree; and
- the window census and review artifacts are public project files at the same
  immutable Git revision.

The evaluator cannot establish those social and provenance facts. It checks
only the deliberately frozen reviewed record.

Pending items remain in the admitted cohort with null action and latency
fields. This prevents a report from silently selecting only fast completed
responses. An admitted report exposes eligible, observed, and pending counts
for each kind. It calculates a deterministic median over observed integer
seconds and a nearest-rank p95. At least one observed issue response and one
observed pull-request review are required before the metric is reportable.

`ready` means only that a complete reviewed cohort can be measured. M31 defines
no target, service-level objective, quality verdict, release gate, or support
promise. Counts and latency aggregates must be interpreted with their observed
and pending sample sizes.

## Admission and history

The evaluator requires:

1. the exact reviewed whole-manifest SHA-256;
2. canonical sequential windows that are chronological and non-overlapping;
3. a positive opening interval of at most 366 days and an observation cutoff
   no more than 366 days after it closes;
4. canonical public project issue, pull-request, issue-comment, and review
   locations with positive decimal identities;
5. exact timestamp/latency agreement for every observed action;
6. null action facts for pending records;
7. unique resource, action, snapshot, review, census, and review-artifact
   identities;
8. exact issue-before-pull-request resource ordering within each window;
9. reviewed census completeness, eligibility, provenance, validation, external
   human authorship, action state, maintainer status, and participant
   distinctness; and
10. an executable mandatory prefix equal to the complete reviewed window
    history.

Candidate or history-incomplete manifests expose no record-derived aggregates.
Synthetic populated fixtures prove gate mechanics only; they are not people,
issues, pull requests, maintainer work, support, responsiveness, or adoption.

## Security and privacy boundary

The evaluator reads one explicitly selected bounded local JSON file. It rejects
symlinks, oversized or deeply nested documents, duplicate or unknown fields,
noncanonical types and timestamps, unsafe/non-project locations, incomplete
review, and excess windows or records. It performs no discovery, networking,
remote lookup, dynamic import, subprocess launch, telemetry, contributor
contact, issue/PR mutation, installation, or provider execution.

The frozen manifest may contain only canonical public project resource and
evidence locations, immutable hashes, bounded UTC timestamps and latency
seconds, action outcomes, and reviewed booleans. It must not contain usernames,
email addresses, private correspondence, credentials, local paths, prompts,
hostnames, IP addresses, unpublished user data, or private logs. Reports expose
only aggregate counts, latency statistics, policy/reason identifiers, and the
reviewed manifest digest.

M31 changes no runtime source, public API/export, canonical state, persistent
format, protocol, dependency, lock, package version, workflow, CI topology,
tag, release, publication, certification, stability label, or support policy.
See [RFC-0014](rfcs/0014-response-review-latency-admission-readiness.md).
