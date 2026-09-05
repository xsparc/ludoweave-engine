# Windows protected guardian-handoff probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M177
- **Date:** 2026-08-29
- **Baseline:** M175's protected live interval and M176's abrupt settlement

## Decision

Retain one Windows-only, test-only controlled observation showing that a
noninheritable no-delete-share guardian can preserve one coordination identity
through a participant-free interval, admit a later M175 protected participant,
and release while that participant retains namespace protection. The guardian
does not own the byte range. This is not generation authority, crash recovery,
or cleanup authority. Windows is not admitted.

## Why an identity guardian is material but insufficient

Microsoft documents that each `CreateFileW` handle's sharing options remain in
effect until that handle closes. Omitting `FILE_SHARE_DELETE` prevents later
delete-access opens, and delete access includes rename. A compatible retained
handle can therefore preserve M175's no-substitution condition while no shared
`LockFileEx` participant exists.

Namespace continuity and cooperative quiescence are separate. The guardian
requests generic read and read/write sharing without delete sharing, but it
does not call `LockFileEx`. An exclusive byte-range owner must succeed during
the participant-free interval and fail only while a protected participant is
live.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_protected_guardian_handoff_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` beneath an NTFS
   pytest root and retains its `FILE_ID_INFO` identity;
2. opens a private guardian with generic read, read/write sharing without
   delete sharing, null security attributes, reparse rejection, and a
   noninheritable owned handle;
3. with only the guardian live, requires M174 substitution error 32 and exact
   M173 exclusive acquire/release success;
4. starts M175's unchanged protected participant, requires exact `ready`,
   substitution error 32, and exclusive-range error 33, then closes it exactly;
5. during the participant-free interval, requires the guardian to preserve
   substitution refusal while exact exclusive acquire/release succeeds;
6. starts a second unchanged participant and proves a fresh pathname handle
   still observes the original identity;
7. closes the guardian while the second participant remains live and requires
   substitution error 32 plus exclusive-range error 33 to persist;
8. closes the participant, requires exact exclusive acquire/release and M174
   substitution success, then proves the displaced original retains the old
   identity while the replacement differs; and
9. preserves exact bytes and settles every handle, process, stream, and range
   owner, including assertion-failure paths.

The probe adds no fixture. It reuses M175's fixed no-argument,
no-environment-value child byte-for-byte. It uses no sleep or retry.

## Security consequence

The observation narrows M175's zero-participant gap only while a separate
guardian remains live. It shows one exact current-host handoff chain can keep
the same identity continuously protected without treating the guardian as a
quiescence participant.

It is not generation authority and not crash recovery. The probe begins after
the guardian successfully opens a pathname under an already selected test
root. It does not establish trusted placement, protect startup before that
open, recover a crashed guardian, authenticate participants, guarantee complete
admission, or prevent an uncooperative actor from ignoring the range protocol.

Mapped views, multiple guardians, arbitrary termination, filesystem/driver
variation, durable generation issuance and retention, revalidation through
mutation, fail-closed policy, typed receipts, cleanup authority, and
independent hosts remain unresolved. Windows is not admitted.

## Scope and CI restraint

M177 adds no runtime subprocess or `ctypes`, adapter, guardian or lock API,
public probe, cache access, candidate disclosure, cleanup authority, mutation
command, dependency, native extension, compiler requirement, workflow, job,
permission, or CI allocation. The existing Windows suite is the only future
hosted execution path; no hosted check is added.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [Microsoft: `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [M147 cleanup threat model](cache-cleanup-threat-model.md)
- [M175 live substitution-exclusion probe](cache-cleanup-windows-cooperative-lock-live-substitution-exclusion-probe.md)
- [M176 abrupt-settlement probe](cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe.md)
