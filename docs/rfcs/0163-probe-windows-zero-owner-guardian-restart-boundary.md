# RFC-0163: probe Windows zero-owner guardian restart boundary

- **Status:** Accepted
- **Milestone:** M180
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe with two controlled observations
after an M178 guardian is abruptly terminated and reaped. First, start a new
guardian without intervening mutation and require it to reacquire the unchanged
coordination identity. Second, substitute the pathname during the zero-owner
interval and require a later guardian to protect the replacement identity, not
the displaced original. Add no runtime or CI surface.

## Context

M179 proves overlapping rotation: a second guardian is already live before the
first fails. It deliberately leaves the zero-owner restart boundary open.

Microsoft documents that a file's sharing modes remain effective until the
owning handle closes. Microsoft also documents `TerminateProcess` as
asynchronous, so a replacement must not be interpreted until the terminated
process has been boundedly waited. `MoveFileExW` operates on pathnames; after
all no-delete-share owners close, the existing M174 fixture can rename the
original and create a distinct object at the reusable coordination pathname.

These primitives support a bounded negative boundary observation. They do not
provide durable identity, trusted placement, guardian election, authenticated
startup, recovery, or generation authority.

## Decision

Accept the [Windows zero-owner guardian restart-boundary
probe](../security/cache-cleanup-windows-zero-owner-guardian-restart-boundary-probe.md)
as current-host, test-only evidence for two exact sequences.

For the benign sequence, create M173's ordinary `live/coordination.lock` and
retain its `FILE_ID_INFO`. Start M178's unchanged guardian, require exact
`ready`, M174 substitution error 32, and exact M173 exclusive range
acquire/release. Kill and boundedly wait for that guardian through M176's
unchanged helper. Observe the pathname still names the original identity and
that the range remains available. Start a second unchanged guardian, require
exact `ready`, original identity, substitution error 32, and range
availability. Close it exactly, then require substitution success, displaced
original identity, distinct replacement identity, and exact bytes.

For the substitution sequence, repeat the first guardian start and bounded
abrupt wait. During the zero-owner interval, require M174 substitution success,
retain the displaced original identity, and observe the distinct replacement
identity. Start the second guardian only afterward. Require it to preserve the
replacement identity, block a second direct rename with sharing error 32, and
leave exact range ownership available. Close it exactly, require that rename
to succeed, and verify the moved replacement identity, displaced original
identity, exact bytes, and complete cleanup. Use no retry or sleep.

## Consequences

On the observed host, a newly started guardian can open an unchanged pathname
after a zero-owner interval. If substitution occurs first, the same guardian
behavior protects the replacement object instead. The guardian has no memory
of, proof about, or authority over the prior identity.

This is a restart-boundary probe, not crash recovery, generation authority,
leader election, trusted placement, startup authentication, continuity, or
cleanup authority. The benign case is explicitly mutation-free; it cannot show
that mutation was impossible. The substituted case demonstrates the opposite:
pathname reuse alone cannot recover the displaced generation.

Windows remains unadmitted. Simultaneous loss, failed guardian launch, hostile
preexisting handles, arbitrary process trees, mapped views, filesystem/driver
variation, durable generation issuance, use-time revalidation, fail-closed
policy, typed receipts, complete admission, and independent-host proof remain
open.

No fixture, runtime API, adapter, public probe, production subprocess or
`ctypes`, cache access, cleanup authority, dependency, workflow, permission,
or hosted check is added.

## Alternatives considered

- Treat benign pathname reacquisition as recovery. Rejected because an
  unobserved actor could substitute the object during the zero-owner interval.
- Require the later guardian to recover the displaced object. Rejected because
  the fixed guardian receives only the current pathname and no trusted identity
  or generation record.
- Add a durable generation file or coordinator. Rejected as security-sensitive
  runtime design beyond this test-only evidence slice.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  will collect the source test after the prerequisite stack is integrated.

## Validation

Focused validation must prove both post-wait orderings, original and
replacement identities, sharing error 32 while each restarted guardian is
live, exact range availability, successful rename after exact close, byte
preservation, and complete process/stream/handle/range cleanup. Architecture
tests must preserve M179, runtime, examples, scripts, dependencies, workflows,
fixtures, and the wheel package boundary.

Supported-Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, and findings-first gates remain required.

## References

- [Microsoft: `CreateFileW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Microsoft: `MoveFileExW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [GitHub Actions matrix behavior](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [RFC-0162](0162-probe-windows-overlapping-guardian-rotation.md)
