# Agent-tool recovery-rate readiness

M34 defines how LudoWeave may report the percentage of product agent-tool
calls that complete without manual recovery. The evaluator is an explicitly
invoked offline evidence reader. It does not instrument the engine, collect
telemetry, discover sessions, contact users, or run during normal operation.

Run the current reviewed evidence:

```console
uv run python examples/agent_tool_recovery_rate_readiness.py
```

The committed manifest is exactly 195 bytes with SHA-256
`e952c045b039055e8439069cf88176b6ac1d2ad7de49a94d39b2737e5d06e1d5` and
contains no evaluation windows. The exact result is `not-ready` with reason
`agent-tool-recovery-rate-evidence-absent`, zero admitted calls, and no
measured recovery-free completion rate. Product examples, conformance runs,
tests, maintainer-invoked calls, synthetic fixtures, and passing CI are not an
operational cohort.

## Unit and cohort

The unit is one dispatched invocation of one of the exact 12 tools in
`ludoweave.agent.service/1` during a reviewed task-directed software-agent
session. A future admitted window must enumerate every eligible dispatched
call from the complete predeclared session census in its half-open interval.
Eligibility is fixed before outcomes are reviewed.

Synthetic fixtures, conformance profiles, benchmarks, CI contract exercises,
maintainer-driven CLI calls, passive documentation examples, and sessions
without reviewed public sanitized evidence are excluded. Human review owns
task-directed status, census completeness, eligibility, provenance, outcome,
validation, and whether any manual recovery occurred. The evaluator checks
only the frozen bounded record.

Every eligible call remains present as exactly one of:

- `completed-without-manual-recovery`, with a terminal result and no recovery
  evidence;
- `completed-after-manual-recovery`, with both terminal result and recovery
  evidence;
- `not-completed`, with a reviewed rejection, failure, or cancellation result,
  whether or not manual recovery was attempted; or
- `terminal-unobserved`, when a dispatched call lacks reviewable terminal
  evidence.

Known non-completions remain in the denominator. A `terminal-unobserved` call
remains counted but blocks rate publication so incomplete evidence cannot be
silently selected away.

## Manual recovery

Manual recovery occurs when a human intervenes after dispatch to make the same
intended operation proceed—for example by changing tool arguments,
configuration, environment, or authoritative state, or by directing a retry
or alternate call. Required approval before dispatch is not recovery. Passive
human observation is not recovery. A retry, repair, or alternate tool selected
autonomously without human intervention is not manual recovery, although each
dispatched invocation is still a separate denominator record.

The distinction is a reviewed operational fact, not something the evaluator
can infer from a receipt or error code. Public evidence must be sanitized and
must not disclose prompts, world content, credentials, usernames, private
communications, filesystem paths, or environment values.

## Exact rate semantics

Only an admitted non-empty cohort with no `terminal-unobserved` call exposes
`completion_without_manual_recovery_rate`. Its numerator is the count of
`completed-without-manual-recovery` calls and its denominator is every admitted
call, including calls completed after recovery and known non-completions. The
report emits the ratio as exact integers, never as a floating-point percent.

No success target, quality verdict, reliability guarantee, release gate,
service level, support promise, or provider certification is defined. A zero
numerator or zero manual-recovery count can be reported only from a non-empty
complete reviewed cohort.

## Admission and history

Admission requires the exact reviewed whole-manifest SHA-256; bounded
chronological non-overlapping windows; a later observation cutoff; complete
task-directed session census review; exact service protocol and 12-tool names;
immutable service-contract, call, result, and recovery evidence identities;
sequential per-session call indices; all required reviews; and a mandatory
prefix equal to the complete accepted history.

Both the window and every call require an explicit privacy-and-consent review.
That review must establish that public evidence publication is authorized and
that the frozen records contain no participant identity or sensitive content.

The sanitized report contains only aggregate counts, the exact rational rate
when admitted, policy/schema identities, and admission reasons. It never
returns session or adapter identifiers, tool names, timestamps, revisions,
artifact locations, local paths, prompts, arguments, results, errors, or raw
recovery records.

## CI quota boundary

The eight existing CI jobs remain the practical supported Python, desktop OS,
distribution, and graphics gate. M34 runs them only on substantive pull
requests. The redundant post-merge `main` run is removed, and pull requests
that change only `.project/**` factual records do not allocate runners. Runtime
and release changes still receive the complete gate.

## Boundary

M34 changes no runtime source, agent protocol/tool, command, receipt, public
API/export, persistent format, dependency, lockfile, package version, provider,
telemetry path, native/WASM boundary, release workflow, tag, publication,
certification, stability label, SLA, or support policy. The empty reviewed
manifest is readiness machinery, not a measured result.
