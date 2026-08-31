# Windows cache-cleanup durable recovery policy

- **Status:** Accepted decision
- **Milestone:** M204
- **Date:** 2026-09-01

## Decision and current boundary

Windows is not admitted for asset-cache cleanup. Cleanup remains unimplemented
and unauthorized. This decision resolves M199 criterion 5 as policy: a future
implementation must persist bounded intent before acknowledgement, quarantine
on the same filesystem before deletion, reconcile physical state after an
interruption, and stop safely when recovery evidence is ambiguous or altered.

M204 adds no journal implementation, filesystem adapter, protocol constant,
command, native call, or recovery authority. The request, acknowledgement, and
receipt documents fixed by M203 remain evidence only. They cannot mint
authority. Recovery records are also evidence only and cannot substitute for a
fresh M201 authority admission or the immediate M202 use-time gates.

## Private recovery store

A future adapter owns exactly one private recovery store for each admitted
trusted root. The private recovery store is root-confined beneath that trusted
root, is an ordinary non-reparse directory, and is on the same volume as the
candidate and quarantine directories. Its identity and security are admitted
through retained handles; a path string is not sufficient.

There is one active cleanup operation per trusted root and generation. A
second request refuses until the first operation reaches durable completion or
an operator resolves a recovery-required state. This serialization is local to
the private cleanup adapter and does not imply a process-global engine
singleton.

The store is not canonical world state. It is private platform recovery
evidence, never enters ECS components or world hashes, and cannot mint
authority. Its request and operation IDs are correlation values rather than
capabilities. Terminal history remains for the life of the generation. Journal
compaction, archive export, and garbage collection are outside M204 and must
not be inferred from terminal status.

## Bounded immutable record chain

The reserved internal record identity is
`ludoweave.windows-cleanup-recovery-record/1`. This is a policy identity, not a
public Python constant or supported decoder.

One operation admits a maximum 1,024 candidates, maximum 4,098 committed
records, maximum 65,536 bytes per record, and maximum 67,108,864 committed
bytes. Admission must prove that the complete worst-case record plan fits every
limit before acknowledgement. If corruption or unexpected state would exhaust
an admitted budget, recovery stops before the next effect. A sequence starts at
zero. Every later record contains `previous_record_sha256` for the exact
canonical bytes of its predecessor. Each record carries its own canonical
SHA-256 and the fixed root, generation, operation, request digest, phase,
candidate ordinal where applicable, and expected object identity.

The reader accepts one closed canonical record shape per sequence position. It
rejects unknown or missing fields, duplicate keys, noncanonical bytes, an
unsupported protocol, and any chain whose layout cannot prove: no gap,
duplicate, branch, rewrite, truncation, or replacement. Admission requires a
contiguous immutable chain and refuses upon any such defect. Sequence names,
record bytes, and hashes must agree. Canonical SHA-256 detects corruption and
correlation mismatch; canonical hashes are not authentication.

## Durable record publication

Every phase record uses the same fail-closed publication sequence:

1. exclusive create of one unique staging record in the retained store;
2. write the exact canonical bytes and reject a partial or mismatched write;
3. flush record contents and metadata through the retained record handle;
4. perform a no-replace same-directory publish to the reserved sequence slot;
5. settle the parent metadata using the platform procedure validated by the
   eventual implementation milestone;
6. reopen through the retained recovery-store handle; and
7. compare protocol, sequence, exact bytes, object identity, and canonical
   digest with the in-memory candidate record.

Only then is the phase durable. `ReplaceFile` is forbidden because it permits
replacement semantics and documents partial failure states. Transactional
NTFS is forbidden because Microsoft recommends alternatives to TxF. A rename
that can fall back to cross-volume copy and delete is forbidden. Unsupported
durability refuses before acknowledgement or mutation. M204 does not claim
that these ordered steps are already proven across supported Windows,
filesystems, storage devices, or power-loss conditions; criteria 6 and 7 retain
that proof obligation.

ReplaceFile is forbidden. Transactional NTFS is forbidden. Those names are
stated without implying that either mechanism enters the implementation.

An uncommitted staging record never advances the durable phase. On restart it
is admitted only as a known staging entry with the expected naming and
identity. An unexpected staging object is tamper or corruption evidence and
blocks the root rather than being silently removed.

## Write-ahead state machine

The private chain recognizes these ordered phase identities:

- `intent_durable` records the bounded candidate plan and correlation tuple;
- `quarantine_pending` records the exact next quarantine effect;
- `quarantined` records the verified post-rename object identity;
- `delete_pending` is the irreversible commit boundary for one candidate;
- `restore_pending` records an allowed pre-commit restoration;
- `deleted` records verified completion of the admitted deletion;
- `restored` records verified return of the candidate before commit; and
- `completed` records that every candidate has a durable terminal result.

The `quarantine_pending` record must be durable before quarantine. The
`delete_pending` record must be durable before deletion. The `restore_pending`
record must be durable before restoration. A `quarantined`, `deleted`, or
`restored` record is appended only after reopening and verifying the physical
postcondition. `completed` is durable only after every candidate is terminal.

In protocol terms, quarantine_pending must be durable before quarantine,
delete_pending must be durable before deletion, and restore_pending must be
durable before restoration. Completed is durable only after every candidate is
terminal.

The transition graph is bounded per candidate:

```text
intent_durable -> quarantine_pending -> quarantined
quarantined -> restore_pending -> restored
quarantined -> delete_pending  -> deleted
all candidates unchanged, restored, or deleted -> completed
```

`unchanged` is a deterministic terminal result for an admitted candidate that
the fresh gates refuse to mutate before any candidate-specific pending record.
It is included in the final `completed` record without inventing a filesystem
effect. No phase may be skipped, reordered, or inferred solely from a path
being absent.

## Acknowledgement, replay, and receipt binding

Accepted acknowledgement is forbidden before `intent_durable` and its durable
replay lookup have both passed the publication and reopen checks. The lookup
binds root identity, generation, `operation_id`, `request_sha256`, receipt ID,
record-chain head, and last durable phase. The same operation ID plus the same
request digest selects that operation; another digest is a conflict and does
not mutate.

The M203 public receipt phase is exactly one of `none, intent_durable,
quarantine_pending, quarantined, delete_pending, restore_pending, deleted,
restored, or completed`. An item outcome status is exactly one of `unchanged,
quarantined, deleted, restored, or recovery_required`. A completed receipt is
forbidden before `completed` is durable. A nonterminal state after an accepted
request produces recovery-required evidence bound to the last durable phase.

This is no exactly-once claim. The policy prevents deliberate repetition after
reconciliation, but process failure or response loss can leave delivery
unknown. Receipt delivery remains evidence rather than the commit point.

For exact protocol interpretation, accepted acknowledgement is forbidden
before intent_durable. The durable replay lookup exposes the last durable
phase. The public phase set is none, intent_durable, quarantine_pending,
quarantined, delete_pending, restore_pending, deleted, restored, or completed.
The item outcome set is unchanged, quarantined, deleted, restored, or
recovery_required. Completed receipt is forbidden before completed is durable.

## Same-filesystem quarantine

Quarantine operates on the same retained candidate handle admitted by the
M202 use-time checks and a retained quarantine-directory handle admitted under
the same trusted root. The adapter proves equal volume identity before intent
becomes durable. The intent fixes an engine-generated private slot for every
candidate. The target slot must not exist.

The rename is handle-relative, same-volume, and no replace. There is no
copy/delete fallback, and `MOVEFILE_COPY_ALLOWED` is forbidden. The adapter
must verify the same candidate identity after rename by reopening through the
retained quarantine-directory handle and comparing the admitted stable file
identity, type, link count, reparse state, and delete disposition. Failure is
`recovery_required`; it is not permission to retry a guessed pathname.

MOVEFILE_COPY_ALLOWED is forbidden.

Quarantine never changes canonical world state. It only moves an already
admitted cache candidate into a private location so the next irreversible
effect has a bounded recovery state.

## Restart reconciliation and idempotence

Restart first replays the complete bounded chain, verifies the private store,
and performs a fresh M201-style read admission for the trusted root and
generation. It must reconcile before applying an effect. A mutation or restore
then requires fresh private recovery authority and the immediate M202 gates;
the journal, request, acknowledgement, or receipt cannot supply it.

Recovery uses the same `operation_id` and `request_sha256`. It compares the
last durable record with handles to the exact original and quarantine slots and
must never repeat an already observed transition. For each candidate it
classifies exactly these physical observations:

- **original exact and quarantine absent:** no quarantine effect is visible;
- **original absent and quarantine exact:** the admitted object is quarantined;
- **both present:** conflict or hostile interference, never overwrite either;
- **both absent:** deletion may have occurred, but absence alone cannot prove
  which actor or phase caused it.

The word `exact` means the admitted stable identity plus required root,
generation, type, single-link, non-reparse, security, and delete-state checks,
not a pathname or matching content. Any observation inconsistent with the
last durable phase yields `recovery_required`. New cleanup requests refuse
while recovery is unresolved.

Recovery uses the same operation_id and request_sha256; the unformatted names
here describe exact protocol fields rather than caller authority.

Reconciliation may append only the unique next record justified by the last
durable phase and observed exact state. It never rewrites history, never
repeats a transition already proven by a durable successor, and never advances
from ambiguous absence.

## Restore and irreversible boundary

Restore is permitted only before `delete_pending`. The original slot must be
absent, the quarantine slot must be the same retained quarantined object, and
all current gates must pass. Restore never overwrites. A durable
`restore_pending` precedes the no-replace same-volume rename, and `restored`
follows exact verification at the original slot.

After `delete_pending`, automatic rollback is forbidden. Recovery may prove
and complete the already committed deletion, or it stops as
`recovery_required`; it must not guess rollback. In particular, it must not
recreate content from a digest, substitute a same-named object, move an
unverified quarantine occupant, or treat an absent pathname as successful
deletion.

Restore is permitted only before delete_pending. After delete_pending,
automatic rollback is forbidden.

## Tamper and corruption response

Any invalid record chain, unknown committed or staging entry, owner, DACL,
root, or generation mismatch, or identity, link, type, reparse, or delete-state
mismatch causes a fail-closed stop. The adapter must block cleanup for the
entire root and generation, preserve records and quarantined objects, and emit
bounded path-free recovery-required diagnostics.

There is no automatic journal repair, deletion, or restoration. An operator
must investigate outside the untrusted request path and establish a newly
approved recovery procedure. Hash-chain consistency does not prove principal
identity, trusted execution, or absence of a hostile writer.

## Crash and power-loss disposition

The future adversarial harness must exercise at least these interruption
boundaries:

| Interruption point | Required disposition |
| --- | --- |
| before `intent_durable` | No accepted acknowledgement and no mutation; an expected staging entry is inspected, never trusted as committed intent. |
| after `intent_durable` | Replay the operation and reconcile the original/quarantine observations before any effect. |
| after `quarantine_pending` | If the original remains exact, the authorized transition may be attempted once; otherwise reconcile without blind retry. |
| after quarantine but before `quarantined` | If the original is absent and quarantine exact, append `quarantined`; all other states stop or follow their uniquely justified transition. |
| after `delete_pending` but before `deleted` | If quarantine is exact, the committed deletion may proceed once; if both slots are absent, report `recovery_required`. The engine does not report completed from absence alone. |
| after `deleted` but before `completed` | Verify the durable deleted record and every terminal candidate, then append `completed`; never repeat deletion. |
| after terminal persistence but before response delivery | Return the durable correlated receipt on retry; delivery remains unknown to the original caller. |

The named fault windows are before intent_durable, after intent_durable, after
quarantine_pending, after quarantine but before quarantined, after
delete_pending but before deleted, and after deleted but before completed.
Across those windows the engine does not report completed from absence alone,
and response delivery remains unknown until the caller observes it.

Process-crash tests alone are insufficient. Criterion 7 must establish what
the selected filesystem and storage stack can prove after forced termination,
restart, cache flush, and power interruption on independent Windows hosts.

## Admission-criterion disposition

M199's seven criteria now have this exact state:

1. **Criteria 1 through 5 are resolved as policy.** M200 defines singleton-link
   refusal; M201 defines trusted authority and root/generation admission; M202
   defines immediate use-time revalidation; M203 defines bounded protocol
   evidence; M204 defines bounded durable intent, quarantine, and recovery.
2. **Criterion 5 is resolved as policy.** No implementation, native adapter,
   durability proof, or production admission follows from the decision.
3. **Criteria 6 and 7 remain unresolved.** Hostile cross-principal evidence and
   independent Windows/filesystem/power-loss proof remain absent.

Windows is not admitted, and cleanup remains unimplemented and unauthorized.
All seven criteria must pass together in a coherent implementation and its
adversarial validation before platform admission can be reconsidered.

## Scope and CI boundary

M204 changes this decision, one accepted RFC, public registrations, project
evidence, and one architecture guard only. It preserves M203, runtime code,
fixtures, examples, scripts, benchmarks, dependencies, lock, metadata,
version, workflows, permissions, and package surface. It adds no public or
private implementation, recovery store, file mutation, adapter, command,
transport, protocol reader, native call, compiler, credential, release effect,
job, matrix entry, or hosted allocation. Existing local validation is the
acceptance path; no hosted check is added.

## Primary references

- [Microsoft: Alternatives to using Transactional NTFS](https://learn.microsoft.com/en-us/windows/win32/fileio/deprecation-of-txf)
- [Microsoft: FILE_RENAME_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_rename_info)
- [Microsoft: MoveFileEx](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexa)
- [Microsoft: ReplaceFile](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew)
- [Microsoft: File caching](https://learn.microsoft.com/en-us/windows/win32/fileio/file-caching)
- [Microsoft: FlushFileBuffers](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-flushfilebuffers)
- [Microsoft: SetFileInformationByHandle](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfileinformationbyhandle)
- [ADR-0008](../adr/0008-versioned-command-envelope-and-canonical-json.md)
- [ADR-0009](../adr/0009-authoritative-session-and-atomic-staging.md)
- [ADR-0017](../adr/0017-content-addressed-project-confined-assets.md)
- [ADR-0019](../adr/0019-agent-service-capabilities-and-safe-points.md)
- [RFC-0182](../rfcs/0182-refresh-windows-cache-cleanup-readiness.md)
- [RFC-0186](../rfcs/0186-adopt-windows-cleanup-protocol-receipt-policy.md)
