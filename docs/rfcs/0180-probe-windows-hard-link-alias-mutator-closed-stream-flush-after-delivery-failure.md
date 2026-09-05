# RFC-0180: probe Windows closed-stream flush after delivery failure

- **Status:** Accepted
- **Milestone:** M197
- **Date:** 2026-08-30

## Summary

Add one Windows-only, test-only NTFS probe that reuses M196's exact repeated-
close disposition after buffered delivery failure. After the first `close()`
raises generic `OSError`, the second `close()` returns `None`, and the stream
is closed, call `flush()` exactly once. Require generic `ValueError` and the
stream still closed. Preserve the alias, guardian, identity, link-count,
range, rename, and cleanup boundaries. Add no runtime or CI surface.

## Context

M196 proves that the concrete `Popen.stdin` buffered stream remains closed and
accepts a repeated `close()` as a no-op after the first close reports delivery
failure. It deliberately leaves every other closed-stream operation outside
its boundary.

Python documents that operations on a closed stream raise `ValueError`, while
also warning that general method behavior on a closed `IOBase` is undefined.
CPython's buffered writer checks closed state before flushing. Microsoft
documents only what happens when `WriteFile` reaches an anonymous pipe whose
read handle is closed. The observation therefore must distinguish one local
concrete-stream exception from a second native write or peer acknowledgement.

## Decision

Accept the [Windows hard-link alias mutator closed-stream flush after delivery-
failure probe](../security/cache-cleanup-windows-hard-link-alias-mutator-closed-stream-flush-after-delivery-failure-probe.md)
as current-host, test-only closed-stream flush disposition evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Start M186's unchanged child and require exact `deleted`. Send the exact
recreate token and require exact `recreated`. Require both children live, the
peer alias present, unchanged shared identity and bytes, link count two, and
byte-range availability through both names.

Delegate the terminal invalid-sequence, first-close failure, and repeated-
close path byte-for-byte to M196. That path preserves M195's buffered late
byte, generic first-close `OSError`, and resulting closed state, then requires
the second `close()` to return `None` with the stream still closed. After the
helper returns, require closed state, call `flush()` exactly once, require
generic `ValueError`, and require closed state again. Freeze no message,
subtype beyond `ValueError`, `errno`, or Windows error code. The observation
does not establish a second native write, retry, or acknowledgement.

Require guardian liveness, continued alias presence, unchanged identity,
bytes and two-link state, range availability, and persistent rename refusal.
Release the guardian exactly, rename the original, and require complete
identity, count, bytes, process, stream, native-handle, and range cleanup. Use
no retry or sleep.

## Consequences

On the observed host and concrete stream, one `flush()` after M196's closed
state raises generic `ValueError` and leaves the stream closed. This is local
closed-stream flush disposition evidence. It does not establish a second
native write, delivery retry, or child acknowledgement.

This does not establish arbitrary closed-stream operations, other stream
implementations, exact error text, larger or repeated buffered writes, partial
raw writes, concurrent commands, portable exception behavior,
acknowledgement semantics, authenticated cancellation, rollback policy, or
safe cache cleanup. A production protocol must use explicit framing,
authenticated authority, acknowledgements or typed receipts, bounded I/O,
durable intent, quarantine, idempotency, reconciliation, and typed recovery
behavior.

This remains a three-process, same-principal observation under one parent-
owned process tree. It does not establish cross-principal behavior,
duplicated/inherited writers, unrelated processes or sessions, hostile
simultaneous racing, crash consistency, power loss, or security isolation.

Windows is not admitted. ReFS, SMB, other drivers and Windows versions,
cross-volume behavior, file-ID reuse, durable recovery, and independent-host
proof remain open. No runtime API, adapter, public probe, production
subprocess or `ctypes`, cache access, cleanup authority, dependency, workflow,
permission, or hosted check is added.

## Alternatives considered

- Stop after M196's repeated close. Rejected because it leaves the nearest
  delivery-adjacent closed-stream operation unobserved.
- Call `write()` or inspect a file descriptor. Rejected because either widens
  the operation and argument boundary or freezes a different inquiry path.
- Assert an exact exception message. Rejected because the current contract
  needs only generic `ValueError` from the concrete observed stream.
- Infer that no native write occurred. Rejected without native-call tracing;
  M197 records only the public method result and retained closed state.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  remains the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove M196 remains byte-for-byte protected, its
repeated-close helper still returns after closed state, and exactly one later
`flush()` raises generic `ValueError` while the stream remains closed. It must
retain identity/count, alias presence, bytes, ranges, guardian liveness,
rename refusal, post-guardian rename, and complete cleanup. Architecture tests
must preserve M196, the fixed fixture, runtime, examples, scripts,
dependencies, workflows, and the wheel boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, findings-first, and guarded-cleanup gates remain
required.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: pipe handle inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance)
- [Microsoft: `WriteFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile)
- [Python 3.14: buffered I/O](https://docs.python.org/3.14/library/io.html)
- [CPython 3.14: `_pyio`](https://github.com/python/cpython/blob/3.14/Lib/_pyio.py)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [RFC-0179](0179-probe-windows-hard-link-alias-mutator-repeated-buffered-close-after-delivery-failure.md)
