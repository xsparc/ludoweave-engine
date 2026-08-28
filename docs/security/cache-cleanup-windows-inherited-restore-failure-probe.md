# Windows cache-cleanup inherited-handle restoration-failure probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M165
- **Date:** 2026-08-29
- **Baseline:** M164's inherited-launch failure probe

## Decision

Retain one Windows-only, test-only ownership observation around an injected
restoration failure after successful explicit handle inheritance. M163's
unchanged helper must close and reap its already-created child before
re-raising the identical injected error. The caller then explicitly repairs
the still-inheritable parent handle, retains false/error 32 denial until parent
close, and observes true/code zero only afterward. Windows is not admitted.

## Why restoration failure matters

M163's launch helper temporarily makes one blocker handle inheritable, creates
the fixed child, and restores noninheritability in `finally`. It already has a
defensive branch that closes the process when restoration raises. M164 proves
a real missing-executable launch failure, but that path creates no child and
restoration succeeds.

A failure after successful process creation crosses two ownership boundaries:
the child exists and may own the inherited handle, while the parent's handle
may remain inheritable. Reaping the child is necessary but does not repair the
parent flag. M165 isolates both duties without mutating the accepted helper or
claiming that a deterministic test injection is a real kernel failure.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_inherited_restore_failure_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned
   root, binds that root to handle-reported NTFS, and closes the root probe;
2. opens one noninheritable no-delete-share handle to `live` and captures the
   original setter and close/reap function;
3. delegates the initial inheritable transition to the real setter, permits
   M163's real fixed child launch, and injects one fixed exception before the
   first restore transition for that exact handle;
4. observes the close/reap delegation and requires the identical exception,
   no returned process, exactly one terminal child, and all owned child pipe
   streams closed;
5. requires the parent handle still inheritable and still owned exactly once,
   then uses the captured original setter in `finally` to repair it;
6. requires repaired noninheritability and M154's unchanged native rename
   false/error 32 with namespace/content unchanged while the parent owns the
   handle; and
7. closes the parent handle exactly once and requires owned count zero plus the
   identical final rename true/code zero with content preserved beneath
   ordinary `displaced`.

The injected restoration failure is not a real native restoration failure.
The test does not inject `Popen`, replace the native close/reap implementation,
run concurrent launches, or leave an inheritable handle behind. The integration
module remains excluded from the wheel.

## Executed evidence

Execution results are recorded only after the live current-host test runs.

## Missing admission evidence

Windows admission still requires:

- a safely reproducible real native restoration failure and exact native error
  mapping without invalidating or abandoning owned handles;
- controlled concurrent interleavings and leak-freedom during simultaneous
  inheritance, creation, restoration, cancellation, wait, and close;
- invalid inherited values, child crash, cross-process duplication/transfer,
  partial ownership transfer, and native close failure;
- other process-creation failures, nonzero wait, actual graceful-close timeout,
  cancellation, process restart, and durable recovery;
- arbitrary pipe failures, partial or multiple writes, retry, and Python
  exception-mapping variation;
- oplock, lease, share-mode stress, competing descendants, readers, writers,
  publishers, cleanup actors, and general quiescence/exclusion;
- cross-version, cross-filesystem, cross-driver, alternate-rename, and exact
  native-error variation evidence;
- NTFS variation plus ReFS, Dev Drive, removable media, remote shares, and safe
  refusal for every unsupported filesystem;
- crash, disk-full, denial, retry, restore, finalize, and durable recovery;
- an accepted private adapter ABI with bounded backend-neutral errors; and
- candidate, retained-root, policy, trusted-time, durable receipt, and recovery
  designs plus independent installed-host proof.

This is one injected restoration-failure ownership observation, not a real
native restoration failure and not a concurrency-safe inheritance contract.

## Scope and CI restraint

M165 adds no runtime subprocess or `ctypes`, adapter, public probe, cache
access, candidate disclosure, cleanup authority, recovery, mutation command,
dependency, native extension, compiler requirement, API, workflow, job,
permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Python: inheritance of file descriptors and handles](https://docs.python.org/3/library/os.html#inheritance-of-file-descriptors)
- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Microsoft: `SetHandleInformation`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-sethandleinformation)
- [Microsoft: `CloseHandle`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)
- [M164 inherited-launch failure probe](cache-cleanup-windows-inherited-launch-failure-probe.md)
