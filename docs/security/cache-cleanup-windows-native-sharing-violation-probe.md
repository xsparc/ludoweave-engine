# Windows cache-cleanup native sharing-violation probe

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M154
- **Date:** 2026-08-28
- **Baseline:** M153's cross-process share-delete exclusion probe

## Decision

Retain one Windows-only, test-only child that invokes `MoveFileExW` directly
and reports its immediate native result through bounded exact-schema JSON. It
verifies error 32 while delete sharing is withheld and success after close. The
result is direct current-host error evidence, not cleanup authority or platform
admission.

## Why direct native capture matters

M153 proves a command-level denial/release pair but intentionally does not
interpret localized stderr or claim an exact underlying error. Microsoft
documents that a failing `MoveFileExW` returns zero and directs the caller to
retrieve `GetLastError` immediately. System error 32 is
`ERROR_SHARING_VIOLATION`.

M154 gives that one native call to a distinct, isolated Python child. The child
captures the error immediately on failure and normalizes success to code zero;
it does not format a system message. Microsoft warns that exact error returns
can vary across operating systems or drivers, so this observation is not a
portable or universal error contract.

## Test-only contract

`tests/fixtures/windows_share_delete_rename_child.py`:

1. runs only on Windows as a fixed repository-owned script;
2. accepts no argument, stdin command, path, or environment-selected behavior;
3. loads only `MoveFileExW` from `kernel32` with retained test-only `ctypes`;
4. uses only relative `live` and `displaced` names with zero move flags;
5. reads the calling thread's last error immediately only when the native call
   returns false; and
6. emits one canonical bounded JSON object containing schema, Boolean success,
   and a non-negative error code.

`tests/integration/test_windows_cache_cleanup_native_error_probe.py`:

1. creates an ordinary `live` directory and candidate below one pytest-owned
   temporary root;
2. opens the root and requires handle-bound NTFS;
3. retains `live` with read and write sharing but without delete sharing;
4. starts the current interpreter directly with `-I -B`, the fixed helper,
   `shell=False`, `close_fds=True`, a trusted working directory, and a bounded
   timeout;
5. requires child exit zero, empty stderr, at most 512 stdout bytes, exact
   fields and types, native false/32, unchanged namespace/content, and both
   native handles still owned;
6. deterministically closes the blocking handle;
7. executes the identical child and requires native true/0;
8. requires `live` absent and an ordinary `displaced` directory containing the
   unchanged candidate; and
9. closes the root and proves zero native handles remain.

The child path is trusted repository test source. No `-c` evaluation, dynamic
module name, caller path, environment value, or content enters the operation or
result. Both modules are excluded from the wheel.

## Executed evidence

On the current Windows CPython 3.12 host, the opened pytest root reports NTFS.
The first isolated native call returns false with code 32 while the no-delete-
share handle is open and leaves the namespace/content unchanged. After explicit
close, the identical child returns true with normalized code zero and the
candidate is unchanged under `displaced`. Both native handles close.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings at every acquisition and mutation
  boundary with explicit synchronization;
- cross-version, cross-filesystem, cross-driver, and alternate native-rename
  error/behavior evidence rather than assuming code 32 universally;
- exclusion or quiescence against competing readers, writers, publishers,
  cleanup actors, descendant activity, and handle duplication/inheritance;
- oplock, lease, share-mode, cancellation, timeout, and close-failure behavior;
- ancestor substitution, mounted folders, symbolic links, unknown tags, hard-
  link policy, file-ID reuse, pins, and publication interleavings;
- NTFS variation plus ReFS, Dev Drive, removable media, remote shares, and safe
  refusal for every unsupported filesystem;
- crash, disk-full, denial, retry, restore, finalize, and durable recovery;
- an accepted private adapter ABI with bounded backend-neutral errors; and
- candidate, retained-root, policy, trusted-time, durable receipt, and recovery
  designs plus independent installed-host proof.

## Scope and CI restraint

M154 adds no runtime subprocess or `ctypes`, adapter, public probe, cache access,
candidate disclosure, cleanup authority, mutation command, dependency, native
extension, compiler requirement, API, workflow, job, permission, or CI
allocation. The fixture participates only in the existing Windows test suite;
no hosted check is added.

## References

- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [Microsoft: `GetLastError`](https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror)
- [Microsoft: `CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [Microsoft: system error codes](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-)
- [Python: command-line isolation](https://docs.python.org/3/using/cmdline.html#cmdoption-I)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [M153 share-delete exclusion probe](cache-cleanup-windows-share-delete-exclusion-probe.md)
