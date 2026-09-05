# RFC-0185: adopt Windows use-time revalidation policy

- **Status:** Accepted
- **Milestone:** M202
- **Date:** 2026-08-31

## Summary

Resolve M199 admission criterion 3 as policy by requiring a future private
Windows cleanup adapter to revalidate the complete M200-M201 admitted state
through the same retained token, root, generation, lineage, and candidate
objects immediately before every mutation boundary.

Require exact equality with admission, fresh least-privilege security
evaluation, an uninterrupted private gate before the same-handle mutation, and
a new complete gate before every later irreversible phase. Refuse before the
first mutation on any missing, changed, ambiguous, mismatched, untrusted,
invalid, or unsupported fact. Treat failure after a completed transition as
recovery-required without guessing rollback or continuing deletion.

Windows cleanup remains unimplemented and unauthorized. This RFC adds no
runtime or hosted CI surface.

## Context

M199 consolidated seven Windows cleanup admission criteria. M200 resolved the
hard-link criterion as a singleton-link refusal policy. M201 resolved authority
admission as policy by binding the exact effective token, retained trusted root
and security, and a separate durable generation into a private single-use
capability.

Those admission observations are not permanent. The current effective token,
security descriptor, link count, reparse/type state, generation bytes,
namespace relationships, and candidate state may change before quarantine,
delete disposition, restore, or finalization. M199 criterion 3 therefore
requires a handle-retained check immediately at use.

Microsoft documents that `FILE_ID_INFO` identifies a file on one computer when
combined with the volume serial number. `FILE_STANDARD_INFO` exposes link
count, delete-pending, and directory state; `FILE_ATTRIBUTE_TAG_INFO` exposes
attributes and reparse tag. Windows also exposes current effective-token and
handle-based security queries plus object-specific access checks.

These are separate functions. Microsoft explicitly states that
`GetSecurityInfo` does not handle race conditions. A user-mode sequence cannot
be described as atomic merely because its calls are adjacent. The policy can
remove application-introduced gaps and define strict refusal, but production
admission still requires cross-principal adversarial evidence and independent-
host classification.

## Decision

Accept the [Windows cache-cleanup use-time revalidation
policy](../security/windows-cache-cleanup-use-time-revalidation-policy.md).

### Same retained objects

The future adapter must retain the exact M201 authority objects and the exact
admitted candidate. Revalidation uses those owned references; it does not close
and reopen a name, deserialize an earlier result, enumerate aliases, or trust a
saved path or observation.

The fresh use-time tuple contains:

- the capability lifecycle and owning engine/thread;
- the current effective-token identity and revision;
- the trusted root identity, type, reparse/delete state, owner, DACL, security
  digest, trusted-writer policy, and exact access decision;
- the durable generation-record identity, root/project/cache/policy bindings,
  canonical bytes, and digest;
- the retained acquisition-lineage identities and states; and
- the candidate content/file identity, ordinary-file state, singleton link
  count, non-delete-pending/reparse state, root relationship, generation, and
  operation phase.

Every required field must equal admission and the phase's expected state. A
partial or unavailable tuple refuses; no field, path, open success, or earlier
pass can compensate for another.

### Fresh token and security evaluation

The same owning thread must freshly query the token currently effective for it
and compare the `TOKEN_USER` and `TOKEN_STATISTICS` user SID, token ID,
authentication ID, modified ID, token type, and impersonation level with M201.
The adapter must reject replacement, modification, anonymous or identification-
only impersonation, malformed data, query failure, and unsupported state.

Through the retained root handle, the adapter must freshly query owner and DACL
with `GetSecurityInfo`, compare the complete security binding, and perform
`AccessCheck` or the exact approved equivalent for only the versioned rights
needed by the next step. Null DACL, unknown ACE semantics, untrusted writers,
owner mismatch, descriptor change, overbroad privilege, or failed/denied access
refuses. Existing handle access and `MAXIMUM_ALLOWED` are not authority.

### Identity, lineage, generation, and candidate

The adapter must query `FILE_ID_INFO`, `FILE_STANDARD_INFO`, and
`FILE_ATTRIBUTE_TAG_INFO` as applicable through the retained root, generation,
candidate, and lineage handles. Identity, directory/file type, delete state,
reparse state, and the candidate's exactly-one link count must remain admitted
and phase-valid.

Root relationship must be freshly proven through the platform-approved handle-
relative, no-follow acquisition lineage. A pathname string or final-name query
cannot make the relationship pass. If the platform cannot prove the lineage
without a weaker fallback, the operation is unsupported.

The bounded generation record must be reread through the retained object,
strictly decoded, canonically hashed, and compared in full. Object identity,
project/cache, root, unpredictable generation, policy, size, bytes, and digest
must remain exact. Saved evidence, time, process/logon identity, or a path is
not a generation check.

### Every mutation boundary

The complete gate runs before the first quarantine/rename and again after any
successful phase before deletion, delete disposition, finalization, restore,
or another irreversible change. One successful gate cannot authorize a batch
or later phase.

The adapter holds its non-reentrant single-owner gate and all owned references
from the final successful observation into the same-handle mutation call. It
introduces no callback, user/project code, voluntary scheduling yield, blocking
wait, queue handoff, request decoding, provider call, pathname lookup, reopen,
or ownership release between them.

This eliminates avoidable application gaps; it does not prevent operating-
system preemption or make separate Win32 calls atomic. Criterion 6 must test
hostile changes during the sequence.

### Failure phases

Any failure before the first mutation leaves the candidate untouched and
refuses the operation. There is no retry by name, best-effort path, or fallback
to a prior observation.

After a successful namespace transition, a later failure must stop before
deletion and enter a private recovery-required disposition. The implementation
must not guess rollback, continue, or claim success. Criterion 5 must define
durable intent and idempotent recovery before this can become runtime behavior;
criterion 4 must define any typed receipt.

### Criterion status and authority boundary

M200-M202 resolve criteria 1, 2, and 3 as policy only. Criteria 4 through 7
remain unresolved: protocol/acknowledgement/receipts, durable mutation recovery,
hostile cross-principal evidence, and independent-host/filesystem proof.

This is a direction-preserving refinement under ADR-0017, ADR-0019, and
RFC-0129 through RFC-0131. It is a no authority increase decision. There is no
production adapter or callable revalidation surface. Preserve M201, runtime,
fixtures, examples, scripts, dependencies, lock, metadata, workflows,
permissions, version, and package surface exactly. Use no new hosted
allocation.

## Consequences

Reviewers gain one precise answer to when admitted Windows state must be
rechecked and which objects/fields participate. The policy forbids stale
snapshot reuse, pathname reopening, one-check-per-batch behavior, and silent
continuation after a partial transition.

The policy deliberately accepts false refusal. A changed token revision,
security descriptor, root/generation/candidate identity, lineage, link count,
type, reparse/delete state, record digest, capability phase, or unavailable
query stops progress. An unsupported filesystem or adapter is not degraded to
a path implementation.

The security and mutation queries remain non-atomic. M202 does not establish
cross-principal safety, quiescence, durable recovery, receipt semantics,
independent-host support, or production readiness.

M202 adds one architecture guard and decision documentation. It adds no native
call, implementation, production adapter, runtime API, command, protocol,
decoder, public capability, generation file, cache access, quarantine,
mutation, recovery path, integration fixture, dependency, compiler, version,
workflow, job, matrix, permission, credential, release authority, tag,
publication, or CI change. No new hosted allocation is added.

## Alternatives considered

- Revalidate only candidate identity. Rejected because token, root security,
  generation, lineage, type, link, and lifecycle state are equally necessary.
- Reopen the candidate by its final pathname. Rejected because reopening can
  select a replacement and a path is not authority.
- Check once before a multi-step cleanup. Rejected because quarantine changes
  phase state and later deletion requires a new complete gate.
- Treat adjacent checks as atomic. Rejected because Microsoft explicitly
  documents the security query's race boundary and the calls are separate.
- Automatically roll back after a post-quarantine mismatch. Rejected because
  rollback requires the durable criterion-5 state machine and may itself race
  or mutate the wrong object.
- Implement the adapter now. Rejected because criteria 4 through 7 remain
  unresolved and there is no admitted complete mutation/recovery design.
- Add another Windows hosted job. Rejected because this policy-only change has
  no new implementation for another allocation to validate.

## Validation

Architecture validation must:

- preserve exact M201, runtime, examples, scripts, integration fixtures,
  dependencies, lock, metadata, workflows, permissions, and package surface;
- require the same retained authority/root/generation/lineage/candidate objects
  and complete equality with admission;
- require fresh effective-token, owner/DACL/security-digest, and exact-rights
  access checks;
- require handle-derived identity, type, link, delete/reparse, root-relation,
  and generation-record revalidation;
- require an uninterrupted single-owner boundary before every same-handle
  mutation phase;
- distinguish untouched pre-mutation refusal from recovery-required partial
  transitions without defining protocol or recovery behavior;
- mark criterion 3 resolved as policy, retain criteria 1 and 2, and leave
  criteria 4 through 7 unresolved;
- preserve the explicit non-atomic/cross-principal/independent-host limits;
- retain Windows non-admission and the absence of cleanup or revalidation
  implementation; and
- require public registration of RFC-0185 and the policy without CI expansion.

Run focused architecture tests, whole-tree static checks, strict docs, static
and current-date governance, supported-Python regression, reproducible package
and release rehearsals, findings-first review, and exact scratch cleanup before
local closeout. Claim no hosted result without an actual safely published run.

## References

- [Microsoft: `GetFileInformationByHandleEx`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [Microsoft: `FILE_STANDARD_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_standard_info)
- [Microsoft: `FILE_ATTRIBUTE_TAG_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_attribute_tag_info)
- [Microsoft: effective thread token](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentthreadeffectivetoken)
- [Microsoft: `GetSecurityInfo`](https://learn.microsoft.com/en-us/windows/win32/api/aclapi/nf-aclapi-getsecurityinfo)
- [Microsoft: `AccessCheck`](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-accesscheck)
- [Microsoft: `SetFileInformationByHandle`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfileinformationbyhandle)
- [MITRE CWE-367](https://cwe.mitre.org/data/definitions/367.html)
- [ADR-0017](../adr/0017-content-addressed-project-confined-assets.md)
- [ADR-0019](../adr/0019-agent-service-capabilities-and-safe-points.md)
- [RFC-0129](0129-defer-asset-cache-cleanup.md)
- [RFC-0130](0130-asset-cache-cleanup-threat-model.md)
- [RFC-0131](0131-defer-portable-cache-cleanup-capability.md)
- [RFC-0182](0182-refresh-windows-cache-cleanup-readiness.md)
- [RFC-0183](0183-adopt-windows-singleton-link-refusal-policy.md)
- [RFC-0184](0184-adopt-windows-cleanup-authority-admission-policy.md)
