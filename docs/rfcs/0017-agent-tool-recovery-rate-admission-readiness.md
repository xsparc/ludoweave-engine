# RFC-0017: Agent-tool recovery-rate admission readiness

- **Status:** Accepted
- **Date:** 2026-08-08

## Context

The design plan lists the percentage of agent tool calls that complete without
manual recovery after benchmark-regression rate in its ordered longer-term
metrics. LudoWeave has 12 typed tools, an installed conformance profile, and
project-owned examples, but none of those establishes how task-directed calls
behave in a complete operational cohort. Selecting only successful calls or
silently dropping missing terminal evidence would bias the result.

M34 must define evidence admission without instrumenting the runtime,
collecting private telemetry, querying a provider, exposing session content, or
claiming that synthetic conformance is operational success.

The existing workflow also executes all eight supported-platform jobs after a
validated pull-request tree is squash-merged to unprotected `main`. That
second identical gate consumes runner quota without adding distinct evidence.

## Decision

Adopt the versioned
`ludoweave.operations.agent-tool-recovery-rate/1` reviewed manifest and the
explicitly invoked offline evaluator described in the
[readiness guide](../agent-tool-recovery-rate-readiness.md).

The manifest:

1. uses bounded chronological non-overlapping windows and a later observation
   cutoff;
2. requires a complete reviewed census of eligible task-directed sessions and
   every dispatched call rather than successful-call selection;
3. restricts calls to the exact 12 tools and
   `ludoweave.agent.service/1` contract;
4. excludes synthetic fixtures, conformance profiles, benchmarks, CI contract
   exercises, maintainer-invoked calls, and unreviewed/private sessions;
5. binds immutable service-contract, dispatch, terminal-result, and recovery
   evidence with sanitized session and adapter identities;
6. preserves calls as completed without recovery, completed after recovery,
   not completed, or terminal unobserved;
7. keeps known failures in the denominator and makes an unobserved terminal
   state block publication;
8. requires reviewed eligibility, task context, manual-recovery classification,
   outcome, privacy and consent, provenance, validation, and census
   completeness;
9. preserves sequential per-session call indices, canonical order, unique
   evidence, and complete mandatory history; and
10. exposes only an exact integer numerator/denominator ratio after admission.

Manual recovery means a human intervenes after dispatch by changing arguments,
configuration, environment, authoritative state, retry direction, or alternate
call selection for the same intended operation. Required approval before
dispatch, passive observation, and autonomous agent retry/repair are not manual
recovery. Human review establishes this fact; evaluator logic cannot.

Keep the existing eight-job CI topology because it covers baseline quality and
distribution, CPython 3.13/3.14 compatibility, and graphics on Windows, macOS,
and Linux. Trigger it only for substantive pull requests. Remove the duplicate
post-merge `main` trigger and ignore `.project/**`-only factual record PRs.

## Current result

The reviewed manifest contains no evaluation windows. Its deterministic report
is `not-ready`, contains zero calls, and exposes no recovery-free completion
rate. Existing examples, conformance passes, tests, CI runs, and populated
synthetic fixtures do not establish the longer-term metric.

## Consequences

- Future evidence can report an exact, auditable aggregate without emitting
  per-session data.
- Failures, cancellations, calls completed after human recovery, and missing
  terminal evidence cannot disappear from the cohort.
- Public evidence must be consented, sanitized, immutable, and free of prompts,
  world data, credentials, usernames, private correspondence, paths, and
  environment details.
- No success target, quality verdict, release gate, reliability guarantee,
  provider certification, SLA, or support promise is introduced.
- Each substantive milestone uses one hosted eight-job PR gate instead of a
  duplicate PR-plus-main gate; factual `.project/**` records consume no runner.
- No engine or agent source, protocol, tool, public export, format, dependency,
  lock, version, provider, telemetry path, release workflow, tag, publication,
  native/WASM implementation, or stability label changes.

## Alternatives considered

Treating the M18 conformance pass as a recovery-free call rate was rejected
because a deterministic fixture is not an operational agent cohort. Counting
only completed calls was rejected because it hides failures. Treating missing
terminal evidence as a known failure was rejected because the outcome and
recovery state are unverified; it instead blocks publication. Automatic
runtime telemetry was rejected because it widens privacy, retention, and
operational boundaries. Removing platform jobs was rejected because those
jobs cover distinct supported compatibility surfaces; removing the duplicate
post-merge trigger retains the same substantive PR evidence at lower cost.
