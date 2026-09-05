# Windows live coordination-substitution exclusion probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M175
- **Date:** 2026-08-29
- **Baseline:** M174's live pathname-substitution identity split

## Decision

Retain one Windows-only, test-only controlled observation showing that multiple
shared coordination-lock participants which omit delete sharing prevent M174's
rename/replacement while any such participant remains live. Preserve the same
cooperative exclusive-range refusal. Also retain the exact counter-boundary:
substitution succeeds after the final protected participant closes. This is not
cleanup authority. Windows is not admitted.

## Why live exclusion is insufficient but material

Microsoft documents that `CreateFileW` sharing options remain in force until
the handle closes. Without `FILE_SHARE_DELETE`, another open cannot request
delete access, and delete access includes rename. `LockFileEx` separately
provides shared/exclusive coordination over one file handle and range.

Combining the two can protect one live coordination identity from M174's
rename/replacement attack while preserving cooperative quiescence observation.
It cannot preserve identity when no protected participant exists. The live
window and the generation-lifecycle problem must remain separate claims.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_cooperative_lock_live_substitution_exclusion_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` beneath an NTFS
   pytest root and retains its `FILE_ID_INFO` identity;
2. starts two fixed isolated children that open only that file with generic
   read, read/write sharing without delete sharing, null security attributes,
   and noninheritable handles;
3. requires both children to hold overlapping shared fail-immediate locks over
   byte zero/length one and emit exact bounded `ready`;
4. runs M174's unchanged substitution child and requires exact
   `rename_failed`/32 while both participants remain live;
5. requires M173's unchanged exclusive request to fail with error 33;
6. closes one child exactly and requires the same substitution and exclusive-
   lock refusals while the other remains live;
7. closes the final child, acquires/releases exact exclusive ownership, then
   requires M174's unchanged substitution child to report `substituted`/0;
8. proves the displaced original retains the captured identity and the
   replacement differs; and
9. preserves both exact byte sequences and settles every handle, process,
   stream, and parent lock owner.

`tests/fixtures/windows_coordination_lock_protected_participant_child.py`
accepts no argument, path, command, or environment value. It owns only the
fixed ordinary file handle and range lock. It never returns a path, payload, or
native handle.

## Executed evidence

On the current Windows CPython 3.12 NTFS host, two protected participants hold
the shared range concurrently. M174's native rename returns error 32 while both
are live and again after one closes. M173's exclusive range request returns
error 33 in both ownership states. After the final protected participant
unlocks and closes, exact exclusive acquire/release succeeds and the unchanged
substitution child renames and replaces the file. The displaced identity equals
the retained original and the replacement differs. Both contents remain exact
and every observed owner settles.

## Security consequence

Omitting delete sharing protects the coordination identity only across a
continuous live-ownership interval. It does not authenticate a later pathname
resolution or bind independently starting processes to a stable generation.

A future design must still define trusted root and coordination identities,
generation issuance and retention, process admission, revalidation around
mutation, startup/shutdown and crash recovery, fail-closed policy, and typed
receipts. M175 does not establish uncooperative-process exclusion, mapped-view
coverage, abrupt-exit settlement, filesystem variation, independent-host
behavior, or cleanup authority. Windows is not admitted.

## Scope and CI restraint

M175 adds no runtime subprocess or `ctypes`, adapter, lock API, public probe,
cache access, candidate disclosure, cleanup authority, mutation command,
dependency, native extension, compiler requirement, workflow, job,
permission, or CI allocation. The fixture participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [M147 cleanup threat model](cache-cleanup-threat-model.md)
- [M174 substitution probe](cache-cleanup-windows-cooperative-lock-substitution-probe.md)
