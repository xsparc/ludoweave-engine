# Windows post-admission hard-link creation probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M183
- **Date:** 2026-08-29
- **Baseline:** M182's hard-link alias non-exclusion boundary

## Decision

Retain one Windows-only, test-only NTFS observation showing that M181's
matching no-delete-share guardian does not prevent a same-user caller from
adding a hard-link alias after admission. The exact opened pathname remains
protected, but the link set is not frozen. Treat this as a negative ownership
boundary, not root-confined ownership and not cleanup authority. Windows is
not admitted.

## Why admission does not freeze ownership

M181 admits one already protecting handle after comparing the expected
`FILE_ID_INFO`. M182 shows that another entry which already names that file can
be renamed. M183 begins with exactly one link and shows that a second entry can
be created after the guardian reaches `ready`.

The guardian still identifies and protects the object opened through
`live/coordination.lock`. It does not authenticate every directory on the
volume or control future directory-entry creation. `NumberOfLinks` changes
from one to two on the already open original handle, demonstrating that link
count is live state rather than immutable admission evidence.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_post_admission_hard_link_creation_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` and an empty peer
   directory;
2. opens the coordination file through the existing capability helper,
   retains its `FILE_ID_INFO`, and requires link count one;
3. starts M181's guardian with that identity and requires exact `ready` while
   the process remains live;
4. requires rename of the exact opened coordination pathname to fail with
   Windows sharing error 32;
5. creates `peer/coordination.alias` with `os.link` while the guardian remains
   live;
6. requires both open handles to retain the original identity, both link
   counts to equal two, exact bytes, and exclusive byte-range availability
   through both names;
7. requires a second coordination-path rename to fail with error 32, then
   performs the exact release and requires exact `closed`;
8. renames the coordination entry successfully and verifies both remaining
   names retain identity, link count two, exact bytes, and complete process,
   stream, native-handle, and range cleanup.

The probe uses no retry or sleep. It reuses the accepted helpers and fixture;
it adds no native declaration, production import, environment-derived control
input, shell, network access, or inherited handle.

## Security consequence

The link set is not frozen by expected-identity guardian admission on the
observed host. A one-link precondition can become two while the guardian stays
live. Expected identity and a prior link-count sample are not root-confined
ownership and cannot independently authorize cleanup.

A future design must decide which roots are trusted, whether any multiple-link
state is acceptable, when and how link count is revalidated, how a count
change fails closed, and which typed receipt records that refusal. M183 does
not define those policies or imply that enumeration itself would be race-free.

This probe uses one process and one principal. It does not establish behavior
for another process or principal, enumerate hard links, create across volumes,
delete an alias, authenticate parent directories, or cover ReFS, SMB, other
drivers, or independent Windows hosts. File-ID reuse, durable generation
provenance, failed launch, simultaneous owner loss, hostile handles, mapped
views, recovery, and cleanup authority remain unresolved.

No runtime or package surface changes. No production subprocess, native API,
cache mutation, dependency, workflow, permission, or hosted allocation is
added. No hosted check is added. Windows is not admitted.

## Revisit criteria

Revisit Windows admission only after a design supplies trusted root ownership,
explicit hard-link and link-count policy, use-time identity revalidation,
generation provenance, failure-safe launch and recovery behavior, typed
receipts, and independent-host evidence without expanding essential CI merely
to repeat this bounded observation.

## References

- [Microsoft: `CreateHardLinkW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createhardlinkw)
- [Microsoft: Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Microsoft: `FILE_LINK_INFORMATION`](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_link_information)
- [Microsoft: `BY_HANDLE_FILE_INFORMATION`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information)
- [Python: `os.link`](https://docs.python.org/3/library/os.html#os.link)
- [RFC-0166](../rfcs/0166-probe-windows-post-admission-hard-link-creation.md)
