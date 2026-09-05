# Windows zero-owner guardian restart-boundary probe

- **Status:** Accepted current-host bounded capability evidence; Windows is not admitted
- **Milestone:** M180
- **Date:** 2026-08-29
- **Baseline:** M179's overlapping guardian rotation

## Decision

Retain one Windows-only, test-only controlled probe with two observations after
an unchanged guardian is abruptly terminated and boundedly reaped. A later
guardian reacquires the original identity when no mutation occurs. When the
pathname is substituted during the zero-owner interval, a later guardian
instead protects the replacement identity. This is a restart boundary, not
crash recovery and not generation authority. Windows is not admitted.

## Why the zero-owner interval is material but insufficient

M179 avoids a protection gap by starting the second guardian before losing the
first. M180 deliberately removes that overlap. M176's process wait establishes
that the first guardian has settled before any exposed-state observation or
later launch.

In the benign case, a fresh `FILE_ID_INFO` observation shows that the current
pathname was unchanged before the second guardian opens it. This is an
observation, not proof that the interval was protected. In the substitution
case, M174 renames the original and creates a distinct object at the same
pathname. The later guardian's no-delete-share handle applies to that distinct
replacement. It cannot infer or restore the displaced generation.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_zero_owner_guardian_restart_boundary_probe.py`:

1. creates M173's exact ordinary `live/coordination.lock` beneath an NTFS
   pytest root and retains its original `FILE_ID_INFO` and bytes;
2. starts M178's unchanged guardian, requires exact `ready`, substitution error
   32, and exact exclusive range availability;
3. kills and boundedly waits for that guardian through M176's unchanged helper;
4. in the benign case, observes the exposed pathname still names the original
   identity, starts a second guardian, and requires that identity, substitution
   error 32, and range availability until exact close;
5. after that close, requires M174 substitution success, displaced original
   identity, distinct replacement identity, and exact bytes;
6. in the mutation case, substitutes the pathname before starting the second
   guardian and records the displaced original and replacement identities;
7. requires the later guardian to protect only the replacement identity,
   refuse a second direct rename with sharing error 32, and leave the
   cooperative range available;
8. closes that guardian exactly, requires the same rename to succeed, and
   verifies both moved identities, exact bytes, and complete cleanup.

The probe adds no child fixture. It uses no retry or sleep.

## Security consequence

The two observations close one measurement gap while exposing the architectural
gap. A benign launch can reacquire an unchanged object, but a pathname-only
guardian cannot distinguish an authorized continuation from a substituted
generation. Its successful start is therefore not recovery evidence and cannot
authorize cleanup.

This is not crash recovery, not generation authority, not guardian election,
not trusted placement, not authentication, and not continuity. Simultaneous
loss, failed replacement launch, hostile prior handles, arbitrary process
trees, mapped views, filesystem/driver variation, durable generation issuance
and retention, use-time revalidation, fail-closed policy, typed receipts,
cleanup authority, and independent hosts remain unresolved. Windows is not
admitted.

## Scope and CI restraint

M180 adds no fixture, runtime subprocess or `ctypes`, adapter, guardian or lock
API, public probe, cache access, candidate disclosure, cleanup authority,
mutation command, dependency, native extension, compiler requirement,
workflow, job, permission, or CI allocation. The existing Windows suite is the
only future hosted execution path; no hosted check is added.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [M174 pathname-substitution probe](cache-cleanup-windows-cooperative-lock-substitution-probe.md)
- [M179 overlapping guardian rotation](cache-cleanup-windows-overlapping-guardian-rotation-probe.md)
