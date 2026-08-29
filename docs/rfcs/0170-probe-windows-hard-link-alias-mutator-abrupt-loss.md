# RFC-0170: probe Windows hard-link alias mutator abrupt loss

- **Status:** Accepted
- **Milestone:** M187
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that terminates and reaps M186's
independent alias-mutator child after its exact `deleted` event and before the
recreate token. Require the peer alias to remain absent and the original to
retain its identity, bytes, and one-link count while M181's matching guardian
child remains live. Add no runtime or CI surface.

## Context

M186 proves that a distinct sibling child can delete and recreate a hard-link
alias while the exact-name guardian remains live. The success path deliberately
supplies a recreate token, however, and therefore says nothing about state when
the mutation actor is lost between those operations.

Microsoft documents `TerminateProcess` as unconditional and asynchronous for
an external caller, which must wait to know termination has completed. Python
maps `Popen.kill()` to process termination on Windows. Microsoft also documents
hard links as independently deletable directory entries for one file; it does
not provide application-level rollback of a deleted entry. Those contracts
support a focused abrupt-loss observation but do not define a cleanup recovery
protocol.

## Decision

Accept the [Windows hard-link alias mutator abrupt-loss
probe](../security/cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-probe.md)
as current-host, test-only negative recovery evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian child with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Start M186's unchanged fixed mutator child and require its exact `deleted`
event. Before sending any recreate token, require both children live, alias
absence, unchanged original identity and bytes, link count one, and byte-range
availability. Then terminate and reap the mutator with the existing bounded
abrupt-settlement helper. Require a nonzero exit, empty remaining output,
guardian liveness, continued alias absence, unchanged identity and bytes, link
count one, range availability, and persistent exact-name rename refusal.

Release the guardian through its exact close protocol. Rename the original
successfully and require the displaced name to retain the original identity,
one-link count, and bytes. Require both child processes and all streams, native
handles, and byte ranges to be settled. Use no retry or sleep.

## Consequences

On the observed host, process loss after the delete phase does not recreate the
peer alias. The parent observes a stable one-link state after the mutator is
reaped while the guardian still protects the original name. This is evidence
of a recovery gap: there is no automatic rollback or recovery in this test
boundary.

The result does not mean abrupt termination is safe. It intentionally kills a
controlled test process only after a bounded event and then waits for complete
termination. A production mutation state machine would still need durable
intent, quarantine, idempotency, reconciliation, and typed recovery receipts.

This remains a three-process, same-principal observation under one parent-owned
process tree. It does not establish cross-principal behavior, an unrelated
process tree or user session, hostile simultaneous racing, crash consistency,
power-loss behavior, or security isolation from the mutator.

Windows remains unadmitted. Cross-volume behavior, ReFS, SMB, other drivers or
Windows versions, file-ID reuse, failed launch, owner loss during other phases,
durable recovery, and independent-host proof remain open.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check is
added.

## Alternatives considered

- Treat M186's successful recreate as recovery evidence. Rejected because the
  parent explicitly sends the recreate token and observes no failure.
- Modify the child to self-terminate. Rejected because reusing the fixed M186
  fixture keeps the mutation boundary unchanged and lets the parent exercise
  the documented external termination-and-wait sequence.
- Infer durable rollback from alias absence. Rejected because absence is only
  the residual namespace state, not a receipt, repair action, or recovery
  state machine.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  is the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove initial shared identity/count, exact guardian and
mutator phase ordering, child-owned deletion, termination before any recreate
token, nonzero reaped exit, empty remaining child output, one-link residual
state, retained bytes, range availability, guardian liveness and rename
refusal, post-guardian rename, and complete cleanup. Architecture tests must
preserve M186, runtime, examples, scripts, dependencies, workflows, and the
wheel boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, findings-first, and guarded-cleanup gates remain
required.

## References

- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [GitHub Actions matrix jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [RFC-0169](0169-probe-windows-independent-hard-link-alias-mutator-aba.md)
