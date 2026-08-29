# Windows hard-link alias non-exclusion probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M182
- **Date:** 2026-08-29
- **Baseline:** M181's expected-identity guardian admission boundary

## Decision

Retain one Windows-only, test-only NTFS observation showing that M181's
matching no-delete-share guardian protects the exact pathname it opens but
does not exclude rename through a preexisting hard-link alias. Treat the
result as a negative ownership boundary, not root-confined ownership and not
cleanup authority. Windows is not admitted.

## Why identity is not namespace ownership

A hard link is a directory entry for a file. Multiple same-volume entries can
name one object. `FILE_ID_INFO` identifies the object opened by a handle, and
`NumberOfLinks` reports how many entries refer to it, but neither value proves
where every entry resides or who controls its parent directory.

M181 correctly compares expected identity on its already protecting handle.
M182 demonstrates why that is insufficient as a sole ownership condition. On
the observed NTFS host, the handle's lack of delete sharing rejects rename of
`live/coordination.lock`; it does not prevent rename of the preexisting
`peer/coordination.alias` directory entry that names the same file.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_hard_link_alias_non_exclusion_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` and a peer hard-link
   alias with `os.link`;
2. opens both through the existing capability helper and requires equal
   `FILE_ID_INFO` plus link counts of at least two before guardian launch;
3. starts M181's guardian with the original identity and requires exact
   `ready` while the process remains live;
4. requires rename of the opened coordination pathname to fail with Windows
   sharing error 32;
5. renames the preexisting alias successfully while the guardian remains live,
   then verifies the moved alias retains the original identity and link count;
6. requires exclusive byte-range acquisition to remain available through both
   names and a second coordination-path rename to fail with error 32;
7. performs the exact release, requires exact `closed`, and then renames the
   coordination entry successfully; and
8. verifies both remaining names retain the original identity, link count,
   exact bytes, and complete process, stream, native-handle, and range cleanup.

The probe uses no retry or sleep. It reuses the accepted helpers and fixture;
it adds no native declaration, production import, environment-derived control
input, shell, network access, or inherited handle.

## Failed hypothesis retained as evidence

The first M182 live run expected both rename attempts to fail. The exact opened
name did fail with error 32, but the alias rename completed. The test failed at
the expected-exception assertion. The corrected probe encodes that observed
asymmetry and additionally proves that the guardian survives the alias rename
and continues to protect the exact name it opened.

Retaining this correction matters: replacing the result with the intended
outcome would create a false security claim. The observation establishes
hard-link alias non-exclusion on this host; it does not establish deletion
behavior or a universal filesystem rule.

## Security consequence

Expected object identity is not sole-name authority and not root-confined
ownership. A matching `FILE_ID_INFO` cannot by itself prove that all names for
the object are inside the intended cache root or under one principal's control.
A future design must decide trusted-root placement, multiple-link policy,
link-count revalidation, race handling, and failure receipts before mutation.

This probe does not create a hard link after guardian admission, enumerate
every link, test deletion through an alias, cross a volume, authenticate either
directory, or cover ReFS, SMB, other drivers, or independent Windows hosts.
File-ID reuse, durable generation provenance, failed launch, simultaneous
owner loss, hostile handles, arbitrary process trees, mapped views, recovery,
and cleanup authority remain unresolved.

No runtime or package surface changes. No production subprocess, native API,
cache mutation, dependency, workflow, permission, or hosted allocation is
added. No hosted check is added. Windows is not admitted.

## Revisit criteria

Revisit Windows admission only after a design supplies trusted root ownership,
explicit hard-link policy, use-time identity and link-count validation,
generation provenance, failure-safe launch and recovery behavior, typed
receipts, and independent-host evidence without expanding essential CI merely
to repeat this bounded observation.

## References

- [Microsoft: Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Microsoft: `CreateHardLinkW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createhardlinkw)
- [Microsoft: `BY_HANDLE_FILE_INFORMATION`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `DeleteFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-deletefilew)
- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [RFC-0165](../rfcs/0165-probe-windows-hard-link-alias-non-exclusion.md)
