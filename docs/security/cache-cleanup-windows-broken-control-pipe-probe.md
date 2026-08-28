# Windows cache-cleanup blocker broken-control-pipe probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M159
- **Date:** 2026-08-28
- **Baseline:** M158's blocker invalid-control-token probe

## Decision

Retain one Windows-only, test-only fixed late release byte probe. It verifies
false/error 32 while M155's unchanged blocker child owns the no-delete-share
directory handle, kills and boundedly reaps that owner, requires
one direct test-only `WriteFile` call to report false/error 232 with zero bytes,
explicitly closes the parent writer, and requires the identical native rename
child to return true/code zero with content preserved. This is current-host
evidence, not a recovery contract, cleanup authority, or platform admission.

## Why the broken write matters

M156 orders abrupt owner termination and a subsequent rename. M158 observes a
fixed invalid byte while the child is still alive. Neither observes the
control-plane sender after the blocker has terminated and its inherited pipe
reader is closed.

Microsoft's `WriteFile` page describes `ERROR_BROKEN_PIPE` after an anonymous-
pipe reader closes, while its system-error table defines `ERROR_NO_DATA` 232 as
"the pipe is being closed." Python documents `BrokenPipeError` for the closed-
reader condition. Initial live probes instead observed `OSError(errno.EINVAL)`
through CPython's buffered stream and exact native false/error 232 with zero
bytes on this host. M159 records only the native current-host result. It waits
for process termination and output EOF before one direct native write and
performs no retry or timing sleep.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_broken_control_pipe_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned root,
   binds that root to handle-reported NTFS, and closes the parent root handle;
2. starts M155's exact child under the current interpreter with `-I -B`,
   explicit pipes, `shell=False`, `close_fds=True`, and the trusted temporary
   root as working directory;
3. requires bounded exact-schema `ready` and a live blocker;
4. runs M154's unchanged isolated rename child and requires false/error 32,
   unchanged namespace/content, and a still-live blocker;
5. kills the child exactly once and completes M155's bounded process wait with
   a nonzero result before any control write;
6. requires output EOF, attempts exactly one fixed late release byte through
   test-only `WriteFile`, and requires false/error 232 with zero bytes;
7. explicitly closes and confirms the parent writer;
8. requires empty stdout and stderr, runs the identical rename child once, and
   requires true/code zero; and
9. closes all subprocess streams and preserves the candidate under ordinary
   `displaced`.

The new module remains excluded from the wheel.

## Executed evidence

Execution results are recorded only after the live current-host test runs.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings inside every acquisition, mutation,
  pipe, cancellation, termination, and close boundary;
- arbitrary pipe failures, Python exception-mapping variation, write retry,
  readiness/termination timeout, native close failure, cancellation, process
  restart, and durable restart recovery;
- duplicated/inherited handles, oplock, lease, share-mode stress, competing
  descendants, readers, writers, publishers, cleanup actors, and general
  quiescence/exclusion;
- cross-version, cross-filesystem, cross-driver, alternate-rename, and exact
  native-error variation evidence;
- ancestor substitution, mounted folders, symbolic links, unknown tags, hard-
  link policy, file-ID reuse, pins, and publication interleavings;
- NTFS variation plus ReFS, Dev Drive, removable media, remote shares, and safe
  refusal for every unsupported filesystem;
- crash, disk-full, denial, retry, restore, finalize, and durable recovery;
- an accepted private adapter ABI with bounded backend-neutral errors; and
- candidate, retained-root, policy, trusted-time, durable receipt, and recovery
  designs plus independent installed-host proof.

This single fixed late write is not a recovery contract.

## Scope and CI restraint

M159 adds no runtime subprocess or `ctypes`, helper, adapter, public probe,
cache access, candidate disclosure, cleanup authority, recovery, mutation
command, dependency, native extension, compiler requirement, API, workflow,
job, permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Microsoft: `WriteFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile)
- [Microsoft: system error codes 0-499](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-)
- [Python: `BrokenPipeError`](https://docs.python.org/3/library/exceptions.html#BrokenPipeError)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [M158 invalid-control-token probe](cache-cleanup-windows-invalid-control-token-probe.md)
