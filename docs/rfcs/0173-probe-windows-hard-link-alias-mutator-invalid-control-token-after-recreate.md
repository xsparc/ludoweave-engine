# RFC-0173: probe Windows alias-mutator invalid control token after recreation

- **Status:** Accepted
- **Milestone:** M190
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that writes the repository-fixed
invalid `?` byte to M186's independent alias-mutator control pipe after its
exact `recreated` event and before the close token. Require the unchanged child
to settle with its fixed exit code 5 and no `closed` event. Require the peer
alias to remain present with the original identity, bytes, and two-link count
while M181's matching guardian remains live. Add no runtime or CI surface.

## Context

M186 proves the normal `2 -> 1 -> 2` mutation and valid-token close path. M189
proves that control-pipe EOF after recreation leaves the alias present. Neither
observes the unchanged child's second control read receiving one invalid byte
after recreation.

Microsoft documents anonymous pipes as byte streams whose writes complete or
fail. Python documents `Popen.stdin` as a writable binary stream when no text
mode is selected, buffered `write()` as returning the accepted byte count,
`flush()` as forwarding buffered bytes, and `wait(timeout=...)` as a bounded
process wait. Microsoft documents a hard link as one of multiple same-volume
paths to one file; rejecting a user-mode control byte is not a namespace
rollback operation.

## Decision

Accept the [Windows hard-link alias mutator invalid control token after
recreation
probe](../security/cache-cleanup-windows-hard-link-alias-mutator-invalid-control-token-after-recreate-probe.md)
as current-host, test-only negative rollback evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian child with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Start M186's unchanged fixed mutator child and require exact `deleted`. Send
the exact recreate token and require exact `recreated`. Before any close token,
require both children live, the peer alias present, unchanged shared identity
and bytes, link count two, and byte-range availability through both names.

Write exactly one repository-fixed `?` byte, require the buffered write to
accept exactly one byte, flush it, close the parent writer, and confirm that
stream is closed. Wait with M186's fixed timeout. Require the child's existing
exit code 5, no `closed` event, stdout EOF, and empty stderr. After settlement,
require guardian liveness, continued alias presence, unchanged shared identity
and bytes, link count two, range availability, and persistent exact-name rename
refusal. Release the guardian exactly, rename the original, and require
displaced and alias identity, count, bytes, processes, streams, native handles,
and ranges to settle. Use no retry or sleep.

## Consequences

On the observed host, a fixed invalid control token after recreation leaves
the peer alias present and does not automatically roll back to one link. The
child settles through its user-mode exit path while the guardian still protects
the original name. This is negative rollback evidence, not durable commit or
recovery.

The result is not control-pipe EOF and not abrupt process termination. It does
not establish arbitrary malformed input, partial or multiple writes, an
authenticated cancellation protocol, rollback policy, or safe cleanup action.
A production mutation state machine would still need durable intent,
quarantine, idempotency, reconciliation, and typed recovery receipts.

This remains a three-process, same-principal observation under one parent-
owned process tree. It does not establish cross-principal behavior, duplicated
or inherited control writers, unrelated processes or sessions, hostile
simultaneous racing, crash consistency, power loss, or security isolation.

Windows is not admitted. ReFS, SMB, other drivers and Windows versions,
cross-volume behavior, file-ID reuse, durable recovery, and independent-host
proof remain open. No runtime API, adapter, public probe, production subprocess
or `ctypes`, cache access, cleanup authority, dependency, workflow, permission,
or hosted check is added.

## Alternatives considered

- Close the writer without sending a byte. Rejected because M189 already
  records the distinct control-pipe EOF condition.
- Send M186's valid close token. Rejected because that reproduces the normal
  acknowledged close path rather than protocol rejection.
- Generalize to arbitrary malformed input. Rejected because the fixture reads
  exactly one byte and M190 has evidence only for one repository-fixed value.
- Modify the fixture to acknowledge rejection. Rejected because M190 must
  exercise M186's fixed second-read behavior unchanged.
- Treat exit code 5 as rollback. Rejected because the recreated directory entry
  remains present and there is no durable mutation journal or recovery policy.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  is the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove initial shared identity/count, exact guardian and
mutator phase ordering, child-owned delete and recreation, one accepted and
flushed invalid byte, explicit parent-writer close, bounded exact exit 5, no
`closed` event, stdout EOF and empty stderr, persistent two-link shared state,
retained bytes, range availability, guardian liveness and rename refusal,
post-guardian rename, and complete cleanup. Architecture tests must preserve
M186-M189, the fixed fixture, runtime, examples, scripts, dependencies,
workflows, and the wheel boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, findings-first, and guarded-cleanup gates remain
required.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [Python: `io`](https://docs.python.org/3/library/io.html)
- [GitHub Actions matrix jobs](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [RFC-0172](0172-probe-windows-hard-link-alias-mutator-control-pipe-eof-after-recreate.md)
