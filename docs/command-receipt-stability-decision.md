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

M21 adds the bounded reader under
[RFC-0004](rfcs/0004-bounded-receipt-reader-and-v1-baseline.md), and M22 adds
the exact built-in operation/version evolution policy under
[RFC-0005](rfcs/0005-built-in-operation-argument-compatibility.md). M23 adds
the receipt semantic-diff and diagnostic-code evolution policy under
[RFC-0006](rfcs/0006-receipt-semantic-diff-and-diagnostic-compatibility.md).
Those complete three prerequisites without changing the overall decision:
cross-version history, external feedback, and a supported release channel
remain absent.
M24/RFC-0007 adds strict admission machinery for the first missing gate, but
the current `0.1.0a1` reader/fixture identity and empty supported-release set
keep that gate false.
M25/RFC-0008 adds strict external-feedback admission, but its reviewed corpus
is empty. M26/RFC-0009 adds strict supported-release-channel admission, but its
reviewed release set is empty. Both gates remain false.

## Installed evidence

Run the dependency-free evidence composition from source or the version-matched
sample bundle:

```console
python command_receipt_stability_decision.py
```

It prints one deterministic
`ludoweave.evaluation.command-receipt-stability/4` JSON document. Schema `/4`
records the M21 reader, M22 operation-policy, and M23 receipt-policy gates; earlier report schemas
are not silently reinterpreted. The
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
   **Admission is defined by M24/RFC-0007; evidence remains absent.**
2. At least one external consumer supplies feedback from a real command/receipt
   integration; project-owned samples are not adoption evidence.
   **Admission is defined by M25/RFC-0008; the reviewed corpus is empty.**
3. Built-in operation argument schemas have an explicit compatibility and
   deprecation policy independent of their current implementation.
   **Satisfied by M22/RFC-0005.**
4. A bounded public receipt reader validates untrusted receipt documents.
   **Satisfied by M21/RFC-0004.**
5. Semantic-diff fields and diagnostic-code compatibility have an explicit
   versioned evolution policy. **Satisfied by M23/RFC-0006.** Cross-version
   execution evidence remains independently required by gate 1.
6. A supported feature-release channel exists so the preview deprecation
   promise can actually be fulfilled.
   **Admission is defined by M26/RFC-0009; the reviewed release set is empty.**

The `/4` evidence marks gates 3, 4, and 5 true. The existing versioned schemas,
canonical codec, transaction atomicity, transport-independent tool profile,
and frozen single-version fixtures are necessary foundations, not substitutes
for compatibility history or the other three gates.

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

M20-M23 add no operation, command field, receipt field, migration, persistent
format, root export, plugin field, transport,
listener, storage backend, dependency, lock change, package version, CI job,
tag, release, or publication. It does not promote any API and does not claim
external adoption, certification, cross-version compatibility, or maintenance
readiness.
