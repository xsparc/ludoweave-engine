# RFC-0176: probe Windows alias-mutator invalid-prefix settlement with an open writer

- **Status:** Accepted
- **Milestone:** M193
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that writes and flushes M192's fixed
two-byte `?!` sequence to M186's unchanged independent alias-mutator child
after exact `recreated`, then waits for child settlement while the parent
writer remains open. Require exit 5, no `closed` event, stdout EOF, empty
stderr, and a still-open parent writer after child exit. Close the writer only
after those observations. Preserve the alias, guardian, identity, link-count,
range, rename, and cleanup boundaries. Add no runtime or CI surface.

## Context

M192 proves leading-byte rejection for `?!`, but closes the parent writer
before waiting. That sequence cannot distinguish rejection caused by the
invalid byte from settlement triggered by control-pipe EOF.

Python documents `Popen.wait()` as waiting for child termination and returning
the exit code. Its deadlock warning applies when a child can fill a piped
stdout or stderr before termination. M186's fixed fixture emits the already
consumed `deleted` and `recreated` lines, then emits no further stdout and no
stderr on its invalid-byte path. This bounded-output fixture therefore permits
the parent to wait before draining final EOF for this exact condition.

Microsoft documents anonymous pipes as byte streams and byte-mode pipes as not
preserving write boundaries. Python documents buffered binary `write()` as
accepting bytes or raising and `flush()` as forcing buffered data to the
underlying stream. M186 performs one `read(1)` in its close phase and returns 5
immediately when that byte is not `!`.

## Decision

Accept the [Windows hard-link alias mutator invalid-prefix open-writer
settlement after recreation
probe](../security/cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-open-writer-settlement-after-recreate-probe.md)
as current-host, test-only open-writer settlement evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Start M186's unchanged child and require exact `deleted`. Send the exact
recreate token and require exact `recreated`. Require both children live, the
peer alias present, unchanged shared identity and bytes, link count two, and
byte-range availability through both names.

Write `?!` exactly once, require both bytes accepted, and flush. Require the
parent writer open before a bounded `wait()`. Require exit 5 while the writer
remains open, then require stdout EOF with no `closed` event and empty stderr.
Close the writer only after these observations. Require guardian liveness,
continued alias presence, unchanged identity, bytes and two-link state, range
availability, and persistent rename refusal. Release the guardian exactly,
rename the original, and require complete identity, count, bytes, process,
stream, native-handle, and range cleanup. Use no retry or sleep.

## Consequences

On the observed host, the unchanged fixture settles on the leading invalid byte
without waiting for control-pipe EOF. It leaves the alias present and emits no
close acknowledgement. This isolates the exact invalid-byte branch from the
parent-writer-close condition used in M192.

This does not establish arbitrary malformed input, partial or separate writes,
unbounded output safety, arbitrary wait-before-drain safety, multiple or
inherited writers, authenticated cancellation, rollback policy, or safe cache
cleanup. The wait ordering is justified only by the bounded-output fixture and
the exact already-consumed phase events. A production protocol must use
explicit framing, authenticated authority, bounded I/O, durable intent,
quarantine, idempotency, reconciliation, and typed recovery receipts.

This remains a three-process, same-principal observation under one parent-owned
process tree. It does not establish cross-principal behavior, unrelated
processes or sessions, hostile simultaneous racing, crash consistency, power
loss, or security isolation.

Windows is not admitted. ReFS, SMB, other drivers and Windows versions,
cross-volume behavior, file-ID reuse, durable recovery, and independent-host
proof remain open. No runtime API, adapter, public probe, production subprocess
or `ctypes`, cache access, cleanup authority, dependency, workflow, permission,
or hosted check is added.

## Alternatives considered

- Close the parent writer before waiting. Rejected because M192 already covers
  that condition and cannot isolate invalid-byte settlement from EOF.
- Use `communicate()`. Rejected because it closes stdin and would erase the
  open-writer condition.
- Wait with arbitrary fixture output. Rejected because piped output can fill
  and deadlock; this decision is limited to M186's fixed bounded-output path.
- Change the fixture. Rejected because the milestone observes the established
  child rather than creating a new protocol.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  remains the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove exact phase ordering, one accepted and flushed
two-byte write, parent-writer openness immediately before and after bounded
exit 5, no close acknowledgement, stdout EOF, empty stderr, and writer closure
only after settlement. It must retain initial and final identity/count, alias
presence, bytes, ranges, guardian liveness, rename refusal, post-guardian
rename, and complete cleanup. Architecture tests must preserve M186-M192, the
fixed fixture, runtime, examples, scripts, dependencies, workflows, and the
wheel boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, findings-first, and guarded-cleanup gates remain
required.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: named-pipe type and read modes](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-type-read-and-wait-modes)
- [Microsoft: `WriteFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Python: `io`](https://docs.python.org/3/library/io.html)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [RFC-0175](0175-probe-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-after-recreate.md)
