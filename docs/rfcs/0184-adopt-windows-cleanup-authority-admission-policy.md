# RFC-0184: adopt Windows cleanup-authority admission policy

- **Status:** Accepted
- **Milestone:** M201
- **Date:** 2026-08-31

## Summary

Resolve M199 admission criterion 1 as policy by requiring a future private
Windows cleanup authority to bind the exact effective access-token context,
one retained identity- and security-bound root, and one separate durable
generation record. Only the trusted composition root may issue the resulting
non-serializable, operation-scoped, single-use, cleanup-only capability.

Refuse before authority issuance whenever any token, root, security,
least-privilege, or generation fact is missing, changed, ambiguous, untrusted,
invalid, or unsupported. Do not reuse world-write capability, request data,
paths, logon identifiers, or saved evidence as cleanup authority. Windows
cleanup remains unimplemented and unauthorized.

## Context

M199 consolidated seven Windows cleanup admission criteria. M200 resolved the
hard-link criterion as a strict singleton-link refusal policy without creating
runtime enforcement. Criterion 1 still required authenticated authority,
least privilege, trusted-root ownership, and durable generation binding.

The existing `AgentCapabilities.write` contract is deliberately an immutable
composition choice for typed world transactions. The local MCP adapter defines
stdio process access as its security boundary and has no authentication
protocol. Reusing either surface for filesystem mutation would confuse world
capability selection with authenticated cleanup authority.

Windows documents that a thread may act under an impersonation token instead
of its process token. `TOKEN_USER` identifies the user, while
`TOKEN_STATISTICS` distinguishes the token, local authentication session, and
security-context revision. Windows also documents object-specific access
checks, handle-derived file identity, and handle-based security-descriptor
inspection. Parent-directory permission alone does not authorize a child, and
`GetSecurityInfo` does not prevent concurrent descriptor changes.

These facts support one conservative admission contract. They do not support
production authority, cross-principal safety, or durable recovery without the
remaining criteria.

## Decision

Accept the [Windows cleanup-authority admission
policy](../security/windows-cache-cleanup-authority-admission-policy.md).

### Trusted issuer and principal

Only a trusted composition root may attempt issuance. It must bind the exact
effective Windows access token: `TOKEN_USER` user SID plus
`TOKEN_STATISTICS` token ID, authentication ID, modified ID, token type, and
any impersonation level. Anonymous and identification-only impersonation,
unreadable or malformed token information, replacement, and unsupported token
types fail closed.

The authentication ID remains a local session binding, not a durable cache
generation. A CLI flag, MCP request, actor ID, project file, environment value,
or existing `AgentCapabilities.write` value cannot mint cleanup authority.

### Trusted root

The issuer must retain one exact root handle and bind its `FILE_ID_INFO`
volume/file identity, type, delete state, attributes/reparse tag, owner SID,
non-null DACL, and exact security-policy digest. The root must be an ordinary,
non-reparse, non-delete-pending directory owned by the admitted user SID.

The DACL may grant mutation-relevant rights only to a bounded trusted-principal
set fixed outside request data. Null, unreadable, unknown, owner-mismatched, or
untrusted-writer security state fails closed. A versioned least-privilege
rights profile must be evaluated without `MAXIMUM_ALLOWED`, backup/restore
bypass, ownership takeover, or DACL-changing authority. Handle-open success
and pathname confinement are not application authorization.

### Durable generation

The issuer must separately bind an immutable, root-confined, versioned durable
generation record. The record identifies the project/cache, retained root,
unpredictable generation, policy, generation-record object, and complete
canonical-record SHA-256. It must settle durably through a future
platform-proven no-follow, handle-relative mechanism before issuance.

The record is not a capability. A timestamp, path, process, token, user, logon
session, guardian name, or in-memory counter cannot substitute for it. Missing,
mutable, replayed, differently rooted, mismatched, or not-provably-durable
state fails closed.

### Private capability

The resulting capability is private, engine-owned, non-serializable,
operation-scoped, single-use, and cleanup-only. It owns or retains the live
bindings needed to support later revalidation, has explicit close semantics,
and cannot be reconstructed from diagnostics or saved evidence. Native
objects, raw SIDs, token/root identifiers, security descriptors, generation
nonces, and paths do not enter public APIs, canonical state, telemetry, or
future receipts.

This decision resolves criterion 1 as policy only. Criterion 2 remains
resolved as policy under M200. Criteria 3 through 7 remain unresolved,
including production use-time revalidation, protocol/receipts, durable
mutation recovery, cross-principal adversarial proof, and independent-host
support. The admission snapshot is explicitly raceable and cannot admit
cleanup by itself.

This is a direction-preserving refinement under ADR-0017, ADR-0019, and
RFC-0129 through RFC-0131. It is a no authority increase decision. Preserve
M200, runtime, fixtures, examples, scripts, dependencies, lock, metadata,
workflows, permissions, version, and package surface exactly. Use no new
hosted allocation.

## Consequences

The project gains an auditable answer to what could eventually authorize a
Windows cleanup operation. Authority cannot be inferred from a user account,
an open handle, a root path, a world-write flag, or a saved cache observation.
Authentication, root ownership/security, and generation are distinct required
bindings.

The policy deliberately accepts false refusal. Existing cache roots whose
ownership, DACL, filesystem identity, reparse status, or durable generation
cannot satisfy the exact contract are unsupported. No compatibility fallback
is allowed.

Security-descriptor and token changes remain raceable. A future criterion-3
RFC must define immediate use-time revalidation against the same retained
objects, and criterion 6 must supply hostile cross-principal evidence. A future
criterion-5 RFC must define generation issuance, rotation, intent, quarantine,
recovery, and persistence behavior before any adapter can be admitted.

M201 adds one architecture guard and decision documentation. It adds no
production adapter, runtime API, command, protocol, decoder, public capability,
generation record, cache access, mutation, integration fixture, native code,
dependency, compiler, version, workflow, job, matrix, permission, credential,
release authority, tag, publication, or CI change. No new hosted allocation is
added.

## Alternatives considered

- Reuse `AgentCapabilities.write`. Rejected because it is a trusted local
  composition switch for world transactions, not authenticated filesystem
  authority or durable generation provenance.
- Bind only the user SID. Rejected because it does not distinguish token
  instances, impersonation context, security-context modification, or cache
  generation.
- Treat the logon-session authentication ID as generation. Rejected because it
  is local token context, not a durable root-confined cache lifecycle record.
- Trust a successfully opened root. Rejected because Windows grants requested
  object access under the effective token; open success does not prove the
  project's ownership policy, DACL trust, or generation.
- Trust a normalized or final path. Rejected because a name is not the retained
  object identity or an atomic root/security proof.
- Implement the adapter now. Rejected because criteria 3 through 7 remain
  unresolved and no production mutation authority is approved.
- Add a Windows hosted job. Rejected because M201 changes policy and an
  architecture guard only; the existing suite is the future execution path.

## Validation

Architecture validation must:

- preserve exact M200, runtime, examples, scripts, integration fixtures,
  dependencies, lock, metadata, workflows, permissions, and package surface;
- require trusted-composition issuance and the complete effective-token tuple;
- require retained root identity, owner, non-null DACL, reparse/type, and
  least-privilege security admission with no pathname authority;
- require a separate immutable, root-confined, versioned durable generation
  binding and reject logon-session substitution;
- keep the capability private, non-serializable, operation-scoped, single-use,
  cleanup-only, and path/security-material silent;
- mark criterion 1 resolved as policy, retain criterion 2, and leave criteria 3
  through 7 unresolved;
- retain Windows non-admission and the absence of cleanup commands, adapters,
  generation state, or public authority; and
- require public registration of RFC-0184 and the policy decision without CI
  expansion.

Run focused architecture tests, whole-tree static checks, strict docs, static
and current-date governance, supported-Python regression, reproducible package
and release rehearsals, findings-first review, and exact scratch cleanup before
local closeout. Claim no hosted result without an actual safely published run.

## References

- [Microsoft: effective thread token](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentthreadeffectivetoken)
- [Microsoft: `TOKEN_USER`](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_user)
- [Microsoft: `TOKEN_STATISTICS`](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_statistics)
- [Microsoft: `GetSecurityInfo`](https://learn.microsoft.com/en-us/windows/win32/api/aclapi/nf-aclapi-getsecurityinfo)
- [Microsoft: `AccessCheck`](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-accesscheck)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [Microsoft: `FILE_ATTRIBUTE_TAG_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_attribute_tag_info)
- [Microsoft: file security and access rights](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights)
- [MITRE CWE-367](https://cwe.mitre.org/data/definitions/367.html)
- [ADR-0017](../adr/0017-content-addressed-project-confined-assets.md)
- [ADR-0019](../adr/0019-agent-service-capabilities-and-safe-points.md)
- [RFC-0129](0129-defer-asset-cache-cleanup.md)
- [RFC-0130](0130-asset-cache-cleanup-threat-model.md)
- [RFC-0131](0131-defer-portable-cache-cleanup-capability.md)
- [RFC-0182](0182-refresh-windows-cache-cleanup-readiness.md)
- [RFC-0183](0183-adopt-windows-singleton-link-refusal-policy.md)
