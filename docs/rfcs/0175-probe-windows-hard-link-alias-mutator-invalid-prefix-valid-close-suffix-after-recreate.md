# RFC-0175: probe Windows alias-mutator invalid prefix with valid close suffix after recreation

- **Status:** Accepted
- **Milestone:** M192
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that writes the fixed two-byte
sequence `?!` to M186's independent alias-mutator control pipe after its exact
`recreated` event. The first byte is M190's fixed invalid token and the second
is the fixture's valid close token. Require the unchanged child to emit no
`closed` event and settle with exit 5. Require the peer alias to remain present
with the original identity, bytes, and two-link count while M181's matching
guardian remains live. Add no runtime or CI surface.

## Context

M190 proves that one fixed invalid byte after recreation produces exit 5
without a close event. M191 proves that `!?` accepts the leading valid close
byte and ignores its trailing invalid byte. Neither observes the inverse fixed
sequence supplied together in one write.

Microsoft documents anonymous pipes as byte streams and states that byte-mode
pipes do not preserve distinctions between write operations. Python documents
buffered binary `write()` as returning the accepted byte count and `flush()`
as forcing buffered bytes to the underlying stream. M186's unchanged child
performs exactly one `read(1)` for its close phase and returns immediately after
the byte either matches or fails its fixed token check.

## Decision

Accept the [Windows hard-link alias mutator invalid prefix with valid close
suffix after recreation
probe](../security/cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-after-recreate-probe.md)
as current-host, test-only prefix-precedence rejection evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian child with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Start M186's unchanged fixed mutator child and require exact `deleted`. Send
the exact recreate token and require exact `recreated`. Before the close-phase
sequence, require both children live, the peer alias present, unchanged shared
identity and bytes, link count two, and byte-range availability through both
names.

Write `?!` exactly once. Require the buffered write to accept both bytes,
flush, close the parent writer, and wait with M186's fixed timeout. Require exit
5, stdout EOF with no `closed` event, and empty stderr. After settlement,
require guardian liveness, continued alias presence, unchanged shared identity
and bytes, link count two, range availability, and persistent exact-name rename
refusal. Release the guardian exactly, rename the original, and require
displaced and alias identity, count, bytes, processes, streams, native handles,
and ranges to settle. Use no retry or sleep.

## Consequences

On the observed host, the unchanged fixture rejects the leading invalid byte
and exits without consuming the trailing valid close byte as an overriding
command. It emits no close acknowledgement and leaves the alias present. This
is prefix-precedence rejection evidence for one fixed sequence and one fixture,
not a production protocol contract.

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

- Send the bytes in separate writes. Rejected because a byte stream does not
  preserve that boundary and the second write could race the child exit,
  conflating prefix behavior with broken-pipe behavior.
- Change the child to inspect the suffix. Rejected because M192 observes the
  fixed M186 fixture rather than designing a production protocol.
- Generalize to arbitrary invalid prefixes or trailing payloads. Rejected
  because M192 has evidence only for one two-byte sequence.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  is the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove initial shared identity/count, exact guardian and
mutator phase ordering, child-owned delete and recreation, one accepted and
flushed two-byte write, bounded exit 5 without a close acknowledgement, stdout
EOF and empty stderr, persistent two-link shared state, retained bytes, range
availability, guardian liveness and rename refusal, post-guardian rename, and
complete cleanup. Architecture tests must preserve M186-M191, the fixed
fixture, runtime, examples, scripts, dependencies, workflows, and the wheel
boundary.

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
- [RFC-0174](0174-probe-windows-hard-link-alias-mutator-valid-close-prefix-trailing-byte-after-recreate.md)
