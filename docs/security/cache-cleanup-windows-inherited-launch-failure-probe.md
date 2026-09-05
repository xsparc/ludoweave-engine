# Windows cache-cleanup inherited-handle launch-failure probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M164
- **Date:** 2026-08-28
- **Baseline:** M163's inherited-handle retention probe

## Decision

Retain one Windows-only, test-only rollback observation around a real process-
creation failure. A parent temporarily marks one no-delete-share directory
handle inheritable, lists only that handle for a fixed missing executable, and
restores it to noninheritable when `Popen` raises `FileNotFoundError`. The
parent keeps ownership and false/error 32 denial until explicit close, after
which the identical native rename returns true/code zero with content
preserved. Windows is not admitted.

## Why launch failure matters

M163 proves successful explicit inheritance and acknowledged child close. Its
spawn helper also defensively reaps a created child if restoring
noninheritability fails, but that path is not behaviorally injected.

Python requires explicit-list handles to be temporarily inheritable during
`Popen`. A launch exception therefore creates a distinct rollback boundary:
the parent must restore the original noninheritability state even though no
child/process owner is returned. This probe uses a fixed absent executable to
exercise an actual current-host process-creation failure rather than a mocked
exception.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_inherited_launch_failure_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned root,
   binds that root to handle-reported NTFS, and closes the root probe;
2. proves the fixed missing executable is absent and opens one noninheritable
   no-delete-share handle to `live`;
3. builds one `STARTUPINFO` explicit handle list containing only that handle,
   marks it inheritable, and calls the fixed missing executable with
   `close_fds=True`, `shell=False`, explicit executable selection, trusted
   working directory, and `DEVNULL` standard streams;
4. requires exact `FileNotFoundError`, errno `ENOENT`, Windows error 2, no
   returned process, and immediate restoration to noninheritable;
5. requires parent owned count one, the missing path still absent, and M154's
   unchanged native rename false/error 32 with namespace/content unchanged;
6. closes the parent's handle exactly once and requires owned count zero; and
7. requires the identical final rename true/code zero while the candidate is
   preserved beneath ordinary `displaced`.

If the supposedly missing executable unexpectedly starts, the harness closes
and reaps it before failing. If restoration fails after that unexpected spawn,
the process is likewise closed and reaped. No accepted execution creates a
child. The integration module remains excluded from the wheel.

## Executed evidence

Execution results are recorded only after the live current-host test runs.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings inside acquisition, inheritance,
  process creation, mutation, wait, pipe, cancellation, and close boundaries;
- restoration-failure injection, leak-freedom during concurrent launches,
  invalid inherited values, child crash, cross-process duplication/transfer,
  and partial ownership transfer;
- other real process-creation failures, native close failure, nonzero wait,
  actual graceful-close timeout, cancellation, process restart, and durable
  recovery;
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

This is one real process-creation failure, not restoration-failure injection
and not a concurrency-safe inheritance contract.

## Scope and CI restraint

M164 adds no runtime subprocess or `ctypes`, adapter, public probe, cache
access, candidate disclosure, cleanup authority, recovery, mutation command,
dependency, native extension, compiler requirement, API, workflow, job,
permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Python: Windows subprocess startup information](https://docs.python.org/3/library/subprocess.html#windows-popen-helpers)
- [Microsoft: `CreateProcessW`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [Microsoft: creating processes](https://learn.microsoft.com/en-us/windows/win32/procthread/creating-processes)
- [Microsoft: handle inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [M163 inherited-handle retention probe](cache-cleanup-windows-inherited-handle-probe.md)
