# RFC-0172: probe Windows alias-mutator control-pipe EOF after recreation

- **Status:** Accepted
- **Milestone:** M189
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that closes the parent writer for
M186's independent alias-mutator control pipe after its exact `recreated`
event and before the close token. Require the unchanged child to settle with
its fixed exit code 5 and no `closed` event. Require the peer alias to remain
present with the original identity, bytes, and two-link count while M181's
matching guardian remains live. Add no runtime or CI surface.

## Context

M186 proves the normal `2 -> 1 -> 2` mutation and valid-token close path.
M188 proves that external process termination after recreation leaves the
alias present. Neither observes the unchanged child's second control read
settling through EOF after recreation.

Microsoft documents that an anonymous-pipe read returns when all write handles
close and that a child-inherited writer would prevent EOF. Python documents
`stdin=PIPE` as a writable parent stream, `close_fds=True` as excluding
unlisted Windows handles while retaining redirected standard streams, and
`wait(timeout=...)` as a bounded process wait. Microsoft documents a hard link
as one of multiple same-volume paths to one file; closing a control pipe is not
a namespace rollback operation.

## Decision

Accept the [Windows hard-link alias mutator control-pipe EOF after recreation
probe](../security/cache-cleanup-windows-hard-link-alias-mutator-control-pipe-eof-after-recreate-probe.md)
as current-host, test-only negative rollback evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian child with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Start M186's unchanged fixed mutator child and require exact `deleted`. Send
the exact recreate token and require exact `recreated`. Before any close token,
require both children live, the peer alias present, unchanged shared identity
and bytes, link count two, and byte-range availability through both names.

Write no further control byte. Close only the parent's `Popen.stdin`, confirm
the stream is closed, and wait with M186's fixed timeout. Require the child's
existing exit code 5, no `closed` event, stdout EOF, and empty stderr. After
settlement, require guardian liveness, continued alias presence, unchanged
shared identity and bytes, link count two, range availability, and persistent
exact-name rename refusal. Release the guardian exactly, rename the original,
and require displaced and alias identity, count, bytes, processes, streams,
native handles, and ranges to settle. Use no retry or sleep.

## Consequences

On the observed host, control-pipe EOF after recreation leaves the peer alias
present and does not automatically roll back to one link. The child settles
through its user-mode exit path while the guardian still protects the original
name. This is negative rollback evidence, not durable commit or recovery.

The result is not abrupt process termination. It does not establish that EOF
is a production cancellation protocol, authenticated receipt, rollback
policy, or safe cleanup action. A production mutation state machine would
still need durable intent, quarantine, idempotency, reconciliation, and typed
recovery receipts.

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

- Reuse M188's termination helper. Rejected because EOF is a distinct
  cooperative child settlement path and must not be represented as abrupt
  process loss.
- Send an invalid byte. Rejected because it would exercise a protocol value,
  not the absence of every remaining writer.
- Modify the fixture to acknowledge EOF. Rejected because M189 must exercise
  M186's fixed second-read behavior unchanged.
- Treat exit code 5 as rollback. Rejected because the recreated directory entry
  remains present and there is no durable mutation journal or recovery policy.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  is the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove initial shared identity/count, exact guardian and
mutator phase ordering, child-owned delete and recreation, no close token,
explicit parent-writer close, bounded exact exit 5, no `closed` event, stdout
EOF and empty stderr, persistent two-link shared state, retained bytes, range
availability, guardian liveness and rename refusal, post-guardian rename, and
complete cleanup. Architecture tests must preserve M186-M188, runtime,
examples, scripts, dependencies, workflows, and the wheel boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, findings-first, and guarded-cleanup gates remain
required.

## References

- [Microsoft: anonymous pipe operations](https://learn.microsoft.com/en-us/windows/win32/ipc/anonymous-pipe-operations)
- [Microsoft: pipe handle inheritance](https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance)
- [Microsoft: hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [GitHub Actions matrix jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [RFC-0171](0171-probe-windows-hard-link-alias-mutator-abrupt-loss-after-recreate.md)
