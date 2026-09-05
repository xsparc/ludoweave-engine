# RFC-0174: probe Windows alias-mutator valid close prefix with trailing byte after recreation

- **Status:** Accepted
- **Milestone:** M191
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that writes the fixed two-byte
sequence `!?` to M186's independent alias-mutator control pipe after its exact
`recreated` event. The first byte is the fixture's valid close token and the
second is M190's fixed invalid token. Require the unchanged child to emit exact
`closed` and settle with exit 0 while the parent writer is still open after the
event. Require the peer alias to remain present with the original identity,
bytes, and two-link count while M181's matching guardian remains live. Add no
runtime or CI surface.

## Context

M186 proves the normal single-byte close path. M190 proves that one fixed
invalid byte after recreation produces exit 5 without a close event. Neither
observes a valid close prefix and trailing byte supplied together in one
write.

Microsoft documents anonymous pipes as byte streams and states that byte-mode
pipes do not preserve distinctions between write operations. Python documents
buffered binary `write()` as returning the accepted byte count and `flush()`
as forcing buffered bytes to the underlying stream. M186's unchanged child
performs exactly one `read(1)` for its close phase and returns immediately after
the matching byte.

## Decision

Accept the [Windows hard-link alias mutator valid close prefix with trailing
byte after recreation
probe](../security/cache-cleanup-windows-hard-link-alias-mutator-valid-close-prefix-trailing-byte-after-recreate-probe.md)
as current-host, test-only trailing-input acceptance evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian child with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Start M186's unchanged fixed mutator child and require exact `deleted`. Send
the exact recreate token and require exact `recreated`. Before the close
sequence, require both children live, the peer alias present, unchanged shared
identity and bytes, link count two, and byte-range availability through both
names.

Write `!?` exactly once. Require the buffered write to accept both bytes,
flush, then require exact `closed` while the parent writer remains open. Close
that writer, wait with M186's fixed timeout, and require exit 0, stdout EOF, and
empty stderr. After settlement, require guardian liveness, continued alias
presence, unchanged shared identity and bytes, link count two, range
availability, and persistent exact-name rename refusal. Release the guardian
exactly, rename the original, and require displaced and alias identity, count,
bytes, processes, streams, native handles, and ranges to settle. Use no retry
or sleep.

## Consequences

On the observed host, the unchanged fixture treats the leading valid close byte
as sufficient and does not reject the one trailing invalid byte. It emits its
normal close acknowledgement and exit code while the alias remains present.
This is trailing-input acceptance evidence for one fixed sequence and one
fixture, not a production protocol contract.

The result does not establish arbitrary malformed input, partial writes,
separate writes, more than one trailing byte, message boundaries, authenticated
cancellation, rollback policy, or safe cleanup action. A production mutation
state machine would still need explicit framing, authenticated authority,
durable intent, quarantine, idempotency, reconciliation, and typed recovery
receipts.

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

- Send the close and invalid bytes in separate writes. Rejected because a byte
  stream does not preserve that boundary and the second write could race the
  child exit, conflating framing with broken-pipe behavior.
- Send an invalid leading byte. Rejected because M190 already records that
  fixed condition after recreation.
- Change the child to reject trailing bytes. Rejected because M191 is an
  observation of the fixed M186 fixture, not production protocol design.
- Generalize to arbitrary trailing payloads. Rejected because M191 has evidence
  only for one two-byte sequence.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  is the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove initial shared identity/count, exact guardian and
mutator phase ordering, child-owned delete and recreation, one accepted and
flushed two-byte write, exact close acknowledgement before parent-writer close,
bounded exit 0, stdout EOF and empty stderr, persistent two-link shared state,
retained bytes, range availability, guardian liveness and rename refusal,
post-guardian rename, and complete cleanup. Architecture tests must preserve
M186-M190, the fixed fixture, runtime, examples, scripts, dependencies,
workflows, and the wheel boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, findings-first, and guarded-cleanup gates remain
required.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: named-pipe type and read modes](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-type-read-and-wait-modes)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Python: `io`](https://docs.python.org/3/library/io.html)
- [GitHub Actions matrix jobs](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [RFC-0173](0173-probe-windows-hard-link-alias-mutator-invalid-control-token-after-recreate.md)
