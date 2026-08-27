# Windows cache-cleanup child-owned share-delete handshake

- **Status:** Accepted current-host feasibility evidence; Windows is not admitted
- **Milestone:** M155
- **Date:** 2026-08-28
- **Baseline:** M154's direct native sharing-violation probe

## Decision

Retain one Windows-only, test-only child-owned blocker with a fixed pipe
handshake. It verifies that a distinct live process can hold M153's exact
no-delete-share directory handle, cause the unchanged M154 native rename child
to report false/32, close on one fixed release byte, and acknowledge closure
before the identical rename returns true/0. This is ordered current-host
evidence, not cleanup authority or platform admission.

## Why ownership and acknowledgement matter

M154 directly captures the native sharing violation while the pytest process
owns the blocker. Microsoft states that a handle's share options remain in
effect until close regardless of process context. M155 exercises that statement
with the blocker owned solely by a distinct process and makes both acquisition
and release observable without sleeps.

The first metadata-only prototype omitted delete sharing but requested desired
access zero. The current host allowed the rename. No exclusion claim relies on
that attempt. The accepted child instead uses M153's exact
`FILE_LIST_DIRECTORY | FILE_READ_ATTRIBUTES | SYNCHRONIZE` mask, demonstrating
that the share flags alone are not treated as sufficient evidence.

## Test-only contract

`tests/fixtures/windows_share_delete_blocker_child.py`:

1. runs only on Windows as a fixed repository-owned script;
2. accepts no argument, path, command, or environment-selected behavior;
3. opens only relative `live` with M153's exact access mask, read/write sharing,
   and no delete sharing;
4. supplies `NULL` security attributes so the native directory handle is not
   inheritable;
5. emits one canonical bounded `ready` document and reads exactly one byte;
6. closes the handle in `finally`, even for a wrong or closed control channel;
   and
7. emits one canonical bounded `closed` document only after successful close
   and the exact fixed one-byte release token.

`tests/integration/test_windows_cache_cleanup_child_owned_blocker_probe.py`:

1. creates ordinary `live` and candidate entries beneath one pytest-owned root,
   binds that root to handle-reported NTFS, and closes the parent root handle;
2. starts the exact current interpreter directly with `-I -B`, the fixed
   blocker, explicit pipes, `shell=False`, `close_fds=True`, and the trusted
   temporary root as working directory;
3. reads at most 128 bytes for readiness through a daemon reader with a bounded
   queue wait, killing and waiting for the child on timeout;
4. requires exact-schema `ready` and confirms that the blocker remains alive;
5. runs M154's unchanged isolated rename child and requires false/error 32,
   unchanged namespace/content, and a still-live blocker;
6. writes only the fixed one-byte release token, waits with a bound, and
   requires child exit zero, exact-schema `closed`, empty stderr, and no extra
   stdout;
7. runs the identical rename child and requires true/code zero; and
8. closes all subprocess streams and preserves the unchanged candidate under
   ordinary `displaced`.

The direct pipe reads are safe only because the child contract emits two tiny
bounded lines and no other output. This fixture does not generalize direct pipe
reads to unbounded subprocesses. Both new modules remain excluded from the
wheel.

## Executed evidence

On the current Windows CPython 3.12 host, the fixed child emitted `ready` while
owning the blocker. The separate native rename child returned false/code 32 and
left namespace/content unchanged. The blocker stayed alive until the parent
sent the fixed token, then emitted `closed` and exited zero. The identical
rename child returned true/code zero afterward, with unchanged content under
`displaced`.

## Missing admission evidence

Windows admission still requires:

- controlled concurrent interleavings inside every acquisition and mutation
  boundary, not only ordering before and after a live child-held state;
- duplicated/inherited handle cases, abrupt blocker termination, pipe failure,
  cancellation, timeout, close failure, and restart recovery;
- oplock, lease, share-mode stress, competing descendants, readers, writers,
  publishers, cleanup actors, and general quiescence/exclusion;
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

The accepted handshake is not a concurrent race.

## Scope and CI restraint

M155 adds no runtime subprocess or `ctypes`, adapter, public probe, cache access,
candidate disclosure, cleanup authority, mutation command, dependency, native
extension, compiler requirement, API, workflow, job, permission, or CI
allocation. The fixture participates only in the existing Windows test suite;
no hosted check is added.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: handle inheritance](https://learn.microsoft.com/en-us/windows/win32/sysinfo/handle-inheritance)
- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [M154 native sharing-violation probe](cache-cleanup-windows-native-sharing-violation-probe.md)
