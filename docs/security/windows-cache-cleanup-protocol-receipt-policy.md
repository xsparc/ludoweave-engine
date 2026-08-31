# Windows cache-cleanup protocol and receipt policy

- **Status:** Accepted decision
- **Milestone:** M203
- **Date:** 2026-09-01

## Decision and current boundary

Windows is not admitted for asset-cache cleanup. Cleanup remains unimplemented
and unauthorized. This decision resolves M199 criterion 4 as policy without
creating a command, decoder, transport, mutation service, recovery store, or
callable protocol surface.

A future implementation must use three distinct canonical JSON document
identities:

- `ludoweave.asset-cache-cleanup.request/1`;
- `ludoweave.asset-cache-cleanup.acknowledgement/1`; and
- `ludoweave.asset-cache-cleanup.receipt/1`.

The cleanup family is distinct from ludoweave.command/1, distinct from
ludoweave.transaction/1, and distinct from ludoweave.receipt/1. A world
transaction receipt cannot represent cleanup: filesystem cleanup is not an ECS
world transaction, must not change canonical world state, and cannot place
paths, native authority, filesystem identity, or recovery state in the world
protocol.

These documents are evidence and correlation records only. They cannot create,
serialize, transfer, widen, or reconstruct the private authority defined by
M201, and they cannot bypass the M200 or M202 gates.

## One bounded complete document

Each decoder receives one complete canonical JSON object as one exact UTF-8
byte slice with a declared byte length supplied by the owning adapter. The
length is checked before allocation or JSON parsing. The exact whole-document
bounds are:

- request: 16,384 bytes;
- acknowledgement: 8,192 bytes; and
- receipt: 1,048,576 bytes.

Every document also has maximum depth 32, maximum 100,000 nodes, maximum
262,144 UTF-8 string bytes, and exact field/count limits. A receipt has maximum
1,024 outcomes and maximum 64 diagnostics. Tighter field-local string and
collection limits must be fixed with the eventual decoder contract before
implementation.

The decoder rejects a byte order mark, trailing bytes, duplicate keys, missing
or unknown fields, invalid Unicode scalar text, non-canonical values,
non-finite numbers, invalid IDs, oversized input, and any limit violation. It
does not accept concatenated documents, a JSON text sequence, newline framing,
a batch, a notification, an indefinite stream, or a partial parse. Failure to
decode one document cannot skip ahead to another document or authorize work.

The protocol is transport-neutral. An in-process call, local stdio adapter, or
another future approved transport may carry the exact byte slice, but framing
and authentication belong to that separately admitted adapter. M203 creates no
listener, socket, remote endpoint, ambient discovery, or unauthenticated
control path.

## Request contract

The exact request fields are protocol, request_id, operation_id, actor, intent,
and dry_run.

- `protocol` is exactly `ludoweave.asset-cache-cleanup.request/1`.
- `request_id` identifies this submission and uses the existing bounded stable-
  ID grammar.
- `operation_id` is the caller-supplied stable correlation and retry identity.
- `actor` contains the existing bounded attribution kind and ID. Actor
  attribution is not authentication and never substitutes for the effective
  Windows token.
- Intent is exactly asset_cache_cleanup.
- `dry_run` is an exact Boolean. Dry_run cannot authorize mutation, and a false
  value is only a request for the trusted engine to consider private authority.

The request contains no path, root selector, candidate list, policy override,
generation value, retention timestamp, or native data. There is no candidate
identifier in a request. The trusted composition root selects the already
configured project, cache root, generation, policy, and private adapter. The
request cannot mint authority, select deletion targets, weaken limits, choose
an implementation, or turn read-only evidence into capability.

Unknown intent, reused request identity with conflicting bytes, malformed
actor attribution, missing context, unsupported platform, or unavailable
private authority refuses before mutation.

## Acknowledgement contract

The exact acknowledgement fields are protocol, request_id, operation_id,
request_sha256, status, receipt_id, and diagnostic.

- `protocol` is exactly
  `ludoweave.asset-cache-cleanup.acknowledgement/1`.
- The two IDs exactly match the decoded request.
- `request_sha256` is the SHA-256 over canonical request bytes with the
  `sha256:` algorithm prefix.
- `status` is exactly accepted or refused.
- `receipt_id` is the stable identifier to which the terminal or recovery-
  required receipt must bind.
- `diagnostic` is null for accepted status and one bounded code-only rejection
  value for refused status.

Every successfully decoded request produces exactly one acknowledgement before
any mutation is attempted. Accepted acknowledges only bounded admission of the
request and its correlation tuple. It does not mean mutation started, it does
not mean mutation succeeded, it does not mean a receipt is durable, and it does
not prove that the caller received anything. Refused guarantees no mutation
was attempted for that request and binds the refusal to its eventual typed
receipt. An acknowledgement is not a receipt and cannot be replayed as one.

Because criterion 5 is not yet resolved, a production implementation cannot
emit accepted until its durable intent and replay lookup are safely defined.
M203 fixes the semantic boundary; it does not make that prerequisite true.

## Receipt contract

The exact receipt fields are protocol, request_id, operation_id,
request_sha256, acknowledgement_sha256, receipt_id, status, phase, outcomes,
and diagnostics.

- `protocol` is exactly `ludoweave.asset-cache-cleanup.receipt/1`.
- IDs and the canonical request digest equal the request and acknowledgement.
- `acknowledgement_sha256` is the SHA-256 over canonical acknowledgement bytes
  with the `sha256:` prefix.
- `status` is exactly refused, completed, or recovery_required.
- `phase` is one versioned public phase identity defined by criterion 5; M203
  does not invent a durable transition graph.
- `outcomes` is a deterministic tuple of at most 1,024 typed item results.
- `diagnostics` is a deterministic tuple of at most 64 bounded diagnostics.

Each item result has exact fields candidate_ordinal, status, and code. The
candidate ordinal is a zero-based operation-local ordinal assigned from the
future deterministic candidate order. It is not a stable object identity and
cannot be used in another request. Status and code must come from a versioned
closed contract; a breaking meaning change requires a new receipt protocol.

Refused means no candidate mutation occurred. Completed is forbidden before
durable terminal completion of every admitted effect and its required record.
The required disposition is recovery_required after any completed mutation
phase without terminal completion. Criterion 5 defines the durable phase transitions,
quarantine, intent, persistence ordering, restore/finalize meanings, and
restart behavior. M203 does not guess them.

A receipt is evidence, not authority. It cannot authorize deletion, recovery,
restore, finalization, retry, or a new operation. Receipt construction cannot
change the world or filesystem, and receipt delivery cannot determine whether
an effect occurred.

## Correlation, retry, and delivery failure

The canonical request digest is SHA-256 over canonical request bytes. The
canonical acknowledgement digest is SHA-256 over canonical acknowledgement
bytes. A receipt must bind both digests plus all three IDs before it can be
associated with an operation.

A retry with the same operation_id and same request_sha256 refers to the same
logical operation and must not repeat mutation. The same operation_id with a
different request_sha256 is a conflict and refuses without mutation. A new
request_id cannot change that operation binding.

This is no exactly-once claim. Criterion 5 must define durable replay lookup,
record persistence, collision handling, retry responses, and recovery after a
crash. Until then, accepted acknowledgement is not implementable. A timeout,
closed stream, process loss, or delivery failure leaves the outcome unknown;
the caller must not infer refusal or success and must not create a new
operation identity to force progress.

Notifications and fire-and-forget calls are forbidden because the caller
could not distinguish refusal, acceptance, partial transition, or delivery
loss. Batch processing is forbidden because ordering, ownership, and
per-operation recovery must remain explicit.

## Privacy, diagnostics, and non-claims

All three public documents are bounded and path-free. Item outcomes expose
only their operation-local ordinal and versioned status/code. They contain no
path, filename, root, content identities, candidate digest, native handles,
token identifiers, SIDs, security descriptors, DACLs, generation nonces, file
identifiers, account/environment values, or platform error text.

Diagnostic codes are semantic within their versioned protocol. Messages are
metadata: callers must not parse prose for authority or success. Diagnostic
messages and scalar details remain bounded, redacted, non-authoritative, and
unable to carry raw security or filesystem material.

Canonical hashes detect correlation mismatch; they are not a MAC or digital
signature. M203 makes no authenticity, signature, or non-repudiation claim.
Actor fields are attribution only. A receipt does not prove principal identity,
trusted execution, receipt delivery, durable storage, cross-host equivalence,
or absence of hostile races.

## Admission-criterion disposition

M199's seven criteria now have this exact state:

1. **Criteria 1 through 4 are resolved as policy.** M201 defines authority,
   trusted-root, security, and generation admission; M200 defines singleton-
   link refusal; M202 defines immediate use-time revalidation; M203 defines
   bounded request, acknowledgement, and receipt evidence.
2. **Criterion 4 is resolved as policy.** Production decoders, stores,
   delivery, replay, and mutation wiring remain absent.
3. **Criteria 5 through 7 remain unresolved.** Durable intent/quarantine/
   recovery, hostile cross-principal evidence, and independent-host/filesystem
   proof are still absent.

Windows is not admitted, and cleanup remains unimplemented and unauthorized.
All seven criteria must pass together in one coherent implementation and
adversarial validation before reconsideration.

## Scope and CI boundary

M203 changes documentation, project evidence, and one architecture guard only.
It preserves M202, runtime code, integration fixtures, examples, scripts,
benchmarks, dependencies, lock, metadata, version, workflows, permissions, and
package surface. It adds no decoder, public type, protocol constant, operation,
command, CLI/MCP tool, transport, adapter, receipt store, recovery state,
generation file, cache access, quarantine, mutation, native call, native code,
compiler, credential, release effect, job, matrix entry, or hosted allocation.
Existing local validation remains the acceptance path; no new hosted check is
added.

## References

- [RFC 8259: JSON](https://www.rfc-editor.org/rfc/rfc8259.html)
- [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html)
- [RFC 7464: JSON Text Sequences](https://www.rfc-editor.org/rfc/rfc7464.html)
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
- [NIST SP 800-92 Rev. 1 initial public draft](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd)
- [ADR-0008](../adr/0008-versioned-command-envelope-and-canonical-json.md)
- [ADR-0009](../adr/0009-authoritative-session-and-atomic-staging.md)
- [RFC-0004](../rfcs/0004-bounded-receipt-reader-and-v1-baseline.md)
- [RFC-0006](../rfcs/0006-receipt-semantic-diff-and-diagnostic-compatibility.md)
- [RFC-0182](../rfcs/0182-refresh-windows-cache-cleanup-readiness.md)
- [RFC-0185](../rfcs/0185-adopt-windows-use-time-revalidation-policy.md)
