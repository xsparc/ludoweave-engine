# Windows guardian abrupt-handoff probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M178
- **Date:** 2026-08-29
- **Baseline:** M177's graceful protected guardian handoff

## Decision

Retain one Windows-only, test-only controlled observation showing that abrupt
guardian process loss after bounded process wait preserves namespace and range
protection when an M175 protected participant is already live on the same
coordination identity. This is not crash recovery, generation authority, or
cleanup authority. Windows is not admitted.

## Why abrupt handoff is material but insufficient

Microsoft documents that each `CreateFileW` handle's sharing options remain in
effect until that handle closes regardless of process context. The guardian's
no-delete-share handle and the participant's independently opened compatible
handle therefore protect the same identity during their overlap.

`TerminateProcess` is asynchronous. The observation is made only after M176's
bounded process wait returns a nonzero abrupt exit. The surviving participant
owns both its no-delete-share handle and its shared `LockFileEx` range; the
guardian owns no range. Continued substitution error 32 and exclusive-range
error 33 therefore belong to the survivor rather than to delayed guardian
range settlement.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_guardian_abrupt_handoff_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` beneath an NTFS
   pytest root and retains its `FILE_ID_INFO` identity;
2. starts one fixed isolated guardian child which opens only that file for
   generic read with read/write sharing without delete sharing, uses null
   security attributes, opens and rejects final-component reparse identity,
   proves the handle noninheritable, takes no range lock, and emits exact
   versioned events;
3. with only the guardian live, requires M174 substitution error 32 while
   exact M173 exclusive acquire/release succeeds;
4. starts M175's unchanged protected participant and requires exact `ready`,
   the original identity, substitution error 32, and exclusive-range error 33;
5. kills and boundedly waits for the guardian through M176's helper, requires
   a nonzero abrupt exit with no trailing output, then proves the participant
   remains live on the original identity with both refusals intact;
6. closes the participant exactly, requires exclusive acquire/release and M174
   substitution success, and proves the displaced original retains the old
   identity while the replacement differs; and
7. preserves exact bytes and settles every handle, process, stream, and range
   owner, including assertion-failure paths.

The fixed child accepts no path, argument, or environment-selected value. The
probe uses no retry or sleep.

## Security consequence

The observation narrows one M177 failure edge: once a protected participant is
already live on the retained identity, abruptly losing and reaping the
guardian does not remove protection owned independently by that participant.

It is not crash recovery and not generation authority. The probe does not
protect the interval before the guardian opens, start a replacement guardian,
survive an interval with no owner, authenticate participants, guarantee
complete admission, or reconstruct durable state. A guardian crash without a
surviving compatible owner still releases its protection.

Multiple guardians, hostile prior handles, arbitrary process trees, mapped
views, filesystem/driver variation, durable generation issuance and retention,
use-time revalidation, fail-closed policy, typed receipts, cleanup authority,
and independent hosts remain unresolved. Windows is not admitted.

## Scope and CI restraint

M178 adds no runtime subprocess or `ctypes`, adapter, guardian or lock API,
public probe, cache access, candidate disclosure, cleanup authority, mutation
command, dependency, native extension, compiler requirement, workflow, job,
permission, or CI allocation. The existing Windows suite is the only future
hosted execution path; no hosted check is added.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft: `WaitForSingleObject`](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [M176 abrupt-settlement probe](cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe.md)
- [M177 graceful guardian handoff](cache-cleanup-windows-protected-guardian-handoff-probe.md)
