# RFC-0178: probe Windows buffered-close delivery failure after invalid settlement

- **Status:** Accepted
- **Milestone:** M195
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that preserves M194's exact `?!`
write, flush, bounded exit-5 settlement, and one-byte late `!` buffer
acceptance. Do not call a late `flush()`. Instead, call `close()` directly,
require generic `OSError` from the close-triggered delivery attempt, and
require the stream closed afterward. Preserve the alias, guardian, identity,
link-count, range, rename, and cleanup boundaries. Add no runtime or CI
surface.

## Context

M194 proves that a one-byte buffered write can report local acceptance after
the child has settled, then fail delivery when explicitly flushed. It closes
the stream only after that failed flush and suppresses the already-observed
delivery error. It does not isolate what the buffered stream reports when
`close()` itself is the first late delivery attempt.

Python documents `BufferedWriter` as writing pending bytes when the object is
closed or destroyed. Microsoft documents `WriteFile` on an anonymous pipe as
failing with `ERROR_BROKEN_PIPE` after the corresponding read handle closes.
CPython's Windows I/O and C-runtime layers may translate the raw condition, so
one Python exception subtype or numeric code is not a portable protocol
contract.

## Decision

Accept the [Windows hard-link alias mutator buffered-close delivery-failure
probe](../security/cache-cleanup-windows-hard-link-alias-mutator-buffered-close-delivery-failure-after-invalid-settlement-probe.md)
as current-host, test-only close-triggered delivery evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Start M186's unchanged child and require exact `deleted`. Send the exact
recreate token and require exact `recreated`. Require both children live, the
peer alias present, unchanged shared identity and bytes, link count two, and
byte-range availability through both names.

Write and flush `?!` exactly once. Keep the writer open across M186's bounded
wait and require exit 5, stdout EOF, empty stderr, and no `closed` event. Only
after that terminal evidence, write one late valid `!` byte and require the
buffered call to accept exactly one byte. Without a preceding failed late
flush, call `close()` directly, require generic `OSError`, and then require the
stream closed. Make no exception subtype, `errno`, or Windows error-code
assertion.

Require guardian liveness, continued alias presence, unchanged identity, bytes
and two-link state, range availability, and persistent rename refusal. Release
the guardian exactly, rename the original, and require complete identity,
count, bytes, process, stream, native-handle, and range cleanup. Use no retry
or sleep.

## Consequences

On the observed host, direct buffered-stream closure attempts delivery of the
accepted late byte, reports delivery failure, and still leaves the stream
closed. Code must not interpret a close exception as evidence that the stream
remains open, or interpret a prior buffered byte count as peer receipt.

This does not establish arbitrary buffered input, larger or repeated writes,
buffer-full behavior, partial raw writes, concurrent or pre-settlement late
commands, exception-code portability, acknowledgement semantics,
authenticated cancellation, rollback policy, or safe cache cleanup. A
production protocol must use explicit framing, authenticated authority,
acknowledgements or typed receipts, bounded I/O, durable intent, quarantine,
idempotency, reconciliation, and typed recovery behavior.

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

- Reuse M194's explicit late `flush()` before closing. Rejected because it
  would not isolate close as the first delivery attempt.
- Require `close()` to succeed. Rejected because pending bytes must be
  delivered and the peer has already closed its read handle.
- Assert `BrokenPipeError`, `errno`, or `winerror`. Rejected because CPython's
  Windows runtime translation is not the engine protocol and may vary.
- Change the child to acknowledge the late byte. Rejected because the
  milestone observes the established fixture after terminal settlement.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  remains the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove exact phase ordering, M193's accepted and
flushed `?!`, bounded exit 5 and terminal output while the writer is open,
then exactly one buffered late `!` acceptance followed directly by generic
close failure and final stream closure. It must retain identity/count, alias
presence, bytes, ranges, guardian liveness, rename refusal, post-guardian
rename, and complete cleanup. Architecture tests must preserve M194, the fixed
fixture, runtime, examples, scripts, dependencies, workflows, and the wheel
boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, findings-first, and guarded-cleanup gates remain
required.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: pipe handle inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance)
- [Microsoft: `WriteFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Python: buffered I/O](https://docs.python.org/3/library/io.html)
- [Python: built-in exceptions](https://docs.python.org/3/library/exceptions.html)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [RFC-0177](0177-probe-windows-hard-link-alias-mutator-late-valid-close-delivery-failure-after-invalid-settlement.md)
