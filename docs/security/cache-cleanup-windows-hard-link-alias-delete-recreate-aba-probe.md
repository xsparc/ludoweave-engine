# Windows hard-link alias delete/recreate ABA probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M185
- **Date:** 2026-08-29
- **Baseline:** M184's hard-link alias deletion non-exclusion boundary

## Decision

Retain one Windows-only, test-only NTFS observation showing pathname-membership
ABA: while M181's matching no-delete-share guardian child remains live, the
parent process can delete a peer hard-link alias and recreate the same alias
pathname for the same file. The exact opened pathname remains protected while
the observed link count changes `2 -> 1 -> 2`. Treat this as a negative
ownership boundary, not root-confined ownership and not cleanup authority.
Windows is not admitted.

## Evidence correction

M183 and M184 used a subprocess guardian. Their mutation actor and guardian
were therefore separate parent and child processes under one principal, not a
single process. M185 records the accurate classification and supersedes M184's
claim that another process was untested. Cross-principal behavior, an
independent third actor, and unrelated process trees remain untested.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_hard_link_alias_delete_recreate_aba_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` and a peer hard-link
   alias;
2. opens both entries through the existing capability helper, retains their
   shared `FILE_ID_INFO`, requires link count two through both, and closes the
   initial handles;
3. starts M181's guardian child with that identity and requires exact `ready`
   while the parent remains the mutation actor;
4. reopens the original and requires rename of its exact pathname to fail with
   Windows sharing error 32;
5. deletes the peer alias, then requires alias absence, guardian liveness,
   unchanged identity and bytes, link count one, and exclusive byte-range
   availability;
6. recreates the same alias pathname with `os.link`, reopens it, and requires
   guardian liveness, the original identity through both handles, link count
   two through both, exact bytes, and range availability through both names;
7. requires a second exact-name rename failure with error 32, performs the
   exact release, and requires exact `closed`;
8. renames the original entry successfully and verifies the displaced entry
   and peer alias retain identity, link count two, exact bytes, and complete
   process, stream, native-handle, and range cleanup.

The probe uses no retry or sleep. It reuses the accepted helpers and fixture;
it adds no native declaration, production import, environment-derived control
input, shell, network access, or inherited handle.

## Security consequence

Identity match, guardian liveness, and exact-name protection do not freeze the
file's link-set membership. On the observed host, the same peer pathname can
disappear and reappear for the same object while the original handle's link
count falls to one and returns to two. A one-link observation is a transient
sample and cannot independently authorize cleanup.

A future design must decide which roots are trusted, whether multiple-link
history is acceptable, when identity and link count are revalidated, how an
ABA change fails closed, and which typed receipt records that refusal. M185
does not define those policies or imply that enumeration would be race-free.

This is a two-process, same-principal result. It does not establish behavior
across principals, an independent third mutation actor, controlled concurrent
racing, hard-link enumeration, authenticated parent directories, POSIX-delete
flags, cross-volume behavior, ReFS, SMB, other drivers, Windows versions, or
independent hosts. File-ID reuse, durable generation provenance, failed launch,
simultaneous owner loss, hostile handles, mapped views, recovery, and cleanup
authority remain unresolved.

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

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `CreateHardLinkW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createhardlinkw)
- [Microsoft: `DeleteFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-deletefilew)
- [Microsoft: Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `os.link`](https://docs.python.org/3/library/os.html#os.link)
- [Python: `os.remove` and `os.unlink`](https://docs.python.org/3/library/os.html#os.remove)
- [RFC-0168](../rfcs/0168-probe-windows-hard-link-alias-delete-recreate-aba.md)
