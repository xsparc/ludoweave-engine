# RFC-0177: probe Windows late valid-close delivery failure after invalid settlement

- **Status:** Accepted
- **Milestone:** M194
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that preserves M193's exact `?!`
write, flush, and bounded exit-5 settlement with the parent writer open. After
the child has already settled and stdout/stderr have reached their expected
terminal state, write one late valid `!` byte to the parent-side buffered
writer. Require the buffer to accept one byte, then require delivery to fail on
`flush()` with a generic `OSError`. Close the writer best-effort and require it
closed. Preserve the alias, guardian, identity, link-count, range, rename, and
cleanup boundaries. Add no runtime or CI surface.

## Context

M193 proves the child rejects `?!` and exits while the parent writer remains
open. It closes the writer after observing child exit, stdout EOF, and empty
stderr. It does not observe what a parent-side buffered writer reports if a
late command is attempted after that terminal state.

Python documents `BufferedWriter` as normally placing data in an internal
buffer and returning a byte count from `write()`. The underlying raw stream is
updated when the buffer is flushed or closed. Therefore, a successful small
buffered write does not by itself prove that a peer received the byte.

Microsoft documents anonymous pipes as byte streams and specifies that
`WriteFile` fails with `ERROR_BROKEN_PIPE` if the corresponding read handle is
closed. CPython's Windows I/O stack may translate that raw condition through
its C runtime. The project must not treat one observed Python exception name or
numeric code as a portable protocol contract.

## Decision

Accept the [Windows hard-link alias mutator late valid-close delivery-failure
probe](../security/cache-cleanup-windows-hard-link-alias-mutator-late-valid-close-delivery-failure-after-invalid-settlement-probe.md)
as current-host, test-only buffered acceptance-versus-delivery evidence.

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
after that terminal evidence, write one late valid `!` byte. Require the
buffered call to accept exactly one byte, require generic `OSError` when
`flush()` attempts delivery, and make no exception subtype, `errno`, or Windows
error-code assertion. Close the writer while suppressing the already-observed
delivery error and require the stream closed.

Require guardian liveness, continued alias presence, unchanged identity, bytes
and two-link state, range availability, and persistent rename refusal. Release
the guardian exactly, rename the original, and require complete identity,
count, bytes, process, stream, native-handle, and range cleanup. Use no retry or
sleep.

## Consequences

On the observed host, buffering one late valid close byte can report local
acceptance even though the child has already terminated and cannot receive it.
The following flush supplies the delivery-failure boundary. Protocol designs
must not equate a buffered byte count with peer receipt or command execution.

This does not establish arbitrary buffered input, larger writes, buffer-full
behavior, partial raw writes, concurrent or pre-settlement late commands,
exception-code portability, acknowledgement semantics, authenticated
cancellation, rollback policy, or safe cache cleanup. A production protocol
must use explicit framing, authenticated authority, acknowledgements or typed
receipts, bounded I/O, durable intent, quarantine, idempotency,
reconciliation, and typed recovery behavior.

This remains a three-process, same-principal observation under one parent-owned
process tree. It does not establish cross-principal behavior,
duplicated/inherited writers, unrelated processes or sessions, hostile
simultaneous racing, crash consistency, power loss, or security isolation.

Windows is not admitted. ReFS, SMB, other drivers and Windows versions,
cross-volume behavior, file-ID reuse, durable recovery, and independent-host
proof remain open. No runtime API, adapter, public probe, production subprocess
or `ctypes`, cache access, cleanup authority, dependency, workflow, permission,
or hosted check is added.

## Alternatives considered

- Send the late byte before child settlement. Rejected because byte-stream
  scheduling would race the child's close-phase read and conflate prefix
  behavior with peer-close timing.
- Use an unbuffered native write and freeze `ERROR_BROKEN_PIPE`. Rejected
  because M194 is specifically about the public Python buffered stream and
  should not add or expose a native error-code contract.
- Assert `BrokenPipeError`, `errno`, or `winerror`. Rejected because CPython's
  Windows runtime translation is not the engine protocol and may vary.
- Change the child to acknowledge the late byte. Rejected because the milestone
  observes the established fixture after terminal settlement.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  remains the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove exact phase ordering, M193's accepted and flushed
`?!`, bounded exit 5 and terminal output while the writer is open, then exactly
one buffered late `!` acceptance followed by generic flush failure and explicit
stream closure. It must retain identity/count, alias presence, bytes, ranges,
guardian liveness, rename refusal, post-guardian rename, and complete cleanup.
Architecture tests must preserve M186-M193, the fixed fixture, runtime,
examples, scripts, dependencies, workflows, and the wheel boundary.

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
- [RFC-0176](0176-probe-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-open-writer-settlement-after-recreate.md)
