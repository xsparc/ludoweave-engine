# Windows cache-cleanup inherited-handle retention probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M163
- **Date:** 2026-08-28
- **Baseline:** M162's duplicated-handle retention probe

## Decision

Retain one Windows-only, test-only inherited-handle observation. A parent opens
a no-delete-share directory handle, passes only that handle through an
explicit handle list, and immediately restores it to noninheritable. Closing
the parent handle leaves the identical native rename false/error 32 until the
fixed child closes its inherited handle. The final rename returns true/code
zero with content preserved. Windows is not admitted.

## Why explicit inheritance matters

M162 keeps both handles in one process. It cannot establish whether Windows
process creation gives the child a reference to the same kernel object or
whether that child reference retains the share-mode denial after the parent
closes its handle.

Python exposes a Windows `STARTUPINFO` explicit handle list and requires
`close_fds=True` for that list. Microsoft recommends explicit handle lists
when inheritance is necessary so unrelated handles are not inherited. The
probe follows that narrow serial pattern and restores the parent's handle
metadata in `finally` immediately after `Popen`.

Python separately warns that temporary inheritability can leak handles during
concurrent process creation. This observation is not a concurrency-safe
inheritance contract and must not be generalized into a runtime policy.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_inherited_handle_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned root,
   binds that root to handle-reported NTFS, and closes the root probe;
2. opens one no-delete-share handle to `live`, builds one `STARTUPINFO`
   explicit handle list containing only that handle, temporarily marks it
   inheritable around fixed child creation, and restores noninheritability;
3. requires bounded exact-schema `ready`, a live child, and M154's unchanged
   native rename false/error 32 with namespace and content unchanged;
4. closes the parent's handle exactly once and requires owned count zero;
5. requires the identical second rename false/error 32 while only the child
   owns the inherited handle and remains live;
6. writes and flushes only fixed byte `!` and closes the parent writer;
7. requires bounded exact-schema `closed`, child exit zero, and both output
   streams at EOF; and
8. requires the identical final rename true/code zero while the candidate is
   preserved under ordinary `displaced`.

The child accepts only one canonical positive decimal handle argument and no
path. It closes that inherited handle exactly once after the fixed token.
Invalid input and native close failures have bounded nonzero exits. The helper
and integration module remain excluded from the wheel.

## Executed evidence

Execution results are recorded only after the live current-host test runs.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings inside acquisition, inheritance,
  process creation, mutation, wait, pipe, cancellation, and close boundaries;
- leak-freedom during concurrent launches, creation failure, invalid inherited
  values, child crash, cross-process duplication/transfer, and partial
  ownership transfer;
- native close failure, nonzero wait, actual graceful-close timeout,
  cancellation, process restart, and durable recovery;
- arbitrary pipe failures, partial or multiple writes, write retry, and Python
  exception-mapping variation;
- oplock, lease, share-mode stress, competing descendants, readers, writers,
  publishers, cleanup actors, and general quiescence/exclusion;
- cross-version, cross-filesystem, cross-driver, alternate-rename, and exact
  native-error variation evidence;
- ancestor substitution, mounted folders, symbolic links, unknown tags,
  hard-link policy, file-ID reuse, pins, and publication interleavings;
- NTFS variation plus ReFS, Dev Drive, removable media, remote shares, and safe
  refusal for every unsupported filesystem;
- crash, disk-full, denial, retry, restore, finalize, and durable recovery;
- an accepted private adapter ABI with bounded backend-neutral errors; and
- candidate, retained-root, policy, trusted-time, durable receipt, and recovery
  designs plus independent installed-host proof.

## Scope and CI restraint

M163 adds no runtime subprocess or `ctypes`, adapter, public probe, cache
access, candidate disclosure, cleanup authority, recovery, mutation command,
dependency, native extension, compiler requirement, API, workflow, job,
permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Microsoft: handle inheritance](https://learn.microsoft.com/en-us/windows/win32/sysinfo/handle-inheritance)
- [Microsoft: creating processes](https://learn.microsoft.com/en-us/windows/win32/procthread/creating-processes)
- [Microsoft: `UpdateProcThreadAttribute`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute)
- [Microsoft: `CloseHandle`](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)
- [M162 duplicated-handle retention probe](cache-cleanup-windows-duplicated-handle-probe.md)
