# Windows hard-link alias deletion non-exclusion probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M184
- **Date:** 2026-08-29
- **Baseline:** M183's post-admission hard-link creation boundary

## Decision

Retain one Windows-only, test-only NTFS observation showing deletion
non-exclusion: M181's matching no-delete-share guardian does not prevent a
same-user caller from deleting a peer hard-link alias. The exact opened
pathname remains protected while link removal is not excluded. Treat this as
a negative ownership boundary, not root-confined ownership and not cleanup
authority. Windows is not admitted.

## Corrected hypothesis

The initial hypothesis expected peer-alias `Path.unlink` to fail with Windows
sharing error 32 while the guardian remained live. The first focused live run
falsified it: deletion succeeded. The accepted probe preserves that negative
result and then requires the guardian to remain live, the original link count
to fall from two to one, and the exact opened pathname to keep rejecting
rename.

Broad `DeleteFileW` and Python in-use deletion descriptions did not predict
the observed alias-entry behavior for this particular parent/child,
same-principal NTFS setup. The result is deliberately not generalized beyond
the observed host.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_hard_link_alias_deletion_non_exclusion_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` and a peer hard-link
   alias;
2. opens both entries through the existing capability helper, retains their
   shared `FILE_ID_INFO`, requires link count two through both, and closes the
   initial handles;
3. starts M181's guardian with that identity and requires exact `ready` while
   the process remains live;
4. reopens the original and requires rename of its exact pathname to fail with
   Windows sharing error 32;
5. deletes the peer alias with `Path.unlink` while the guardian remains live;
6. requires alias absence, exact original bytes, link count one on the retained
   original handle, exclusive byte-range availability, and another exact-name
   rename failure with error 32;
7. performs the exact release, requires exact `closed`, then reopens the
   original with the same identity and link count one;
8. renames the original entry successfully and verifies the displaced entry
   retains identity, link count one, exact bytes, and complete process,
   stream, native-handle, and range cleanup.

The probe uses no retry or sleep. It reuses the accepted helpers and fixture;
it adds no native declaration, production import, environment-derived control
input, shell, network access, or inherited handle.

## Security consequence

Exact-name protection is not link-set control. On the observed host, the
guardian can keep rejecting rename of the opened coordination name while a
peer entry for the same file is removed. A matching identity and an observed
link count of one after deletion are not root-confined ownership: the system
has neither enumerated every link nor frozen link creation and deletion across
admission and use.

A future design must decide which roots are trusted, whether any multiple-link
history is acceptable, when identity and link count are revalidated, how a
change fails closed, and which typed receipt records that refusal. M184 does
not define those policies or imply that enumeration itself would be race-free.

The deletion actor and guardian are separate parent and child processes under
one principal. This probe does not establish cross-principal behavior, an
independent third mutation actor, unrelated process trees, hard-link
enumeration, authenticated parent directories, POSIX-delete flags,
cross-volume behavior, or coverage of ReFS, SMB, other drivers, or independent
Windows hosts. File-ID reuse, durable generation provenance, failed launch,
simultaneous owner loss, hostile handles, mapped views, recovery, and cleanup
authority remain unresolved. M185 records this corrected process
classification and the combined delete/recreate boundary.

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

- [Microsoft: `DeleteFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-deletefilew)
- [Microsoft: Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `os.remove` and `os.unlink`](https://docs.python.org/3/library/os.html#os.remove)
- [RFC-0167](../rfcs/0167-probe-windows-hard-link-alias-deletion-non-exclusion.md)
