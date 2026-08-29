# Windows expected-identity guardian admission probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M181
- **Date:** 2026-08-29
- **Baseline:** M180's zero-owner guardian restart boundary

## Decision

Retain one Windows-only, test-only guardian fixture and two controlled NTFS
observations. The fixture admits an already protecting handle only when its
`FILE_ID_INFO` matches a caller-supplied expected identity. It closes and
reports `identity_mismatch` when the pathname already names a replacement.
This is not trusted identity provenance and not generation authority. Windows
is not admitted.

## Why the same opened handle matters

M180's guardian denies delete sharing as soon as it opens, but has no expected
identity. M181 adds the missing comparison without reopening the pathname. The
child first opens `live/coordination.lock` with read/write sharing and no delete
sharing, verifies that the handle is non-inheritable and not a reparse point,
then queries `FileIdInfo` on that same handle.

If the observed tuple matches, the already protecting handle remains open and
the child emits `ready`. If it differs, the child closes the handle before it
emits the terminal `identity_mismatch` event. This ordering avoids a
compare-to-protection gap for the admitted handle and avoids leaking namespace
protection on mismatch.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_expected_identity_guardian_admission_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` beneath an NTFS
   pytest root and retains its original `FILE_ID_INFO` and bytes;
2. starts the identity guardian with that expected tuple and requires exact
   `ready` while the process remains live;
3. requires direct rename error 32 while the matching guardian is live and
   exact exclusive range availability;
4. releases the guardian with one exact token, requires exact `closed`, then
   requires rename success, original identity, exact bytes, and complete
   cleanup;
5. in the negative case, uses M174 substitution before guardian launch and
   retains the displaced original and distinct replacement identities;
6. starts the guardian with the original expected identity and requires exact
   `identity_mismatch` plus bounded successful settlement;
7. requires direct rename of the replacement and exact exclusive range
   availability after mismatch, proving the rejected handle no longer protects
   the namespace; and
8. verifies the displaced original and moved replacement identities, exact
   bytes, and complete process, stream, native-handle, and range cleanup.

The probe uses no retry or sleep. The child accepts only a canonical unsigned
64-bit decimal volume serial and exactly 16 lowercase hexadecimal identity
bytes. It has no environment-derived control input, shell, network, runtime
import, or inherited handle.

## Security consequence

The observed guardian can reject a replacement when a correct prior identity
is supplied. That is narrower than continuity or recovery. The test creates
and passes the expected identity in one controlled process tree; it does not
establish how production code would obtain, authenticate, persist, rotate, or
revalidate that value.

This is not trusted identity provenance, not durable identity storage, not
generation authority, not guardian election, not authenticated launch, not
crash recovery, and not cleanup authority. A malicious or stale expected value
can still cause denial or misclassification, and no policy or receipt is
defined for either result.

Simultaneous loss, failed launch, hostile preexisting handles, arbitrary
process trees, mapped views, filesystem/driver variation, durable generation
issuance, trusted root placement, use-time revalidation, fail-closed policy,
typed receipts, complete admission, and independent hosts remain unresolved.
Windows is not admitted.

## Scope and CI restraint

M181 adds one fixture and one integration probe only under `tests/`, plus an
architecture guard and decision documentation. It adds no runtime subprocess
or `ctypes`, adapter, guardian or lock API, public probe, cache access, cleanup
authority, mutation command, dependency, native extension, compiler
requirement, workflow, job, permission, or CI allocation. The existing Windows
suite is the only future hosted execution path; no hosted check is added.

## References

- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [Microsoft: `GetFileInformationByHandleEx`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex)
- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `CloseHandle`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)
- [M174 pathname-substitution probe](cache-cleanup-windows-cooperative-lock-substitution-probe.md)
- [M180 zero-owner restart boundary](cache-cleanup-windows-zero-owner-guardian-restart-boundary-probe.md)
