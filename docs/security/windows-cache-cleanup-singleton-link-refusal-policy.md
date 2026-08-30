# Windows cache-cleanup singleton-link refusal policy

- **Status:** Accepted decision
- **Milestone:** M200
- **Date:** 2026-08-30

## Decision

Windows is not admitted for asset-cache cleanup. Cleanup remains unimplemented
and unauthorized. This policy resolves M199 criterion 2 as policy without
adding production enforcement or mutation authority.

A candidate is link-eligible only while the exact retained opened object has a
handle-derived link count of exactly one link:

1. at admission; and
2. immediately before mutation, including any future same-filesystem
   quarantine step.

The same retained object must be used for both observations. A zero count, a
count greater than one, a changed count, or an unavailable, invalid, or
unsupported result must refuse before mutation. A saved count, pathname
metadata, or reopened name is not a substitute. Future failures require typed
receipts, but M200 defines no protocol or receipt.

Stable observation of exactly one is necessary but not sufficient. It does not
prove request authority, trusted-root ownership, generation, type, root
relationship, quiescence, protocol acknowledgement, durable recovery,
cross-principal resistance, or platform support.

## Why names are not enumerated

Do not enumerate hard-link names for admission or authority.
`FindFirstFileNameW` is a pathname-based observation over a changing namespace,
not authority over every present or future alias. An attacker or concurrent
process can alter namespace state between enumeration and use. Enumeration
also introduces path disclosure, result bounds, volume/root classification,
access-control, and error-settlement questions that do not strengthen the
retained handle at mutation.

The rule therefore accepts conservative refusal instead of attempting to
prove confinement by listing names. A future separately approved diagnostic
may use bounded enumeration only as non-authoritative evidence; it cannot make
a candidate eligible and cannot replace link-count revalidation.

## Admission-criterion disposition

M199's seven criteria now have this exact state:

1. **Criterion 1 remains unresolved.** Authenticated authority, least
   privilege, trusted-root ownership, and durable generation binding are not
   designed or implemented.
2. **Criterion 2 is resolved as policy.** Multiple-link and uncertain-link
   candidates are refused. Name enumeration is not used as authority.
3. **Criteria 3 through 7 remain unresolved.** Use-time enforcement remains
   unimplemented, including the production retained-handle adapter and joint
   identity, type, link-count, root, and generation check. Versioned bounded
   protocol and acknowledgements, typed receipts, durable intent and recovery,
   cross-principal adversarial evidence, and independent-host proof also
   remain absent.

Resolving one policy criterion does not admit a platform. Every criterion must
be satisfied by one coherent design and adversarial validation before a
mutation surface can be proposed.

## Refusal table

| Handle-derived observation | Required disposition |
| --- | --- |
| Exactly one at admission and immediately before mutation | Passes the link-policy gate only; evaluate every other criterion. |
| Zero | Refuse before mutation. |
| Greater than one | Refuse before mutation. |
| Changed between observations | Refuse before mutation. |
| Unavailable or unsupported | Refuse before mutation; do not fall back to a pathname. |
| Invalid, malformed, or inconsistent | Refuse before mutation and preserve the failure for a future typed receipt. |
| Name enumeration appears confined | No authority; the result cannot make a candidate eligible. |

No quarantine-or-delete fallback exists. A refused candidate remains
untouched.

## Ownership and failure boundary

This policy is a contract for a future private engine-owned adapter. Native
handles, link-count structures, and platform objects must remain private. A
future implementation must define acquisition, retention, close order,
single-thread or synchronization ownership, exception translation, typed
receipts, and crash recovery in a separately approved RFC.

Failure to read or revalidate the count is an unsupported-operation result,
not degraded safety. Closing a retained handle after refusal must not mutate
the candidate. M200 implements none of these operations and creates no callable
surface.

## Evidence and limits

Microsoft documents link count on opened-file information structures and hard
links as multiple names for one file. M182-M193 demonstrate on one current
Windows/NTFS host that aliases retain shared identity and that namespace,
sharing, guardian, and control observations do not independently exclude alias
mutation. CWE-367 explains why checking a pathname before use does not close a
race.

Those sources support a conservative policy, not a production claim. No M200
test invokes Win32, creates a hard link, crosses a principal, mutates a cache,
or proves behavior on ReFS, SMB, CSVFS, another Windows version, or an
independent host.

## Scope and CI boundary

M200 changes documentation and one architecture guard only. It preserves the
complete M149-M199 evidence and adds no runtime API, CLI command, public
capability, adapter, integration fixture, cache access, candidate disclosure,
quarantine, deletion, native code, dependency, compiler, version, workflow,
job, matrix entry, permission, credential, release effect, or hosted
allocation. Existing local validation remains the acceptance path.

## References

- [Microsoft: `FILE_STANDARD_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_standard_info)
- [Microsoft: `BY_HANDLE_FILE_INFORMATION`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information)
- [Microsoft: hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Microsoft: `FindFirstFileNameW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-findfirstfilenamew)
- [Microsoft: file security and access rights](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights)
- [MITRE CWE-367](https://cwe.mitre.org/data/definitions/367.html)
- [RFC-0182](../rfcs/0182-refresh-windows-cache-cleanup-readiness.md)
- [RFC-0183](../rfcs/0183-adopt-windows-singleton-link-refusal-policy.md)
