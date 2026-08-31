# Windows cache-cleanup use-time revalidation policy

- **Status:** Accepted decision
- **Milestone:** M202
- **Date:** 2026-08-31

## Decision

Windows is not admitted for asset-cache cleanup. Cleanup remains unimplemented
and unauthorized. This decision resolves M199 criterion 3 as policy without
creating a callable revalidation gate, native adapter, or mutation path.

A future private Windows cleanup adapter must revalidate the complete admitted
authority and candidate state immediately before every mutation boundary. The
gate uses the same retained handles and compares a fresh effective-token tuple,
trusted-root tuple, durable-generation tuple, and candidate tuple. Every field
must remain exactly equal to admission and valid for the expected mutation
phase.

No close and reopen of an admitted object is permitted. A reopened pathname, a
saved record, or an earlier successful check cannot substitute for a fresh
query through the retained objects. A saved observation is not revalidation.

## Complete use-time tuple

The future adapter must enter a private, non-reentrant single-owner gate on the
same owning thread that owns the cleanup authority. Before the first mutation,
it must freshly establish all of the following as one conjunctive use-time
tuple:

1. **Authority lifecycle.** The capability is live, unused, operation-scoped,
   owned by the current engine and thread, and still owns every admitted native
   reference. It has not been serialized, transferred, reconstructed, or
   widened.
2. **Effective principal.** The token currently effective for the thread is
   queried and its complete M201 identity/revision tuple matches admission.
3. **Trusted root and security.** The exact retained cache-root object still
   has its admitted identity, ordinary directory type, non-reparse state,
   ownership, security descriptor, and exact least-privilege authorization.
4. **Durable generation.** The exact retained generation-record object and its
   complete canonical contents, digest, policy, project/cache, root, and
   unpredictable generation bindings still match admission.
5. **Candidate and lineage.** The exact retained candidate object still has
   its admitted content identity, file identity, ordinary-file type,
   singleton-link state, non-delete-pending state, non-reparse state, and
   proven relationship to the retained root and generation.
6. **Mutation phase.** The requested private step is the exact next step bound
   into the operation. A pre-quarantine authority cannot be replayed after
   quarantine, and a later delete step requires a new phase-specific gate.

Missing, changed, ambiguous, mismatched, untrusted, invalid, or unsupported
state in any field rejects the whole gate. No field compensates for another.

## Effective-token and security revalidation

At use, the adapter must call `GetCurrentThreadEffectiveToken` or an exact
platform equivalent and requery `TOKEN_USER` and `TOKEN_STATISTICS`. It must
compare the user SID, token ID, authentication ID, modified ID, token type, and
impersonation level to the M201 admission tuple. Anonymous,
identification-only, replaced, modified, malformed, unreadable, or unsupported
token state refuses.

The adapter must then call `GetSecurityInfo` through the same retained root
handle and revalidate the owner SID, present non-null DACL, security-descriptor
digest, trusted-writer policy, and every admitted security-control field. A
fresh `AccessCheck` or the exact approved equivalent must grant only the
versioned exact least-privilege rights for the next mutation. It must not use
`MAXIMUM_ALLOWED`, backup/restore bypass, ownership takeover, DACL mutation, or
an earlier handle-open result as current application authority.

The token supplied to `AccessCheck` must represent exactly the just-verified
effective principal under a separately reviewed adapter procedure. The check
must map generic rights before evaluation, require an affirmative access
status, reject every privilege outside the approved rights profile, and reject
null-DACL or invalid-descriptor success semantics even if the platform access
function would otherwise grant access.

The existing handle may retain access granted when it was opened. That fact
does not waive the fresh application-policy check and does not make an ACL
change safe.

## Root, lineage, generation, and candidate revalidation

Every object query is handle-derived. For the root, generation record,
candidate, and every retained directory in the admitted acquisition lineage,
the adapter must use `GetFileInformationByHandleEx` or an exact approved
equivalent and obtain the applicable:

- `FILE_ID_INFO` volume serial number and 128-bit file identifier;
- `FILE_STANDARD_INFO` link count, delete-pending state, and directory type;
  and
- `FILE_ATTRIBUTE_TAG_INFO` attributes and reparse tag.

The root must remain the exact admitted ordinary non-reparse directory and must
not be delete-pending. The candidate must remain the exact admitted ordinary
non-reparse file, must not be delete-pending, and must report exactly one link
under M200. The generation record must remain the admitted ordinary
non-reparse, non-delete-pending object. Every available identity and status
field must equal its admitted value and be valid for the phase.

The root relationship is established only by a platform-proven
handle-relative, no-follow acquisition chain rooted in the retained cache-root
handle. Every retained component in that chain must still match its admitted
identity, type, and reparse/delete state. If the platform cannot freshly prove
the relationship to the same retained candidate without a weaker pathname
fallback, the operation is unsupported and refuses.

The generation gate rereads the bounded record through its retained object,
strictly decodes the versioned schema, recomputes the complete canonical
generation-record SHA-256, and compares its generation-record object identity,
project/cache digest, retained-root identity, unpredictable generation ID,
policy ID, record size, and digest to admission. A partial read, trailing data,
changed bytes, alias ambiguity, different root, or unsupported durable state
refuses.

A normalized, final, canonical, or project-confined pathname is not
revalidation. A pathname lookup, name enumeration, saved identity, timestamp,
process ID, account name, or logon ID cannot prove the live root relationship,
generation, or candidate. Path-derived information may not make a gate pass.

## Immediate and repeated mutation boundaries

The complete gate runs immediately before every mutation boundary. At minimum,
it runs before the first quarantine or rename and again after quarantine and
before deletion, delete disposition, finalization, restore, or another
irreversible namespace or object-state change. One check cannot authorize a
later mutation.

After the final successful query and before submitting the exact mutation on
the same retained candidate handle, the adapter must perform no callback, no
user or project code, no scheduling yield, no blocking wait, no queue handoff,
no request decode, no logging provider call, no pathname lookup, no close and
reopen, and no release of the private gate or owned references. The operation
may enter the operating-system call itself; the rule forbids an application-
introduced gap before that call.

This is not a claim that user-mode code prevents operating-system preemption or
hostile concurrent mutation. It is the minimum deterministic application
boundary. Criterion 6 must still test and classify changes that occur during or
after these separate platform queries.

A successful quarantine changes expected phase state. The adapter must verify
that the same retained candidate identity completed the exact expected
transition, retain that handle, advance only durable recovery state approved by
criterion 5, and perform a new phase-specific complete gate before any delete
or finalization. A batch, loop, previous candidate, or earlier successful phase
cannot reuse the gate.

## Failure and partial-transition disposition

Before the first mutation, any failed query, mismatch, race symptom, access
denial, unsupported capability, or ownership/lifecycle fault must refuse before
the first mutation. The candidate remains untouched, the single-use authority
is consumed or closed according to its future lifecycle, and no pathname,
saved-state, retry, or best-effort fallback is allowed.

If an earlier mutation phase has already completed, a later revalidation or
mutation failure is recovery-required. The adapter must not proceed to
deletion, must not guess rollback, must not reopen a path and retry, and must
not report success. Criterion 5 must define the durable intent, quarantine,
reconciliation, restore, finalization, and idempotent restart behavior before
such a state can exist in production.

A typed receipt remains criterion 4. M202 defines neither public failure codes
nor receipt fields. Future output must remain bounded and path/security-
material silent; native handles, SIDs, token identifiers, security descriptors,
file IDs, generation nonces, paths, and platform error text remain private.

## Race and atomicity boundary

Microsoft states that GetSecurityInfo does not handle race conditions. The
file-information, token-information, security-information, access-check, and
mutation calls described here are separate observations; M202 has no evidence
that they form one atomic transaction. A successful gate therefore satisfies a
policy precondition only. It does not prove that another principal or process
cannot change state after the last query.

The policy deliberately rejects any claim that “immediate” means atomic.
Production admission still requires criterion 6 hostile cross-principal,
descriptor, token, namespace, link, reparse, inheritance, and scheduling races,
plus criterion 7 independent-host and filesystem classification. A platform
combination that cannot support the final coherent design must safely refuse.

## Admission-criterion disposition

M199's seven criteria now have this exact state:

1. **Criteria 1 and 2 remain resolved as policy.** M201 defines authority,
   trusted-root, security, and generation admission. M200 requires exact
   singleton-link refusal.
2. **Criterion 3 is resolved as policy.** The complete admitted tuple must be
   freshly revalidated through the same retained objects immediately before
   every mutation phase, with no application-introduced gap or weaker fallback.
   Production enforcement remains absent.
3. **Criteria 4 through 7 remain unresolved.** Versioned bounded protocol,
   acknowledgement, and typed receipts; durable intent/quarantine/recovery;
   hostile cross-principal evidence; and independent-host/filesystem proof are
   still absent. Cross-principal adversarial proof remains criterion 6.

Resolving three policy criteria does not admit a platform. Windows is not
admitted, and cleanup remains unimplemented and unauthorized until all seven
criteria pass together in one coherent production design and adversarial
validation.

## Scope and CI boundary

M202 changes documentation, project evidence, and one architecture guard only.
It preserves M201, runtime code, integration fixtures, examples, scripts,
benchmarks, dependencies, lock, metadata, version, workflows, permissions, and
package surface. It adds no production adapter, revalidation implementation,
runtime API, CLI command, public authority, protocol, receipt, generation file,
cache access, quarantine, mutation, recovery path, native call, native code,
compiler, credential, release effect, job, matrix entry, or hosted allocation.
Existing local validation remains the acceptance path; no new hosted check is
added.

## References

- [Microsoft: `GetFileInformationByHandleEx`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [Microsoft: `FILE_STANDARD_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_standard_info)
- [Microsoft: `FILE_ATTRIBUTE_TAG_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_attribute_tag_info)
- [Microsoft: effective thread token](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentthreadeffectivetoken)
- [Microsoft: `GetTokenInformation`](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-gettokeninformation)
- [Microsoft: `GetSecurityInfo`](https://learn.microsoft.com/en-us/windows/win32/api/aclapi/nf-aclapi-getsecurityinfo)
- [Microsoft: `AccessCheck`](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-accesscheck)
- [Microsoft: `SetFileInformationByHandle`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfileinformationbyhandle)
- [MITRE CWE-367](https://cwe.mitre.org/data/definitions/367.html)
- [RFC-0182](../rfcs/0182-refresh-windows-cache-cleanup-readiness.md)
- [RFC-0183](../rfcs/0183-adopt-windows-singleton-link-refusal-policy.md)
- [RFC-0184](../rfcs/0184-adopt-windows-cleanup-authority-admission-policy.md)
- [RFC-0185](../rfcs/0185-adopt-windows-use-time-revalidation-policy.md)
