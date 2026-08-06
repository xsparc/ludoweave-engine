# Command and receipt stability decision

M20 evaluates whether the installed command, transaction, and receipt contracts
are ready to move from `experimental` to `preview`. It does not redesign those
contracts or silently create a compatibility promise.

## Decision

Retain the current command/receipt Python exports and wire protocols as
`experimental` under [RFC-0003](rfcs/0003-retain-experimental-command-receipt-contracts.md).
The same-version implementation has strong behavioral foundations, but the
project cannot yet honor the preview promise that an incompatible removal is
preceded by at least one supported feature release.

This decision does not weaken the existing versioned-wire rule. Readers must
still reject an incompatible protocol identifier instead of reinterpreting
`ludoweave.command/1`, `ludoweave.transaction/1`, or
`ludoweave.receipt/1` in place.

M21 subsequently adds the bounded reader identified by this gate under
[RFC-0004](rfcs/0004-bounded-receipt-reader-and-v1-baseline.md). That completes
one prerequisite without changing the overall decision: five promotion gates
and actual cross-version evidence remain absent.

## Installed evidence

Run the dependency-free evidence composition from source or the version-matched
sample bundle:

```console
python command_receipt_stability_decision.py
```

It prints one deterministic
`ludoweave.evaluation.command-receipt-stability/2` JSON document. Schema `/2`
records the M21 reader capability; `/1` is not silently reinterpreted. The
evidence uses only installed public APIs and confirms:

- exact command, transaction, receipt, and agent-conformance protocol IDs;
- immutable canonical command/transaction decoding and round trips;
- dry-run non-mutation plus a proposed post-state hash;
- committed pre/post hash continuity and semantic creation evidence;
- atomic stale-hash, unsupported-hash-algorithm, and failed-middle-operation
  rejection with engine-owned diagnostic codes;
- all twelve checks of the installed agent-tool baseline against a fresh
  explicit built-in composition; and
- the exact current `experimental` stability labels and seven built-in
  operation identities.

The report deliberately contains no state hashes, entity/component values,
captures, provider diagnostics, paths, environment/platform values, timing, or
credentials. A strict repository validator rejects any missing field, changed
value, or JSON type drift.

## Preview promotion gate

All of these must be evidenced together before reconsideration:

1. A cross-version fixture corpus proves old accepted command/receipt documents
   remain readable or fail under a documented compatibility rule.
2. At least one external consumer supplies feedback from a real command/receipt
   integration; project-owned samples are not adoption evidence.
3. Built-in operation argument schemas have an explicit compatibility and
   deprecation policy independent of their current implementation.
4. A bounded public receipt reader validates untrusted receipt documents.
   **Satisfied by M21/RFC-0004.**
5. Semantic-diff fields and diagnostic-code compatibility are documented and
   covered by cross-version fixtures.
6. A supported feature-release channel exists so the preview deprecation
   promise can actually be fulfilled.

The `/2` evidence marks only gate 4 true. The existing versioned schemas,
canonical codec, transaction atomicity, transport-independent tool profile,
and frozen single-version fixtures are necessary foundations, not substitutes
for compatibility history or the other five gates.

## Ownership and failure behavior

The example constructs one in-memory `WorldSession` and executes synchronous
transactions on the calling thread. It creates no files, process, thread,
listener, network connection, dynamic import, provider registry, or ambient
discovery. The separate agent-profile composition is explicitly selected,
owned, and closed by the existing M18 runner.

Rejections are normal receipt outcomes. They preserve the live authority hash,
discard staged aliases and semantic changes, and expose only existing
engine-owned error codes. Control-flow, filesystem, provider, transport, and
release behavior are outside this evidence.

## Explicit non-scope

M20 adds no public runtime symbol, reader, operation, command field, receipt
field, migration, persistent format, root export, plugin field, transport,
listener, storage backend, dependency, lock change, package version, CI job,
tag, release, or publication. It does not promote any API and does not claim
external adoption, certification, cross-version compatibility, or maintenance
readiness.
