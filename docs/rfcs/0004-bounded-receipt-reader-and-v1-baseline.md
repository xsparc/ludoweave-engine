# RFC-0004: Bounded receipt reader and v1 fixture baseline

- **Status:** Accepted
- **Date:** 2026-08-06
- **Decision:** Add a strict experimental reader and freeze a single-version v1 baseline
- **Related:** [RFC-0003](0003-retain-experimental-command-receipt-contracts.md), [receipt-reader guide](../receipt-reader.md), [command guide](../commands.md), [API status](../api-status.md)

## Summary

Add `TransactionReceipt.from_mapping`, `TransactionReceipt.from_json`, frozen
`ReceiptLimits`, and structured receipt decode errors without changing
`ludoweave.receipt/1`. Freeze exact committed, dry-run, and rejected fixtures
from `0.1.0a1` as the baseline for a future cross-version corpus.

The public-reader-and-bounds gate in RFC-0003 becomes true. The cross-version
gate remains false because only one package version has read the fixtures. All
receipt and command exports remain experimental.

## Context

Before M21, receipts could be serialized canonically but not reconstructed from
untrusted JSON through a public bounded API. Consumers would have needed to
inspect dictionaries ad hoc, weaken validation, or depend on private engine
details. M20 therefore retained experimental status and named a bounded receipt
reader as one of six mandatory preview gates.

A reader is also required before compatibility can be measured honestly. A
future version cannot prove it still understands historical receipts unless
the project preserves exact historical documents and an explicit decode path.
Creating current-version fixtures alone is not cross-version evidence, so the
manifest must state that limitation machine-readably.

## Decision

`TransactionReceipt.from_json` first applies configurable canonical JSON byte,
depth, node, collection, and string limits. `from_mapping` applies the same
recursive JSON-domain validation and detaches caller containers. Both then
enforce exact v1 object fields, nested semantic limits, typed identities, and
status/hash/tick/change invariants.

Add these experimental `ludoweave.world` exports:

- `ReceiptLimits`;
- `ReceiptDecodeError`; and
- `IncompatibleReceiptError`.

The reader accepts only `ludoweave.receipt/1`; an incompatible identifier is a
typed compatibility failure and is never interpreted in place. It creates
immutable detached evidence and has no authority, world-mutation, provider,
filesystem, process, or network capability.

Freeze three receipt files plus an exact manifest under
`tests/fixtures/receipt_v1`. The manifest schema is repository compatibility
evidence rather than a new installed runtime protocol. It records source
version `0.1.0a1`, exact byte sizes and hashes, and evidence level
`single-version-baseline`. Tests verify the current reader reproduces each
canonical document exactly.

Version the living M20 readiness report from
`ludoweave.evaluation.command-receipt-stability/1` to `/2`. The report now marks
only `public_receipt_reader_and_bounds` true. It retains the overall
`retain-experimental-command-receipt` decision because five gates remain false.

## Compatibility policy

- The v1 field meanings are not reinterpreted by this reader.
- Missing or unknown fields fail closed.
- A future incompatible receipt shape requires another receipt protocol.
- Frozen fixture bytes and hashes are historical evidence and must not be
  rewritten to make a future implementation pass.
- A later version may add expected-result metadata beside the fixtures, but
  must preserve the original documents and source-version attribution.
- Cross-version compatibility is claimed only after a different supported
  package version reads this baseline in CI and the policy for any accepted
  evolution is documented.

RFC-0007 later makes that admission rule executable while retaining its result
as false for the current single-version/no-release-evidence corpus.

This policy establishes a baseline and preservation rule. It does not define
compatibility for every diagnostic code, detail key, or semantic-diff field.
That separate gate was false at M21 and is later satisfied by RFC-0006 without
changing this reader or claiming cross-version history.

## Security and determinism

Canonical JSON limits run before domain construction. Nested arrays and
diagnostic detail maps have additional deterministic caps. Unknown objects,
container inspection failures, duplicate keys/identities, invalid numeric
domains, malformed hashes/UUIDs/entities, and inconsistent status relationships
produce bounded structured errors.

The decoder retains no caller container, opens no file, discovers no code,
loads no provider, and invokes no operation handler. Given the same valid input
and limits, it returns canonically equivalent immutable values. This is parsing
determinism, not receipt authenticity, provenance, or cross-build simulation
evidence.

## Consequences

- Consumers can safely reconstruct current receipt evidence through a public
  engine-owned boundary.
- Future releases have immutable v1 inputs against which to test compatibility.
- M20's readiness schema advances to `/2` rather than silently changing `/1`.
- The project takes on maintenance responsibility for a strict experimental
  reader and its fixture-preservation rules.
- No command, operation, receipt field, protocol, stability label, dependency,
  lock, package version, CI job, tag, release, or publication changes.

## Alternatives considered

- **Leave consumers to parse dictionaries.** Rejected because it duplicates
  security limits and receipt invariants outside the engine.
- **Use command-schema errors.** Rejected because receipt failures need a
  stable subsystem-specific type and code without pretending a receipt is a
  command.
- **Mark the cross-version gate complete immediately.** Rejected because every
  fixture and reader execution still uses `0.1.0a1`.
- **Promote receipts to preview with the reader.** Rejected because external
  feedback, operation/diff/diagnostic policies, real cross-version evidence,
  and a supported deprecation release channel remain absent.
