# Windows overlapping guardian-rotation probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M179
- **Date:** 2026-08-29
- **Baseline:** M178's abrupt guardian-to-participant handoff

## Decision

Retain one Windows-only, test-only controlled observation showing that two
compatible guardian processes may overlap on one retained coordination
identity. After abrupt loss and bounded wait of the first guardian, the second
guardian and participant preserve protection; after the participant closes,
the second guardian alone continues namespace protection while the cooperative
range is available. This is overlapping rotation, not guardian restart or
crash recovery. Windows is not admitted.

## Why overlapping rotation is material but insufficient

Microsoft documents that compatible `CreateFileW` requests may coexist and
that each open handle's share options remain in effect until that handle
closes, regardless of process context. Each unchanged M178 guardian therefore
owns an independent no-delete-share handle on the same protected pathname.

The second guardian starts before the first is killed. M176's bounded process
wait completes before survivor assertions. When the participant later closes,
the second guardian owns no `LockFileEx` range, so exclusive range availability
and continued substitution error 32 distinguish range quiescence from retained
namespace protection.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_overlapping_guardian_rotation_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` beneath an NTFS
   pytest root and retains its `FILE_ID_INFO` identity;
2. starts M178's unchanged fixed guardian, requires exact `ready`, original
   identity, substitution error 32, and exact exclusive range availability;
3. starts M175's unchanged participant and requires substitution error 32 plus
   exclusive-range error 33;
4. starts a second unchanged guardian while all three owners overlap, requires
   exact `ready`, and verifies the original identity and both refusals;
5. kills and boundedly waits for the first guardian, then proves the second
   guardian and participant remain live on the original identity with both
   refusals intact;
6. closes the participant exactly and proves the second guardian alone retains
   original identity and substitution error 32 while exact exclusive range
   acquire/release succeeds;
7. closes the second guardian exactly, requires M174 substitution success,
   retains the displaced original identity, and observes a distinct
   replacement identity; and
8. preserves exact bytes and settles every process, stream, handle, and range
   owner, including assertion-failure paths.

The probe adds no new child. It uses no retry or sleep.

## Security consequence

The observation narrows M178's multiple-guardian gap: independently opened,
compatible guardian handles can overlap and transfer sole namespace ownership
without converting the guardian into a range participant.

It is not guardian restart and not crash recovery. Both guardians exist before
the first failure, no guardian is elected or authenticated, no generation is
issued or persisted, and no zero-owner interval is crossed. A startup race,
failed replacement launch, simultaneous owner loss, or later unprotected
interval remains unaddressed.

Hostile prior handles, arbitrary process trees and guardian counts, mapped
views, filesystem/driver variation, durable generation issuance and retention,
use-time revalidation, fail-closed policy, typed receipts, cleanup authority,
and independent hosts remain unresolved. Windows is not admitted.

## Scope and CI restraint

M179 adds no fixture, runtime subprocess or `ctypes`, adapter, guardian or lock
API, public probe, cache access, candidate disclosure, cleanup authority,
mutation command, dependency, native extension, compiler requirement,
workflow, job, permission, or CI allocation. The existing Windows suite is the
only future hosted execution path; no hosted check is added.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [M176 abrupt-settlement probe](cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe.md)
- [M178 abrupt guardian handoff](cache-cleanup-windows-guardian-abrupt-handoff-probe.md)
