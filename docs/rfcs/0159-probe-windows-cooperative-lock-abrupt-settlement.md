# RFC-0159: probe Windows cooperative-lock abrupt settlement

- **Status:** Accepted
- **Milestone:** M176
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe that forcibly terminates and reaps
M175's protected coordination participants one at a time. Require the survivor
to preserve both pathname-substitution and exclusive-range refusal. After the
last process terminates, require exact exclusive acquire/release and M174
substitution success. Add no runtime or CI surface.

## Context

M175 proves that participants which omit delete sharing protect one
coordination identity throughout continuous graceful ownership. Abrupt-exit
settlement remains unresolved.

Microsoft documents that `TerminateProcess` is asynchronous and that callers
must wait on the process when completed termination matters. Python documents
that `Popen.kill()` is an alias for `terminate()` on Windows and that the latter
uses `TerminateProcess`. Microsoft also documents that the operating system
unlocks outstanding `LockFileEx` ranges after a process terminates or closes
the file, but warns that release time depends on available system resources.

The result therefore must be a bounded current-host observation ordered after
process wait, not a universal immediate-release guarantee.

## Decision

Accept the [Windows cooperative-lock abrupt-settlement
probe](../security/cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe.md)
as current-host, test-only evidence for one exact ownership transition.

Create M173's fixed ordinary `live/coordination.lock`. Start two copies of
M175's unchanged fixed protected child and require both exact `ready` events.
Retain the original `FILE_ID_INFO` identity. While both remain live, require
M174's unchanged substitution child to report `rename_failed`/32 and M173's
unchanged exclusive request to fail with native error 33.

Kill and wait for the first participant with the existing 15-second bound.
Require nonzero status, stdout EOF after the consumed `ready` record, empty
stderr, and no graceful `closed` record. Require the survivor to remain live
and preserve both native refusals.

Kill and wait for the survivor with the same exact checks. Without retry or
sleep, require exclusive acquire/release and then exact M174 substitution
success. Prove the displaced file retains the original identity, the
replacement differs, both bytes remain exact, and every parent handle,
process, pipe, and lock owner settles.

## Consequences

On the observed host, waiting for each abruptly terminated participant orders
release of its no-delete-share handle and shared byte-range lock. One
surviving participant continues to protect the original identity, so the first
termination does not collapse collective ownership.

This is not crash recovery, a guarantee of immediate operating-system release,
or stable generation authority. The test intentionally has no retry that could
hide delayed settlement. Another host may fail the observation within the
fixed bound and must remain unadmitted.

The zero-participant substitution window still exists after the final owner
settles. Trusted root and coordination identity, generation issuance and
retention, complete admission, arbitrary termination timing, process trees,
mapped views, recovery, policy, receipts, and independent hosts remain open.
Windows is not admitted.

No runtime API, adapter, public probe, production subprocess or `ctypes`, cache
access, cleanup authority, dependency, workflow, permission, or hosted check
is added.

## Alternatives considered

- Infer settlement from documentation alone. Rejected because current-host
  behavior and survivor isolation still require an executed observation.
- Poll until ownership disappears. Rejected because a retry would mask the
  exact post-wait boundary and make the evidence less precise.
- Add runtime crash recovery or a permanent coordinator. Rejected because
  generation authority, policy, and durable recovery remain undesigned.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  will collect this source test after the prerequisite stack is integrated.

## Validation

Focused validation must prove both initial refusals, abrupt first-participant
settlement, survivor continuity, abrupt final settlement, exact exclusive
acquire/release, substitution and identity outcomes, byte preservation, EOF,
nonzero exits, and complete owner cleanup. Architecture tests must preserve
M175, runtime, examples, scripts, dependencies, workflows, and the wheel
package boundary.
Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, and findings-first gates remain required.

## References

- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft: `LockFileEx`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)
- [Python: `subprocess`](https://docs.python.org/3.14/library/subprocess.html)
- [M147 cleanup threat model](../security/cache-cleanup-threat-model.md)
- [RFC-0158](0158-probe-windows-live-coordination-substitution-exclusion.md)
