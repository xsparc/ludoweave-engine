# Windows cache-cleanup blocker control-pipe EOF probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M157
- **Date:** 2026-08-28
- **Baseline:** M156's abrupt blocker-owner termination probe

## Decision

Retain one Windows-only, test-only control-pipe EOF probe. It verifies
false/error 32 while M155's unchanged blocker child owns the no-delete-share
directory handle, closes only the parent control writer without sending a
release byte, waits with a fixed bound for fixture exit 4, observes no closed
acknowledgement, and requires the identical native rename child to return
true/code zero with content preserved. This is current-host evidence, not
cleanup authority or platform admission.

## Why the EOF path matters

M155 orders acquisition and valid-token close. M156 forces process termination
and therefore bypasses the helper's user-mode cleanup. The helper also has an
existing invalid-control path that closes its native handle in `finally` before
returning exit 4, but that path had not been exercised with control-pipe EOF.

Microsoft documents that an anonymous-pipe read returns when all writer handles
close and that a child-inherited writer would prevent EOF. The existing launch
uses Python's explicit `stdin=PIPE` redirection with `close_fds=True`; the
parent closes its writer only after exact readiness and denial. The test has no
control write, retry loop, or timing sleep.

## Test-only contract

`tests/integration/test_windows_cache_cleanup_control_pipe_eof_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned root,
   binds that root to handle-reported NTFS, and closes the parent root handle;
2. starts M155's exact child under the current interpreter with `-I -B`,
   explicit pipes, `shell=False`, `close_fds=True`, and the trusted temporary
   root as working directory;
3. requires bounded exact-schema `ready` and a live blocker;
4. runs M154's unchanged isolated rename child and requires false/error 32,
   unchanged namespace/content, and a still-live blocker;
5. writes no control byte, closes only `Popen.stdin`, and confirms that stream
   is closed;
6. waits with M155's existing timeout and requires exact fixture exit 4, EOF
   with no `closed` acknowledgement, and empty stderr;
7. runs the identical rename child once and requires true/code zero; and
8. closes all subprocess streams and preserves the candidate under ordinary
   `displaced`.

The post-wait pipe reads are bounded and safe because the fixed child has
already exited and its only possible stdout documents are tiny and
schema-bounded. The new module remains excluded from the wheel.

## Executed evidence

Execution results are recorded only after the live current-host test runs.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings inside every acquisition, mutation,
  pipe, cancellation, termination, and close boundary;
- wrong-token input, broken-pipe writes, readiness/termination timeout, native
  close failure, cancellation, process restart, and durable restart recovery;
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

This single EOF-triggered helper path is not arbitrary pipe failure.

## Scope and CI restraint

M157 adds no runtime subprocess or `ctypes`, helper, adapter, public probe,
cache access, candidate disclosure, cleanup authority, recovery, mutation
command, dependency, native extension, compiler requirement, API, workflow,
job, permission, or CI allocation. The probe participates only in the existing
Windows test suite; no hosted check is added.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: pipe handle inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [M156 abrupt-termination probe](cache-cleanup-windows-abrupt-blocker-termination-probe.md)
