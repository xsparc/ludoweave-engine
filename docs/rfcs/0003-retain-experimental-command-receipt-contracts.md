# RFC-0003: Retain experimental command and receipt contracts

- **Status:** Accepted
- **Date:** 2026-08-06
- **Decision:** Retain experimental status pending complete compatibility evidence
- **Related:** [command guide](../commands.md), [API status](../api-status.md), [ADR-0008](../adr/0008-versioned-command-envelope-and-canonical-json.md), [ADR-0019](../adr/0019-agent-service-capabilities-and-safe-points.md)

## Summary

The `ludoweave.command/1`, `ludoweave.transaction/1`, and
`ludoweave.receipt/1` contracts remain experimental. M20 confirms their strong
same-version behavioral foundation through deterministic installed evidence,
but it does not promote their Python exports or wire compatibility status.

Promotion to preview is reconsidered only when the project has a cross-version
fixture corpus, external consumer feedback, operation-argument compatibility
rules, a bounded public receipt reader, semantic-diff/diagnostic compatibility
rules, and a supported feature-release channel.

## Context

The alpha retrospective identifies public API candidates as a priority question.
Commands and receipts are the engine's central human/agent mutation boundary,
and M18 proves their use through the complete transport-independent agent tool
surface. That maturity makes them the right first stability candidate to audit.

Preview is nevertheless a compatibility promise, not a quality adjective.
Under `API_COMPATIBILITY.md`, an incompatible preview removal requires a
documented deprecation in at least one feature release. The project has no
published feature-release channel, no independently authored command consumer,
and no cross-version compatibility corpus. Current operation arguments and
receipt semantic-diff/diagnostic fields are tested exactly within one version
but do not yet have separately stated evolution rules. `TransactionReceipt`
also serializes canonical bytes without a public bounded decoder for untrusted
receipt documents.

## Decision

Retain these public `ludoweave.world` exports as `experimental`:

- `COMMAND_PROTOCOL`, `TRANSACTION_PROTOCOL`, and `RECEIPT_PROTOCOL`;
- `CommandActor`, `CommandEnvelope`, and `CommandTransaction`;
- `CommandOutcome`, `ReceiptDiagnostic`, `ReceiptStatus`, and
  `TransactionReceipt`; and
- `TransactionService`.

No v1 protocol is reinterpreted. An incompatible future wire shape requires a
new protocol identifier and decision. Retaining experimental Python status
means an alpha release may still change or remove exports without a deprecation
period, but any user-visible change remains documented and versioned honestly.

M20 adds a strict installed evidence composition. It validates canonical
round-trip behavior; dry-run, commit, stale-hash, unsupported-algorithm, and
failed-batch atomicity; receipt status/code/hash relationships; exact built-in
operations; current stability metadata; and the existing twelve-check agent
profile. Its output is fixed, versioned, sanitized, and exercised from source,
an isolated wheel, and the release sample bundle.

The complete preview promotion gate is:

1. cross-version compatibility fixtures;
2. external consumer feedback;
3. operation-argument compatibility policy;
4. bounded public receipt reader and limits;
5. semantic-diff and diagnostic-code compatibility policy; and
6. a supported deprecation-capable feature-release channel.

All six are required. Project-owned tests, source examples, or hosted passes do
not fabricate external adoption or release history.

## Security and determinism

The evidence runs trusted project code in-process and synchronously. It performs
no discovery, dynamic import, installation, filesystem access, subprocess,
networking, or global registration. It returns booleans, protocol/status/code
identities, field names, operation names, and the installed package version—no
world hashes, values, paths, environment/platform facts, timings, captures, or
provider messages.

Same-version D1 canonical bytes and atomic authority behavior are confirmed.
No cross-version, cross-build, arbitrary-float, transport-security, or external
provider guarantee is inferred.

## Consequences

- Users receive an explicit, evidence-backed reason the central protocols are
  not yet preview rather than an implicit perpetual-alpha status.
- Future promotion has a finite, machine-auditable gate.
- The project avoids promising deprecation behavior it currently cannot deliver.
- No runtime API, wire format, operation, dependency, version, or CI topology
  changes in M20.
- A later RFC may promote a bounded subset once every gate is evidenced; it
  must update stability metadata, compatibility docs, fixtures, and changelog
  in one reviewed change.

## Alternatives considered

- **Promote immediately because M18 passes.** Rejected because same-version
  behavioral conformance does not prove cross-version compatibility or a
  usable deprecation channel.
- **Add a receipt reader during the decision.** Rejected because that would
  combine a compatibility decision with a new untrusted-input API and format
  policy instead of evaluating the current boundary.
- **Mark only Python classes preview while leaving the wire format
  experimental.** Rejected because their purpose and canonical methods are
  inseparable from the versioned documents users would persist or transport.
- **Declare the contracts stable.** Rejected because there is no release or
  adoption evidence supporting a SemVer commitment.
