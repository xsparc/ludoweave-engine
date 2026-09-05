# Windows cache-cleanup authority admission policy

- **Status:** Accepted decision
- **Milestone:** M201
- **Date:** 2026-08-31

## Decision

Windows is not admitted for asset-cache cleanup. Cleanup remains unimplemented
and unauthorized. This decision resolves M199 criterion 1 as policy without
creating a callable authority, native adapter, or mutation path.

A future Windows cleanup authority may be issued only by the trusted
composition root after it binds all three of these independent records:

1. the exact effective Windows access token and its security-context revision;
2. one retained, identity- and security-bound cache root; and
3. one separate durable generation record confined to that root.

The binding is conjunctive. A valid token cannot compensate for an uncertain
root, a trusted root cannot compensate for a missing generation, and saved
evidence cannot mint or restore authority. Every absent, changed, ambiguous,
invalid, untrusted, or unsupported observation must refuse before authority
issuance.

## Effective-principal binding

The authority issuer must inspect the token that is effective for the calling
thread: the thread impersonation token when one exists, otherwise the process
token. It must obtain and bind at least:

- the `TOKEN_USER` user SID;
- the `TOKEN_STATISTICS` token ID, authentication ID, and modified ID;
- token type; and
- impersonation level when the token is an impersonation token.

`SecurityAnonymous` and `SecurityIdentification` impersonation levels are
insufficient and must refuse before authority issuance. A failure to query any
required field, an invalid token shape, or an unsupported token type has the
same disposition. A future implementation must retain an owned token reference
or an equivalently strong engine-owned binding and later detect replacement or
modification before use.

The user SID names the principal. The token ID distinguishes the token object,
the authentication ID binds its local logon session, and the modified ID
detects a changed security context. These identifiers are one admission tuple;
none is independently sufficient. In particular, the logon session is not
generation authority and is not durable across the cache lifecycle.

The existing `AgentCapabilities.write` flag is not authentication. It enables
typed world transactions only when a trusted local composition selects it. A
CLI flag, MCP request, actor ID, project document, environment value, path,
cache inventory, fingerprint, preview, or saved receipt cannot supply or
extend cleanup authority.

## Trusted-root binding

The future adapter must retain the exact root object before it considers
authority issuance. The admission tuple must be derived from the retained root
handle, never from a reopened pathname, and must include:

- `FILE_ID_INFO` volume serial number and 128-bit file identifier;
- directory/type and deletion state from handle-derived information;
- `FILE_ATTRIBUTE_TAG_INFO` attributes and reparse tag;
- the owner SID and a non-null DACL returned by `GetSecurityInfo`; and
- a SHA-256 binding of the exact admitted security descriptor and policy
  identifier.

The root must be an ordinary directory, not delete-pending, and not a reparse
point. Its owner SID must equal the admitted effective-token user SID. The DACL
must be present and must not grant mutation-relevant rights to an untrusted
writer. Every allowed writer must come from a bounded trusted-principal set
fixed by the composition root; that set is not request data. Unknown or
unsupported ACE semantics, a null DACL, unreadable ownership, an owner
mismatch, or an untrusted writer must refuse before authority issuance.

`AccessCheck` or an equivalently exact platform access evaluation must confirm
the admitted principal and the versioned least-privilege rights profile. The
adapter must not request `MAXIMUM_ALLOWED`, backup/restore bypass, ownership
takeover, DACL mutation, or another privilege broader than the exact future
operation requires. Successfully opening a handle proves only that Windows
granted its requested access; it does not itself prove project ownership or
application authority.

A normalized, final, canonical, or project-confined pathname is not authority.
Names may be useful diagnostics only after separate privacy and bounds review.
They cannot replace the retained root handle, its object identity, or its
security binding.

## Durable-generation binding

Principal identity and root identity do not identify a cache generation. A
future issuer must admit a separate durable generation record with a versioned
schema. The record must be immutable, root-confined, and created through the
same no-follow, handle-relative trust boundary before authority issuance. Its
minimum binding is:

- protocol identifier `ludoweave.windows-cache-generation/1`;
- exact project/cache identity digest;
- retained root identity;
- an unpredictable generation identifier;
- policy identifier `ludoweave.windows-cleanup-authority/1`;
- generation-record object identity; and
- SHA-256 of the complete canonical record.

The record is evidence bound into an authority; it is not itself a capability.
Its bytes and identity must be committed through a platform-proven durable
write and metadata-settlement sequence before issuance. A later process may
reconstruct the binding only after reacquiring the exact trusted root and
revalidating the complete immutable record. A timestamp, process ID, pathname,
user SID, token ID, authentication ID, guardian name, or in-memory counter is
not a durable generation record.

Missing, mutable, malformed, replayed, differently rooted, differently
secured, digest-mismatched, unsupported, or not-provably-durable generation
state must refuse before authority issuance. M201 specifies this admission
contract but does not implement generation creation, rotation, recovery, or
storage. Those mechanisms must compose with criterion 5 before cleanup can be
admitted.

## Capability shape and least privilege

The resulting future capability must be a private, engine-owned,
non-serializable, operation-scoped, single-use, cleanup-only object. It must
contain or own the live platform bindings needed to prove the admission tuple;
it is not request data and cannot be reconstructed from its diagnostic fields.
It must have explicit single-thread ownership, deterministic close semantics,
and fail closed if a required owned reference is lost.

Saved evidence cannot mint, widen, transfer, refresh, or replay the capability.
Raw SID values, token identifiers, native handles, security descriptors,
root/file identifiers, generation nonces, and filesystem paths must not enter
public output, canonical world state, diagnostics, telemetry, or future typed
receipts. Future public results may expose only bounded policy identifiers,
content digests, and stable refusal codes approved with the protocol.

No authority is ambient or global. The capability does not enter the package
root, asset contracts, agent service, CLI, MCP adapter, or project manifest.

## Admission-criterion disposition

M199's seven criteria now have this exact state:

1. **Criterion 1 is resolved as policy.** Authentication, least privilege,
   trusted-root ownership, and durable generation have one conjunctive,
   fail-closed admission contract. Production issuance remains absent.
2. **Criterion 2 remains resolved as policy.** M200 requires a handle-derived
   singleton link count at admission and immediately before mutation.
3. **Criteria 3 through 7 remain unresolved.** Security-descriptor
   revalidation remains criterion 3 together with exact use-time token, root,
   generation, identity, type, and link-count checks. Protocol framing,
   acknowledgement and typed receipts; durable mutation intent and recovery;
   cross-principal adversarial proof remains criterion 6; and independent-host
   support remain absent.

Resolving two policy criteria does not admit a platform. Windows is not
admitted, and cleanup remains unimplemented and unauthorized until all seven
criteria pass together in one coherent production design and adversarial
validation.

## Failure and race boundary

Microsoft documents that security descriptors can change concurrently and
that `GetSecurityInfo` does not close that race. M201 therefore treats the
admission snapshot as necessary but not sufficient. Criterion 3 must requery
the same retained root and token binding immediately at mutation; criterion 6
must test hostile cross-principal descriptor, token, namespace, alias, and
inheritance changes. No admission-time snapshot may be described as immutable.

Failure produces no fallback to a path, process identity, account name,
default ACL, saved record, or previously successful authority. A refused
request has no cache side effect. Future cleanup protocol and receipt work must
define stable refusal codes without disclosing security material.

## Evidence and limits

Windows documents the effective-token distinction, token user and revision
information, handle-derived file identity, object security descriptors, and
access checks. Those primitives support a conservative admission policy.
They do not prove this repository has implemented them, that security changes
cannot race, that a durable generation mechanism works, or that an unrelated
principal or independent host is excluded.

M201 adds no Windows integration fixture and invokes no native API. It records
policy, not behavior, portability, or production readiness.

## Scope and CI boundary

M201 changes documentation, project evidence, and one architecture guard only.
It preserves M200, runtime code, integration fixtures, examples, scripts,
dependencies, lock, metadata, version, workflows, permissions, and package
surface. It adds no production adapter, runtime API, CLI command, public
authority, cache access, generation file, quarantine, mutation, native code,
compiler, credential, release effect, job, matrix entry, or hosted allocation.
Existing local validation remains the acceptance path; no new hosted check is
added.

## References

- [Microsoft: effective thread token](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentthreadeffectivetoken)
- [Microsoft: `TOKEN_USER`](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_user)
- [Microsoft: `TOKEN_STATISTICS`](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_statistics)
- [Microsoft: `TOKEN_ORIGIN`](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_origin)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [Microsoft: `FILE_ATTRIBUTE_TAG_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_attribute_tag_info)
- [Microsoft: `GetSecurityInfo`](https://learn.microsoft.com/en-us/windows/win32/api/aclapi/nf-aclapi-getsecurityinfo)
- [Microsoft: `AccessCheck`](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-accesscheck)
- [Microsoft: file security and access rights](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights)
- [MITRE CWE-367](https://cwe.mitre.org/data/definitions/367.html)
- [RFC-0182](../rfcs/0182-refresh-windows-cache-cleanup-readiness.md)
- [RFC-0183](../rfcs/0183-adopt-windows-singleton-link-refusal-policy.md)
- [RFC-0184](../rfcs/0184-adopt-windows-cleanup-authority-admission-policy.md)
