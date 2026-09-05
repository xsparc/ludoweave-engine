# RFC-0187: adopt Windows cleanup durable recovery policy

- **Status:** Accepted
- **Milestone:** M204
- **Date:** 2026-09-01

## Summary

Resolve M199 admission criterion 5 as policy. Require a private root-confined
recovery store, bounded immutable write-ahead records, same-filesystem
no-replace quarantine, restart reconciliation, a pre-deletion restore boundary,
and fail-closed rollback-tamper handling.

Windows cleanup remains unimplemented and unauthorized. Criteria 6 and 7 still
require hostile cross-principal evidence and independent host, filesystem,
crash, and power-loss proof. This RFC adds no runtime or hosted CI surface.

## Context

M200-M203 define singleton-link refusal, private authority admission, immediate
use-time revalidation, and bounded request/acknowledgement/receipt evidence.
M203 deliberately withholds accepted acknowledgement until criterion 5 fixes
durable intent and replay lookup. It also leaves quarantine, persistence
ordering, retry, restart, restoration, and finalization undefined.

A destructive filesystem operation cannot safely infer progress from pathname
absence or retry a transition after process loss. The policy must distinguish
an effect that has not started, one committed by write-ahead intent, an effect
visible but not yet recorded, a durable terminal effect, and evidence that is
ambiguous or altered. None of those states belongs in canonical ECS world
state, and none of their records may create Windows authority.

Current Microsoft documentation reinforces the existing conservative
direction. Transactional NTFS is deprecated for development in favor of
alternatives. `ReplaceFile` has replacement and partial-failure semantics, and
its write-through flag is unsupported. `MoveFileEx` can use copy/delete across
volumes. Windows metadata and writes are cached, while flush and rename
behavior still require proof on the exact supported platform/storage matrix.

## Decision

Accept the [Windows cache-cleanup durable recovery
policy](../security/windows-cache-cleanup-durable-recovery-policy.md).

### Private bounded recovery evidence

One private recovery store resides beneath each trusted root as a retained,
same-volume, ordinary non-reparse directory. At most one operation is active
per root and generation. The store and its records are non-authoritative
platform evidence, not world state or transferable capability.

Reserve the internal policy identity
`ludoweave.windows-cleanup-recovery-record/1`. One operation is bounded to
1,024 candidates, 4,098 committed records, 65,536 bytes per record, and
67,108,864 committed bytes. Records form a zero-based immutable canonical
SHA-256 chain. Any gap, duplicate, branch, replacement, rewrite, truncation,
unexpected staging object, or identity/security mismatch stops recovery.

### Durability and phase ordering

Every record is exclusively staged, written exactly, flushed, published
without replacement in the same directory, followed by parent-metadata
settlement, then reopened and verified through the retained store handle. A
phase is durable only after this sequence succeeds. TxF, `ReplaceFile`, and
copy/delete fallback are excluded.

The state machine is write-ahead: `intent_durable`, `quarantine_pending`,
`quarantined`, `delete_pending`, `restore_pending`, `deleted`, `restored`, then
operation `completed` after all candidates are terminal. The applicable
pending record precedes each effect. Accepted acknowledgement follows durable
intent and lookup; a completed receipt follows durable completion.

### Quarantine, reconciliation, and restore

The admitted candidate handle is moved to its intent-fixed private slot
through a retained quarantine-directory handle. Root and volume identity must
match, the target must be absent, replacement is forbidden, and the same object
identity is verified after rename.

After interruption, recovery replays the bounded chain, performs fresh root
and generation read admission, and reacquires private recovery authority for
any effect. It compares the last durable phase with the exact original and
quarantine objects. It appends only a uniquely justified next record and does
not repeat an already observed effect. Both-present, ambiguous both-absent, or
mismatched observations require operator-visible recovery rather than guessing.

Restore is allowed only before durable `delete_pending`, only when the original
slot is absent and the same quarantined object is verified. It never
overwrites. After the deletion commit boundary, automatic rollback is
forbidden; recovery either proves and completes the committed transition or
stops.

### Tamper and interruption behavior

An invalid chain, unknown store entry, security mismatch, root/generation
mismatch, or object mismatch blocks the whole root and generation. Records and
quarantined objects are preserved. There is no automatic repair, deletion, or
restore, and ordinary hashes are not authentication.

The policy fixes minimum crash windows before/after intent, pending records,
visible rename, delete commitment, terminal deletion, completion, and response
delivery. Absence alone never proves completed deletion. Independent hostile
and power-loss validation remains an admission prerequisite rather than a
documentation claim.

### Criterion and authority boundary

M200-M204 resolve criteria 1 through 5 as policy only. Criteria 6 and 7 remain
unresolved. This is a direction-preserving refinement under ADR-0017,
ADR-0019, ADR-0008, ADR-0009, and RFC-0182. It is a no authority increase
decision. There is no production adapter, recovery implementation, or public
protocol surface. Preserve M203, runtime, fixtures, examples, scripts,
dependencies, lock, metadata, workflows, permissions, version, and package
surface exactly. Use no new hosted allocation.

## Consequences

The future implementation has an explicit commit protocol and can no longer
equate retry with replay, absence with success, or a receipt with filesystem
authority. Same-volume quarantine limits the irreversible interval. Durable
phase records make post-crash reconciliation explicit, while conservative
tamper handling prevents automatic actions from compounding ambiguous state.

The policy does not prove Windows durability, exactly-once effects, hostile-
principal exclusion, or production readiness. It deliberately retains
terminal history for the generation and admits no cleanup-journal compaction.
These costs favor deterministic investigation over silent destructive repair.

M204 adds one architecture guard and decision documentation. It adds no native
call, runtime module, command, public type, constant, decoder, transport,
filesystem adapter, recovery store, quarantine operation, mutation,
integration fixture, dependency, compiler, workflow, job, matrix, permission,
credential, release authority, tag, publication, or CI change.

## Alternatives considered

- Use Transactional NTFS. Rejected because Microsoft recommends alternatives
  and the project would still need explicit application-level recovery.
- Use `ReplaceFile` as a transaction. Rejected because replacement is the
  wrong collision policy and documented partial states do not establish the
  required commit model.
- Permit cross-volume quarantine. Rejected because copy/delete creates another
  content-transfer and recovery protocol rather than one atomic namespace move.
- Acknowledge before durable intent. Rejected because retry lookup could not
  distinguish accepted work from a lost response.
- Infer deletion from both paths being absent. Rejected because another actor,
  rollback, or storage failure could produce the same observation.
- Automatically repair or truncate a damaged chain. Rejected because
  attacker-controlled evidence must not choose destructive recovery behavior.
- Restore after the deletion commit boundary. Rejected because this could
  resurrect or substitute data after the operation has committed to deletion.

## Validation and review boundary

The architecture guard must prove that the policy, RFC, and registrations are
present; M203, runtime, dependencies, workflows, and package surfaces remain
exact; and no cleanup/recovery command or runtime module appears. Existing
local quality, supported-Python, rendering, deterministic example,
distribution, wheel-smoke, release-rehearsal, package-inventory, documentation,
governance, and source-hygiene gates remain sufficient. No CI expansion is
introduced.

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
- [RFC-0182](0182-refresh-windows-cache-cleanup-readiness.md)
- [RFC-0186](0186-adopt-windows-cleanup-protocol-receipt-policy.md)
