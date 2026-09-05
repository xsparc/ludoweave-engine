# RFC-0186: adopt Windows cleanup protocol and receipt policy

- **Status:** Accepted
- **Milestone:** M203
- **Date:** 2026-09-01

## Summary

Resolve M199 admission criterion 4 as policy with a separate versioned asset-
cache cleanup request, acknowledgement, and receipt family. Require one
bounded canonical JSON object per call, exact request/digest/operation
correlation, acknowledgement semantics that never imply success, path-free
typed outcomes, and explicit refusal of notification, batch, replay-authority,
authenticity, durability, and exactly-once claims.

Windows cleanup remains unimplemented and unauthorized. Durable intent and
recovery remain criterion 5. This RFC adds no runtime or hosted CI surface.

## Context

M199 consolidated seven Windows cleanup admission criteria. M200-M202 resolve
the singleton-link, authenticated-authority, and use-time revalidation
criteria as policy. A future caller still needs an unambiguous way to request
work, learn whether a bounded request was admitted, and receive typed evidence
without turning transport data into filesystem authority.

LudoWeave already has `ludoweave.command/1`, `ludoweave.transaction/1`, and
`ludoweave.receipt/1` for canonical ECS world mutations. Reusing those
documents for cleanup would be an architecture violation: cleanup is platform
mutation outside canonical world state, has distinct recovery phases, and
must never expose native/root/candidate information through a world receipt.

Current primary sources reinforce the existing direction. RFC 8259 permits
parser limits, and invariant canonical bytes support stable hashing. JSON-RPC
notifications are unconfirmable and batches may be unordered or concurrent.
RFC 7464 permits parsers to continue after malformed sequence elements and
provides no integrity protection. None of those generic mechanisms supplies
cleanup authority, durability, or receipt authenticity.

## Decision

Accept the [Windows cache-cleanup protocol and receipt
policy](../security/windows-cache-cleanup-protocol-receipt-policy.md).

### Separate protocol family

Reserve these policy identities without adding runtime constants or readers:

- `ludoweave.asset-cache-cleanup.request/1`;
- `ludoweave.asset-cache-cleanup.acknowledgement/1`; and
- `ludoweave.asset-cache-cleanup.receipt/1`.

They do not extend or reinterpret the world command/transaction/receipt v1
protocols. A future incompatible cleanup shape or meaning requires another
cleanup protocol identity.

### Bounded framing and request

Each future decoder accepts one exact, complete, canonical UTF-8 JSON object
with a declared length. Requests are limited to 16,384 bytes,
acknowledgements to 8,192 bytes, and receipts to 1,048,576 bytes. The policy
also fixes maximum depth, nodes, string bytes, outcomes, and diagnostics.
Duplicate/unknown/missing fields, trailing content, noncanonical values,
oversize input, batches, notifications, JSON sequences, and partial recovery
all refuse.

The request contains only protocol, request and operation IDs, bounded actor
attribution, fixed cleanup intent, and a dry-run Boolean. It cannot name a root,
path, candidate, policy override, generation, adapter, or native object. The
trusted composition root supplies private context and authority; caller data
can only request consideration.

### Acknowledgement and receipt

Exactly one acknowledgement binds the request/operation IDs and canonical
request SHA-256. Accepted means only that the bounded request/correlation tuple
was admitted; it does not mean mutation started or succeeded. Refused means no
mutation occurred. Both bind one receipt ID.

One typed receipt binds the request digest and canonical acknowledgement
digest. Its top-level status is refused, completed, or `recovery_required`.
Bounded deterministic item outcomes expose operation-local ordinals plus
versioned status/code, never candidate or path identity. Completed is forbidden
before durable terminal completion; any nonterminal post-mutation state is
recovery-required.

Criterion 5 still owns durable intent, phase transitions, replay lookup,
quarantine, persistence ordering, retry/restart behavior, restore, and
finalization. M203 fixes the evidence boundary without inventing that state
machine.

### Correlation, privacy, and non-authority

The same operation ID and request digest identify one logical operation and
must never repeat mutation. Reusing the ID with another digest is a conflict.
This is not an exactly-once guarantee: delivery loss leaves outcome unknown,
and safe lookup/retry cannot exist until criterion 5 is resolved.

Documents are canonical, bounded, path-free, and silent about content/file
identity, root/generation values, handles, tokens, SIDs, DACLs, environment,
and platform errors. Hashes provide deterministic correlation, not
authentication, signatures, non-repudiation, delivery proof, or durability.
Receipts are evidence and cannot authorize another effect.

### Criterion and authority boundary

M200-M203 resolve criteria 1 through 4 as policy only. Criteria 5 through 7
remain unresolved: durable mutation/recovery, hostile cross-principal evidence,
and independent-host/filesystem proof.

This is a direction-preserving refinement under ADR-0017, ADR-0019, ADR-0008,
ADR-0009, and RFC-0129 through RFC-0131. It is a no authority increase
decision. There is no production adapter, decoder, public protocol surface, or
receipt store. Preserve M202, runtime, fixtures, examples, scripts,
dependencies, lock, metadata, workflows, permissions, version, and package
surface exactly. Use no new hosted allocation.

## Consequences

Reviewers gain an exact distinction among request admission, acknowledgement,
and outcome evidence. Callers cannot use notification, batching, target lists,
paths, or saved documents to obtain cleanup authority. Acknowledgement delivery
cannot be overread as effect, and receipt correlation cannot be overread as
authenticity or durability.

The three protocol names are reserved by accepted policy but are not public API
until a later implementation milestone adds fully tested decoders and the
remaining criteria pass. Existing world receipts remain unchanged and focused
on canonical ECS mutation.

M203 adds one architecture guard and decision documentation. It adds no native
call, implementation, runtime API, protocol constant, command, decoder,
transport, public capability, receipt store, cache access, quarantine,
mutation, recovery path, integration fixture, dependency, compiler, version,
workflow, job, matrix, permission, credential, release authority, tag,
publication, or CI change. No new hosted allocation is added.

## Alternatives considered

- Reuse `ludoweave.receipt/1`. Rejected because its world hashes, ticks, command
  outcomes, and semantic diff are wrong for filesystem effects and would leak
  backend concerns into canonical world APIs.
- Use JSON-RPC notifications. Rejected because unconfirmable destructive calls
  cannot distinguish refusal, admission, outcome, or delivery failure.
- Permit batches. Rejected because ownership, ordering, correlation, and
  recovery must remain explicit per operation.
- Use newline or JSON-sequence framing. Rejected because cleanup requires one
  complete bounded document and fail-closed parsing, not skip-and-continue
  stream recovery.
- Let the request list candidates or paths. Rejected because candidate
  derivation and native authority belong exclusively to the engine.
- Treat receipt hashes as signatures. Rejected because ordinary SHA-256
  correlation provides no authentication or non-repudiation.
- Implement the decoder now. Rejected because criterion 5 durable admission is
  a prerequisite for accepted acknowledgement and safe retry behavior.
- Add another hosted job. Rejected because a policy-only change adds no runtime
  behavior for another allocation to validate.

## Validation

Architecture validation must:

- preserve exact M202 plus runtime, examples, scripts, integration fixtures,
  dependencies, lock, metadata, workflows, permissions, and package surface;
- require three distinct versioned cleanup protocol identities outside world
  command/transaction/receipt v1;
- require one complete bounded canonical UTF-8 object and reject sequence,
  notification, batch, partial, trailing, duplicate, and unknown input;
- require the exact path/candidate-free request and non-authority actor/dry-run
  semantics;
- require acknowledgement correlation and forbid interpreting acceptance as
  mutation or success;
- require typed receipt statuses and bounded operation-local outcomes without
  inventing criterion-5 transitions;
- bind retries by operation ID and canonical request digest while rejecting
  exactly-once and delivery claims;
- retain bounded path/security-material-silent diagnostics and explicit
  authenticity/non-repudiation non-claims;
- mark criterion 4 resolved as policy, retain criteria 1 through 3, and leave
  criteria 5 through 7 unresolved;
- retain Windows non-admission and the absence of cleanup/protocol
  implementation; and
- require public registration of RFC-0186 and the policy without CI expansion.

Run focused architecture tests, whole-tree static checks, strict docs, static
and current-date governance, supported-Python regression, reproducible package
and release rehearsals, findings-first review, and exact scratch cleanup before
local closeout. Claim no hosted result without an actual safely published run.

## References

- [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html)
- [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html)
- [RFC 7464](https://www.rfc-editor.org/rfc/rfc7464.html)
- [JSON-RPC 2.0](https://www.jsonrpc.org/specification)
- [NIST SP 800-92 Rev. 1 initial public draft](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd)
- [ADR-0008](../adr/0008-versioned-command-envelope-and-canonical-json.md)
- [ADR-0009](../adr/0009-authoritative-session-and-atomic-staging.md)
- [ADR-0017](../adr/0017-content-addressed-project-confined-assets.md)
- [ADR-0019](../adr/0019-agent-service-capabilities-and-safe-points.md)
- [RFC-0004](0004-bounded-receipt-reader-and-v1-baseline.md)
- [RFC-0006](0006-receipt-semantic-diff-and-diagnostic-compatibility.md)
- [RFC-0182](0182-refresh-windows-cache-cleanup-readiness.md)
- [RFC-0185](0185-adopt-windows-use-time-revalidation-policy.md)
