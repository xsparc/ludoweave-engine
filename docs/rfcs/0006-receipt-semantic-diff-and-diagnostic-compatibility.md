# RFC-0006: Receipt semantic-diff and diagnostic compatibility

- **Status:** Accepted
- **Date:** 2026-08-06
- **Decision:** Freeze receipt-v1 semantic-diff meanings and diagnostic-code evolution
- **Related:** [compatibility guide](../receipt-semantic-compatibility.md), [command guide](../commands.md), [RFC-0003](0003-retain-experimental-command-receipt-contracts.md), [RFC-0004](0004-bounded-receipt-reader-and-v1-baseline.md), [RFC-0005](0005-built-in-operation-argument-compatibility.md), [ADR-0008](../adr/0008-versioned-command-envelope-and-canonical-json.md)

## Summary

The semantic-diff field sets, status relationships, ordering rules, and named
meanings inside `ludoweave.receipt/1` are exact persistent contracts. A
breaking change requires a new receipt protocol. Existing diagnostic-code
meanings are fixed, while a new well-formed code is additive and must preserve
the receipt's rejected-status authority.

M23 records this policy independently of implementation, freezes a
machine-readable contract, and proves installed behavior with deterministic
source, wheel, and release-bundle evidence. This satisfies gate 5 of RFC-0003
but does not promote command, transaction, or receipt stability.

## Context

M21 added a strict bounded reader, and M22 fixed operation-argument evolution.
The receipt reader already rejects unknown semantic-diff fields and accepts
well-formed diagnostic codes, but tests alone did not state which meanings are
compatibility promises and which diagnostic values may evolve.

Machine consumers need a stable decision identity without being forced to
parse prose. At the same time, freezing messages and detail keys would prevent
safe redaction and useful diagnostic refinement. The policy therefore separates
the code identity from non-authoritative diagnostic metadata.

## Decision

For `ludoweave.receipt/1`:

1. semantic-diff root and nested field sets are exact;
2. committed/dry-run/rejected presence rules are fixed;
3. ordering and named semantic rules in the normative fixture are fixed;
4. unknown receipt or semantic-diff fields are rejected;
5. a breaking shape or meaning change requires a new receipt protocol;
6. an existing diagnostic code cannot be removed, reused, or reinterpreted;
7. a new well-formed diagnostic code is additive and consumers preserve the
   rejected receipt status when the code is unknown;
8. diagnostic phase, message, and scalar detail keys are non-authoritative
   metadata and may evolve without changing the code's meaning; and
9. once the surface is preview, removal follows the supported feature-release
   deprecation rule then in force.

The repository fixture is normative compatibility evidence. Runtime code does
not load it. It binds each current diagnostic identity to a frozen meaning and
an installed rejection scenario. The installed example exercises every
semantic change family against one exact full-diff value and ordering oracle,
all six current top-level transaction rejection code/meaning pairs, exact
missing/unknown field rejection, incompatible protocol rejection, and additive
unknown-code reading.

RFC-0003's readiness report advances to schema `/4`. Gates 3, 4, and 5 are
true. Gate 1 remains the sole cross-version proof requirement; satisfying the
policy gate does not fabricate history. Cross-version fixtures, external
consumer feedback, and a supported feature-release channel remain false, so
preview promotion remains deferred.

## Security and determinism

Rejected status remains authoritative even when a code is unknown. Message,
phase, and detail values never become commands, evaluator input, or canonical
state. Exact semantic fields prevent silent downgrade or typo acceptance.

Evidence uses fresh deterministic in-memory authorities and installed public
APIs. It performs no discovery, dynamic import, filesystem read, subprocess,
network operation, provider selection, or global registration. Reports exclude
state values, hashes, paths, environment/platform facts, timings, credentials,
and diagnostic messages.

## Consequences

- Consumers can make machine decisions from receipt status and diagnostic code
  without parsing prose.
- New codes can describe finer rejection classes without making old readers
  treat failures as success.
- In-place semantic-diff reinterpretation is forbidden even while Python
  exports remain experimental.
- M23 changes no runtime source, public export, wire field, operation,
  dependency, lock, version, or CI topology.
- Same-version evidence is not cross-version history or external adoption.

## Alternatives considered

- **Freeze messages and detail keys.** Rejected because prose, redaction, and
  diagnostic context need safe non-semantic evolution.
- **Treat every new code as breaking.** Rejected because the bounded reader
  already preserves unknown well-formed codes and receipt status supplies a
  safe fallback.
- **Allow optional new semantic-diff fields in v1.** Rejected because an older
  consumer could silently ignore meaning that changes authority interpretation.
- **Mark gate 1 complete with project-owned fixtures.** Rejected because every
  fixture still comes from one package version.
- **Promote the contracts now.** Rejected because cross-version history,
  external feedback, and a supported deprecation channel remain absent.
