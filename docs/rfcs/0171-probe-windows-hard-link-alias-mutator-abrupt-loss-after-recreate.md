# RFC-0171: probe Windows hard-link alias mutator abrupt loss after recreation

- **Status:** Accepted
- **Milestone:** M188
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that terminates and reaps M186's
independent alias-mutator child after its exact `recreated` event but before
the close token. Require the peer alias to remain present with the original
identity, bytes, and two-link count while M181's matching guardian child
remains live. Add no runtime or CI surface.

## Context

M187 proves that losing the mutation actor after its `deleted` event leaves a
stable one-link state and does not automatically recreate the peer alias. M186
also proves the normal `2 -> 1 -> 2` path, but closes its mutator cooperatively
after recreation. Neither result determines whether killing that actor after
recreation removes its completed directory entry or restores the preceding
one-link state.

Microsoft documents `TerminateProcess` as unconditional and asynchronous for
an external caller, which must wait to know termination has completed. Python
maps `Popen.kill()` to process termination on Windows. Microsoft documents a
hard link as a directory entry for one shared file and permits links to be
deleted independently. Those contracts provide no application-level rollback
of a successfully recreated link when its creating process later terminates.

## Decision

Accept the [Windows hard-link alias mutator abrupt-loss-after-recreate
probe](../security/cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-after-recreate-probe.md)
as current-host, test-only negative rollback evidence.

Create M173's ordinary coordination file and peer alias, retain their matching
`FILE_ID_INFO`, require link count two, and close the initial handles. Start
M181's guardian child with that exact identity and require `ready`. Reopen the
original and require exact-name rename to fail with Windows sharing error 32.

Start M186's unchanged fixed mutator child and require its exact `deleted`
event. Send the exact recreate token and require `recreated`. Before any close
token, require both children live, the peer alias present, unchanged shared
identity and bytes, link count two, and byte-range availability through both
names. Then terminate and reap the mutator with the existing bounded abrupt-
settlement helper. Require a nonzero exit and empty remaining output.

After reaping, require guardian liveness, continued alias presence, unchanged
shared identity and bytes, link count two, range availability, and persistent
exact-name rename refusal. Release the guardian through its exact close
protocol. Rename the original successfully and require the displaced name and
alias to retain the shared identity, two-link count, and bytes. Require both
child processes and all streams, native handles, and byte ranges to settle.
Use no retry or sleep.

## Consequences

On the observed host, process loss after recreation does not remove the peer
alias and does not automatically roll back to one link. The parent observes a
stable two-link state after the mutator is reaped while the guardian still
protects the original name. This is negative rollback evidence, not durable
commit or recovery evidence.

The result does not mean abrupt termination is safe. It intentionally kills a
controlled test process only after a bounded event and waits for complete
termination. A production mutation state machine would still need durable
intent, quarantine, idempotency, reconciliation, and typed recovery receipts.

This remains a three-process, same-principal observation under one parent-
owned process tree. It does not establish cross-principal behavior, an
unrelated process tree or user session, hostile simultaneous racing, crash
consistency, power-loss behavior, or security isolation from the mutator.

Windows remains unadmitted. Cross-volume behavior, ReFS, SMB, other drivers or
Windows versions, file-ID reuse, failed launch, owner loss during other phases,
durable recovery, and independent-host proof remain open.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check
is added.

## Alternatives considered

- Treat alias persistence as durable commit evidence. Rejected because the
  probe does not flush intent or recovery state and does not simulate a crash
  or power loss.
- Modify the child to terminate itself. Rejected because reusing the fixed M186
  fixture preserves the mutation boundary and lets the parent exercise the
  documented external termination-and-wait sequence.
- Infer rollback safety from retaining two links. Rejected because persistent
  namespace state is neither an authenticated receipt nor a recovery policy.
- Add a hosted matrix allocation. Rejected because the existing Windows suite
  is the only future hosted execution path needed for this source test.

## Validation

Focused validation must prove initial shared identity/count, exact guardian and
mutator phase ordering, child-owned delete and recreation, termination before
any close token, nonzero reaped exit, empty remaining output, persistent two-
link shared state, retained bytes, range availability, guardian liveness and
rename refusal, post-guardian rename, and complete cleanup. Architecture tests
must preserve M186-M187, runtime, examples, scripts, dependencies, workflows,
and the wheel boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, findings-first, and guarded-cleanup gates remain
required.

## References

- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft: hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Python: `subprocess`](https://docs.python.org/3/library/subprocess.html)
- [GitHub Actions matrix jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [RFC-0170](0170-probe-windows-hard-link-alias-mutator-abrupt-loss.md)
