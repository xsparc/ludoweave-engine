# RFC-0138: probe a child-owned Windows share-delete handshake

- **Status:** Accepted
- **Milestone:** M155
- **Date:** 2026-08-28

## Summary

Add one test-only NTFS fixture in which a fixed isolated child owns M153's
no-delete-share directory handle. Use bounded exact-schema pipe
acknowledgements to order a separate native rename denial, explicit child close,
and the identical post-close success. Preserve the no-admission decision and
add no runtime or CI surface.

## Context

M153 and M154 retain the blocking directory handle in the pytest process while
a child attempts the rename. They establish a process boundary for the rename,
but they do not show that the exclusion remains effective when a distinct
process owns and closes the blocker.

Microsoft documents that each handle's share options remain effective until
that handle closes regardless of process context. It also documents that
omitting `FILE_SHARE_DELETE` prevents another process from requesting delete
access, which includes rename. A fixed cross-process handshake can test that
ownership transition without a timing race.

## Decision

Accept the [Windows child-owned share-delete
handshake](../security/cache-cleanup-windows-child-owned-share-delete-handshake.md)
as current-host, test-only feasibility evidence.

The blocker child must open only the relative `live` directory with M153's exact
`FILE_LIST_DIRECTORY | FILE_READ_ATTRIBUTES | SYNCHRONIZE` access and read/write
sharing without delete sharing. It must use a non-inheritable native handle,
emit one bounded canonical `ready` document, read exactly one fixed release
byte, close the handle in `finally`, and emit one bounded canonical `closed`
document.

The parent must launch the fixed helper with its exact interpreter under
`-I -B`, explicit pipes, `shell=False`, and `close_fds=True`. Readiness must be
bounded independently, and every failure path must terminate, wait for, and
close the child. After `ready`, the unchanged M154 rename helper must return
false/32 while the blocker child remains alive. Only then may the parent send
the fixed release byte. After `closed` and child exit zero, the identical rename
helper must return true/0 and preserve the candidate under `displaced`.

Do not use `-c`, caller arguments, environment-selected behavior, command or
path input over stdin, sleeps, polling, inherited native handles, runtime
subprocess or `ctypes`, a platform adapter, public capability value, cleanup
authority, dependency, workflow, or Windows admission.

## Consequences

The current host now observes one explicitly synchronized case where another
live process owns the blocking handle, a separate child receives native error
32, and the rename succeeds only after the owner acknowledges close. The
control channel carries one fixed byte rather than code, paths, or commands.

An initial metadata-only prototype requested desired access zero and did not
block the rename on this host. The accepted fixture therefore preserves M153's
exact nonzero directory access mask and does not infer exclusion from share
flags alone.

This ordered handshake is not a concurrent race, a selected interleaving inside
`CreateFileW`, `MoveFileExW`, or `CloseHandle`, general cross-process exclusion,
quiescence, an oplock protocol, duplicated-handle behavior, crash recovery, or
platform admission. Other processes, descendants, filesystems, drivers,
recovery, policy, receipts, and independent hosts remain open.

Windows is not admitted.

## Alternatives considered

- Use sleeps to guess when the child acquired the handle. Rejected because a
  fixed readiness acknowledgement supplies a deterministic ordering boundary.
- Pass a path or command to the blocker. Rejected because the fixture requires
  only fixed repository-owned names and one fixed release token.
- Use a metadata-only handle. Rejected because the initial current-host attempt
  did not block the rename and would not reproduce M153's access contract.
- Add a dedicated hosted job. Rejected because the existing Windows suite can
  execute this test after the unpublished stack is safely integrated.
- Implement a runtime coordination adapter. Rejected because the wider
  admission, recovery, and policy requirements remain incomplete.

## Validation

Focused validation must prove the exact blocker access/share mask, fixed
isolated child, bounded readiness, child liveness during false/32, unchanged
denial state, fixed one-byte release, acknowledged deterministic close, child
exit zero, identical true/0 retry, content preservation, timeout cleanup, and
closed streams. Architecture tests must preserve M154, runtime, examples,
scripts, dependencies, workflows, and wheel contents. Supported-Python, full
regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [`CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Windows handle inheritance](https://learn.microsoft.com/en-us/windows/win32/sysinfo/handle-inheritance)
- [`MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [Python `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [RFC-0137](0137-probe-windows-native-sharing-violation.md)
