# RFC-0164: probe Windows expected-identity guardian admission

- **Status:** Accepted
- **Milestone:** M181
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only guardian fixture and one two-case NTFS probe.
The guardian receives a caller-supplied `FILE_ID_INFO` identity, opens the
fixed coordination pathname while denying delete sharing, rejects reparse
points, and compares the identity on that same protecting handle before
admission. A match reaches `ready`; a mismatch closes and reports
`identity_mismatch`. Add no runtime or CI surface.

## Context

M180 shows that a pathname-only guardian protects whichever object occupies
the pathname when it starts. It cannot distinguish an unchanged generation
from a replacement created during a zero-owner interval.

Microsoft documents `FILE_ID_INFO` as a volume serial number plus a 128-bit
file identifier that identifies a file on one computer. Microsoft also
documents that `CreateFileW` sharing modes remain effective until the handle
closes. Opening without `FILE_SHARE_DELETE` before querying `FileIdInfo`
therefore lets this fixture compare and protect the same opened object. It
does not make the caller's expected identity trustworthy or durable.

## Decision

Accept the [Windows expected-identity guardian admission
probe](../security/cache-cleanup-windows-expected-identity-guardian-admission-probe.md)
as current-host, test-only evidence for two exact cases.

For the matching case, create M173's ordinary `live/coordination.lock`, retain
its `FILE_ID_INFO`, and pass that expected identity to the new child. The child
opens with read/write sharing but no delete sharing, verifies a non-inheritable
non-reparse handle, obtains `FileIdInfo`, and emits `ready` only when the
observed and expected tuples match. While live, require direct rename error 32
and exact exclusive range availability. After the exact release token, require
`closed`, successful rename, the original identity, exact bytes, and complete
cleanup.

For the mismatch case, use M174 to displace the original and create a distinct
replacement before launch. Pass the original expected identity. Require exact
`identity_mismatch`, bounded successful process settlement, then successful
rename of the replacement and exact exclusive range availability. Verify the
displaced original and moved replacement retain their respective identities
and exact bytes. Use no retry or sleep.

The child closes the mismatch handle before emitting its terminal result. A
matching handle remains the same no-delete-share handle from open through
comparison and admission. No pathname reopen occurs between comparison and
protection.

## Consequences

On the observed host, a guardian can reject a preexisting replacement when it
is given the prior object's exact identity. This closes the compare-to-
protection race for the particular handle used by the fixture.

This is not trusted identity provenance, not identity storage, not generation
authority, not guardian election, not authenticated launch, not recovery, and
not cleanup authority. The caller can supply any well-formed identity, and the
probe does not establish who issued it, where it was retained, whether it is
fresh, or which policy should act on a mismatch.

Windows remains unadmitted. Simultaneous owner loss, failed guardian launch,
hostile preexisting handles, arbitrary process trees, mapped views,
filesystem/driver variation, durable generation issuance and retention,
use-time revalidation, fail-closed policy, typed receipts, complete admission,
and independent-host proof remain open.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check
is added.

## Alternatives considered

- Trust the current pathname after a benign restart. Rejected because M180
  demonstrates that the pathname can name a replacement.
- Compare by pathname and reopen for protection. Rejected because mutation
  between comparison and reopen would reintroduce the identity race.
- Store or sign the expected identity in runtime code. Rejected because the
  necessary trust, persistence, recovery, and policy model is not yet decided.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  will collect this source test after its prerequisite stack is integrated.

## Validation

Focused validation must prove matching admission, sharing error 32, range
availability, exact close, and post-close rename. It must also prove
pre-launch substitution, exact mismatch, close-before-terminal settlement,
post-mismatch rename, original/replacement identities, exact bytes, and
complete process/stream/handle/range cleanup.

Architecture tests must preserve M180, runtime, examples, scripts,
dependencies, workflows, and the wheel package boundary. Supported-Python,
full regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [Microsoft: `GetFileInformationByHandleEx`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex)
- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `CloseHandle`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [RFC-0163](0163-probe-windows-zero-owner-guardian-restart-boundary.md)
