# RFC-0179: probe Windows repeated buffered close after delivery failure

- **Status:** Accepted
- **Milestone:** M196
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that reuses M195's exact direct
buffered-close delivery failure after terminal invalid settlement. Require the
first `close()` to raise generic `OSError` and leave the stream closed, then
call `close()` a second time and require it to return `None` without another
delivery attempt or exception. Preserve the alias, guardian, identity,
link-count, range, rename, and cleanup boundaries. Add no runtime or CI
surface.

## Context

M195 proves that direct `close()` attempts delivery of one pending late byte,
raises generic `OSError`, and still leaves the concrete `Popen.stdin` buffered
stream closed. It does not isolate the disposition of a later close call after
that exceptional first close.

Python documents `IOBase.close()` as repeatable: it has no effect if a stream
is already closed and only the first call has an effect. Microsoft documents
that an anonymous-pipe write fails after the corresponding read handle has
closed. The current Windows observation must still avoid promoting CPython's
exception translation or one fixture's stream behavior into a portable
protocol promise.

## Decision

Accept the [Windows hard-link alias mutator repeated buffered-close after
delivery-failure probe](../security/cache-cleanup-windows-hard-link-alias-mutator-repeated-buffered-close-after-delivery-failure-probe.md)
as current-host, test-only repeated-close disposition evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Start M186's unchanged child and require exact `deleted`. Send the exact
recreate token and require exact `recreated`. Require both children live, the
peer alias present, unchanged shared identity and bytes, link count two, and
byte-range availability through both names.

Delegate the terminal invalid-sequence and first-close path byte-for-byte to
M195. That path writes and flushes `?!`, waits for exit 5 and terminal output
while the writer remains open, buffers one late `!`, then requires direct
`close()` to raise generic `OSError` and leave the stream closed. After the
helper returns, require the stream still closed, call `close()` exactly once
more, require the call to return `None`, and require the stream still closed.
The second call does not retry delivery. Make no subtype, `errno`, or Windows
error-code assertion.

Require guardian liveness, continued alias presence, unchanged identity,
bytes and two-link state, range availability, and persistent rename refusal.
Release the guardian exactly, rename the original, and require complete
identity, count, bytes, process, stream, native-handle, and range cleanup. Use
no retry or sleep.

## Consequences

On the observed host, the buffered stream's first close can report delivery
failure and still complete local closure. A second close is a no-op returning
`None`; it does not retry delivery and supplies no acknowledgement of the
pending byte.

This does not establish arbitrary repeated operations on closed streams,
larger or repeated buffered writes, partial raw writes, concurrent commands,
portable exception translation, acknowledgement semantics, authenticated
cancellation, rollback policy, or safe cache cleanup. A production protocol
must use explicit framing, authenticated authority, acknowledgements or typed
receipts, bounded I/O, durable intent, quarantine, idempotency,
reconciliation, and typed recovery behavior.

This remains a three-process, same-principal observation under one
parent-owned process tree. It does not establish cross-principal behavior,
duplicated/inherited writers, unrelated processes or sessions, hostile
simultaneous racing, crash consistency, power loss, or security isolation.

Windows is not admitted. ReFS, SMB, other drivers and Windows versions,
cross-volume behavior, file-ID reuse, durable recovery, and independent-host
proof remain open. No runtime API, adapter, public probe, production
subprocess or `ctypes`, cache access, cleanup authority, dependency, workflow,
permission, or hosted check is added.

## Alternatives considered

- Stop after M195's first failed close. Rejected because it leaves repeated
  local cleanup disposition unobserved.
- Expect another `OSError`. Rejected because Python's documented already-
  closed behavior makes the second call a no-op, not another delivery attempt.
- Write again or call `flush()` after closure. Rejected because operations
  other than repeated close on a closed stream are outside this boundary.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  remains the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove M195 remains byte-for-byte protected, its first
close still raises generic `OSError` and leaves the stream closed, and exactly
one second close returns `None` while the stream remains closed. It must retain
identity/count, alias presence, bytes, ranges, guardian liveness, rename
refusal, post-guardian rename, and complete cleanup. Architecture tests must
preserve M195, the fixed fixture, runtime, examples, scripts, dependencies,
workflows, and the wheel boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, findings-first, and guarded-cleanup gates remain
required.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: pipe handle inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance)
- [Microsoft: `WriteFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile)
- [Python: buffered I/O](https://docs.python.org/3/library/io.html)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [RFC-0178](0178-probe-windows-hard-link-alias-mutator-buffered-close-delivery-failure-after-invalid-settlement.md)
