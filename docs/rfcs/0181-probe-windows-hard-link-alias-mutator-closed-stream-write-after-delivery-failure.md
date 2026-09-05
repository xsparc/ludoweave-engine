# RFC-0181: probe Windows closed-stream write after delivery failure

- **Status:** Accepted
- **Milestone:** M198
- **Date:** 2026-08-30

## Summary

Add one Windows-only, test-only NTFS probe that reuses M197's exact closed-
stream flush disposition after buffered delivery failure. After the first
`close()` raises generic `OSError`, the second `close()` returns `None`, one
`flush()` raises generic `ValueError`, and the stream remains closed, call
`write(b"!")` exactly once. Require generic `ValueError` and the stream still
closed. Preserve the alias, guardian, identity, link-count, range, rename, and
cleanup boundaries. Add no runtime or CI surface.

## Context

M197 proves that one `flush()` on the concrete closed `Popen.stdin` buffered
stream raises generic `ValueError` and leaves it closed after the protected
M196 repeated-close sequence. It deliberately leaves `write()` and every other
closed-stream operation outside its boundary.

Python documents that operations after stream closure raise `ValueError`, while
also warning that general method behavior on a closed `IOBase` is undefined.
CPython checks closed state for buffered and raw I/O implementations, but that
implementation evidence cannot prove the absence of a native call on every
interpreter or stream type. Microsoft documents only what happens when
`WriteFile` actually reaches an anonymous pipe whose read handle is closed.
The observation must therefore remain one local concrete-stream exception, not
a native-call or acknowledgement claim.

## Decision

Accept the [Windows hard-link alias mutator closed-stream write after delivery-
failure probe](../security/cache-cleanup-windows-hard-link-alias-mutator-closed-stream-write-after-delivery-failure-probe.md)
as current-host, test-only closed-stream write disposition evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Start M186's unchanged child and require exact `deleted`. Send the exact
recreate token and require exact `recreated`. Require both children live, the
peer alias present, unchanged shared identity and bytes, link count two, and
byte-range availability through both names.

Delegate the terminal invalid-sequence, first-close failure, repeated-close,
and closed-stream flush path byte-for-byte to M197. That path preserves M195's
buffered late byte, generic first-close `OSError`, and resulting closed state;
requires the second `close()` to return `None`; and requires one `flush()` to
raise generic `ValueError` while retaining closed state. After the helper
returns, require closed state, call `write(b"!")` exactly once, require generic
`ValueError`, and require closed state again. Freeze no message, subtype beyond
`ValueError`, `errno`, or Windows error code. The observation does not establish
native-call suppression, a delivery retry, or acknowledgement.

Require guardian liveness, continued alias presence, unchanged identity, bytes
and two-link state, range availability, and persistent rename refusal. Release
the guardian exactly, rename the original, and require complete identity,
count, bytes, process, stream, native-handle, and range cleanup. Use no retry
or sleep.

## Consequences

On the observed host and concrete stream, one `write(b"!")` after M197's closed
state raises generic `ValueError` and leaves the stream closed. This is local
closed-stream write disposition evidence. It does not establish native-call
suppression, a second native write, delivery retry, or child acknowledgement.

This does not establish arbitrary closed-stream operations, other stream
implementations, exact error text, other arguments, larger or repeated writes,
partial raw writes, concurrent commands, portable exception behavior,
acknowledgement semantics, authenticated cancellation, rollback policy, or
safe cache cleanup. A production protocol must use explicit framing,
authenticated authority, acknowledgements or typed receipts, bounded I/O,
durable intent, quarantine, idempotency, reconciliation, and typed recovery
behavior.

This remains a three-process, same-principal observation under one parent-owned
process tree. It does not establish cross-principal behavior, duplicated or
inherited writers, unrelated processes or sessions, hostile simultaneous
racing, crash consistency, power loss, or security isolation.

Windows is not admitted. ReFS, SMB, other drivers and Windows versions,
cross-volume behavior, file-ID reuse, durable recovery, and independent-host
proof remain open. No runtime API, adapter, public probe, production subprocess
or `ctypes`, cache access, cleanup authority, dependency, workflow, permission,
or hosted check is added.

## Alternatives considered

- Stop after M197's closed-stream flush. Rejected because one concrete
  buffered-write operation remains the nearest delivery-adjacent gap.
- Call `writable()`, `fileno()`, or inspect raw state. Rejected because those
  widen the inquiry without testing the bounded write disposition.
- Assert an exact exception message. Rejected because the current contract
  needs only generic `ValueError` from the concrete observed stream.
- Infer that no native write occurred. Rejected without native-call tracing;
  M198 records only the public method result and retained closed state.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  remains the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove M197 remains byte-for-byte protected, its helper
returns after closed state, and exactly one later `write(b"!")` raises generic
`ValueError` while the stream remains closed. It must retain identity/count,
alias presence, bytes, ranges, guardian liveness, rename refusal, post-guardian
rename, and complete cleanup. Architecture tests must preserve M197, the fixed
fixture, runtime, examples, scripts, dependencies, workflows, and the wheel
boundary.

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
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- [RFC-0180](0180-probe-windows-hard-link-alias-mutator-closed-stream-flush-after-delivery-failure.md)
