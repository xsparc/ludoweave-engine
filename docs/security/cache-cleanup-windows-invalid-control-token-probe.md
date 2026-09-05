# Windows cache-cleanup blocker invalid-control-token probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M158
- **Date:** 2026-08-28
- **Baseline:** M157's blocker control-pipe EOF probe

## Decision

Retain one Windows-only, test-only fixed invalid control token probe. It
verifies false/error 32 while M155's unchanged blocker child owns the no-delete-
share directory handle, writes and flushes exactly one fixed `?` byte, closes
the parent control writer, waits with a fixed bound for fixture exit 4, observes
no closed acknowledgement, and requires the identical native rename child to
return true/code zero with content preserved. This is current-host evidence,
not cleanup authority or platform admission.

## Why the fixed invalid token matters

M155 orders acquisition and valid-token close. M157 closes the parent writer
without sending data and therefore exercises EOF. The unchanged helper also
has an existing branch for one received byte that differs from its release
token, but that path had not been distinguished from EOF while the child owned
the blocking native handle.

Microsoft documents that anonymous pipes are byte streams and that write
operations deliver a requested byte count or fail. Python's binary buffered
streams accept bytes, expose an explicit buffer flush, and make close
idempotent. The fixed test writes only one known byte after exact readiness,
flushes and closes the writer, and performs no retry or timing sleep.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_invalid_control_token_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned root,
   binds that root to handle-reported NTFS, and closes the parent root handle;
2. starts M155's exact child under the current interpreter with `-I -B`,
   explicit pipes, `shell=False`, `close_fds=True`, and the trusted temporary
   root as working directory;
3. requires bounded exact-schema `ready` and a live blocker;
4. runs M154's unchanged isolated rename child and requires false/error 32,
   unchanged namespace/content, and a still-live blocker;
5. writes exactly one repository-fixed invalid byte, requires the buffered
   write to accept it, flushes, closes only `Popen.stdin`, and confirms that
   stream is closed;
6. waits with M155's existing timeout and requires exact fixture exit 4, EOF
   with no `closed` acknowledgement, and empty stderr;
7. runs the identical rename child once and requires true/code zero; and
8. closes all subprocess streams and preserves the candidate under ordinary
   `displaced`.

The post-wait pipe reads are bounded and safe because the fixed child has
already exited and its only possible stdout documents are tiny and schema-
bounded. The new module remains excluded from the wheel.

## Executed evidence

Execution results are recorded only after the live current-host test runs.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings inside every acquisition, mutation,
  pipe, cancellation, termination, and close boundary;
- arbitrary malformed input, partial and multiple writes, broken-pipe writes,
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

This single fixed invalid control token is not arbitrary malformed input.

## Scope and CI restraint

M158 adds no runtime subprocess or `ctypes`, helper, adapter, public probe,
cache access, candidate disclosure, cleanup authority, recovery, mutation
command, dependency, native extension, compiler requirement, API, workflow,
job, permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: pipe handle inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance)
- [Python: `io`](https://docs.python.org/3/library/io.html)
- [M157 control-pipe EOF probe](cache-cleanup-windows-control-pipe-eof-probe.md)
