# RFC-0014: Response and review latency admission readiness

- **Status:** Accepted
- **Date:** 2026-08-08
- **Decision:** Define strict issue-response and PR-review latency admission and retain the current result as false
- **Related:** [readiness guide](../response-review-latency-readiness.md), [contributor rehearsal](0010-external-contributor-rehearsal-admission-readiness.md), [contributor retention](0012-external-contributor-retention-admission-readiness.md)

## Summary

Add deterministic source, isolated-wheel, and release-bundle evidence for the
design plan's next longer-term metric: issue-response and pull-request-review
time. The reviewed manifest contains no measurement windows, so the current
result remains false and no response-time, review-time, service-level, or
support claim is made.

M31 defines how a later real public cohort can be admitted. It does not query
GitHub, collect telemetry or private correspondence, contact contributors,
mutate issues or pull requests, or treat project-directed automation and
synthetic fixtures as human community-support evidence.

## Context

Pull-request CI records automation duration, and repository history records
project-owned development activity. Neither establishes how quickly human
maintainers first respond to external public issues or substantively review
external public pull requests. Measuring only completed fast actions would also
hide unanswered items and create selection bias.

External-human eligibility, maintainer identity, distinct participants,
first-qualifying-action status, census completeness, and public provenance are
social and operational facts. An offline evaluator can validate only a frozen
record after reviewers establish those facts from public evidence.

## Decision

The response/review-latency manifest:

1. uses bounded chronological non-overlapping opening windows and a later
   observation cutoff;
2. requires a complete reviewed census of eligible external-human public issues
   and pull requests, including pending items with no qualifying action;
3. requires observed issues to identify the first qualifying public response
   by a human maintainer and observed pull requests to identify the first
   qualifying substantive public review by a distinct human maintainer;
4. binds canonical project resource/action locations, exact UTC timestamps,
   integer latency seconds, action outcomes, source/review hashes, and reviewed
   provenance and validation;
5. requires public census and review artifacts at the same immutable project
   Git revision, with distinct SHA-256 identities;
6. rejects noncanonical order, duplicate identities, selection of only
   completed actions, timestamp/latency disagreement, unreviewed facts, unsafe
   locations, and incompatible types or outcomes;
7. reports eligible, observed, and pending counts plus deterministic median and
   nearest-rank p95 seconds separately for issues and pull requests;
8. requires at least one observed issue response and one observed pull-request
   review before the metric becomes reportable;
9. preserves every accepted window as a complete executable mandatory prefix
   equal to the reviewed manifest identity sequence; and
10. requires the exact whole-manifest digest to be pinned by reviewed code and
    strict installed evidence.

An admitted `ready` report means only that the metric is reportable from a
complete reviewed cohort. No latency threshold, SLA, quality verdict, release
gate, or support promise is defined. Pending counts remain visible beside
observed latency aggregates.

Before pinning a nonempty manifest, reviewers verify the public resources and
actions, complete eligible census, frozen source/review evidence, human and
maintainer status, participant distinctness, first-action facts, chronology,
provenance, validation, and mandatory history. The evaluator checks the frozen
record but cannot replace that review.

The current normative report is `not-ready`, with zero measurement windows and
reason code `response-review-latency-evidence-absent`. Synthetic future-state
regressions prove gate mechanics only.

## Security, privacy, and determinism

The evaluator reads one explicitly selected bounded local manifest. It rejects
unknown or duplicate JSON fields, symlinks, oversized documents, more than 16
structural object/array levels, excess windows or records, malformed values,
unsafe/non-project locations, reused resource/action/evidence identities,
incomplete review, and missing history.

The public manifest may contain canonical public project resource/evidence
locations, immutable hashes, bounded UTC timestamps and latency seconds,
outcomes, and reviewed booleans. It must not contain usernames, email
addresses, credentials, private communication or logs, local paths, prompts,
telemetry, hostnames, IP addresses, or unpublished user data. Reports omit
resource/action locations, timestamps, per-record hashes, identities, paths,
hosts, and raw evidence.

The harness performs no discovery, networking, remote lookup, dynamic import,
installation, subprocess launch, provider execution, telemetry, contributor
contact, issue/PR mutation, or retained-resource lifecycle.

## Consequences

- Issue-response and PR-review time have an exact artifact-exercised admission
  path but remain unmeasured.
- Pending items remain visible in future aggregates, preventing completed-only
  selection from satisfying the gate.
- A real complete reviewed public cohort is required before the metric can be
  reported.
- M31 changes no runtime source, public export, wire or persistent format,
  dependency, lock, package version, workflow, CI topology, tag, release,
  publication, certification, stability label, SLA, or support policy.

## Alternatives considered

- **Use GitHub Actions duration.** Rejected because automation time is not human
  maintainer response or review time.
- **Query GitHub during CI.** Rejected because mutable remote state and network
  availability would make evidence nondeterministic.
- **Measure only completed responses.** Rejected because it hides pending items
  and systematically biases results toward faster actions.
- **Store public usernames.** Rejected because the evaluator needs reviewed role
  facts, not personal identifiers.
- **Define an SLA from no data.** Rejected because M31 establishes measurement
  admission, not a fabricated performance target.
- **Mark the result true from synthetic tests.** Rejected because fixtures prove
  validation mechanics, not human responsiveness or support.
