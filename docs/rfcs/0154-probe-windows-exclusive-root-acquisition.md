# RFC-0154: probe Windows exclusive-root acquisition

- **Status:** Accepted
- **Milestone:** M171
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe for two directions of native share-
mode exclusion around a directory that represents a selected cache root. A
retained handle opened with sharing mode zero must deny one fixed late child
open until close. An existing fixed child participant must make the exclusive
acquisition fail with error 32 until that child closes. Add no runtime or CI
surface.

## Context

M153 proves that omitting only delete sharing blocks one child rename. M155
proves that a child-owned no-delete-share handle blocks rename until an
acknowledged close. M166-M170 harden handle inheritance and pairwise failure
isolation. They do not execute the two directions of acquiring a directory
handle with no read, write, or delete sharing.

Microsoft documents that a successful `CreateFile` call with sharing mode zero
prevents later opens requesting read, write, or delete access until the handle
closes. A new sharing mode that conflicts with an existing open handle fails
with `ERROR_SHARING_VIOLATION`, and sharing remains in force across processes
until close. A null security-attributes pointer produces a noninheritable
handle. Python exposes the handle-inheritability flag for direct verification.

## Decision

Accept the [Windows exclusive-root acquisition
probe](../security/cache-cleanup-windows-exclusive-root-acquisition-probe.md)
as current-host, test-only evidence.

Create one ordinary `live/candidate.bin` beneath an NTFS pytest root. A private
test probe opens `live` with list/read-attribute/synchronize access, sharing
mode zero, backup semantics, open-reparse-point behavior, and null security
attributes. It must reject a reparse identity, own the returned handle, and
prove that handle noninheritable.

While that owner remains live, a fixed isolated child attempts an ordinary
all-sharing `CreateFileW("live")`. Require an exact versioned document with
`succeeded=false` and error 32, no stderr, and unchanged content. After the
parent closes the exact owner, the identical child must return
`succeeded=true` and error zero.

For the reverse direction, start M155's unchanged fixed child and wait for its
exact `ready` acknowledgement while it owns an ordinary `live` handle. The
parent's zero-sharing acquisition must raise the existing private native error
with exact error 32, adopt no handle, leave the child live, and preserve
content. After the child receives its existing fixed release token, emits
`closed`, and exits zero, the identical parent acquisition must succeed,
remain noninheritable, and close deterministically.

All child arguments, working directories, streams, output bounds, waits, and
cleanup are fixed or pytest-owned. Do not use sleeps, retries, shells, broad
inheritance, environment overrides, arbitrary commands, or unbounded output.

## Consequences

The current host now demonstrates two fail-closed acquisition transitions for
one ordinary NTFS directory: an owned zero-sharing handle blocks one later
participant, and one existing participant blocks zero-sharing acquisition.
Both transitions release only after deterministic close.

This is not a complete quiescence protocol. Attribute-only access is outside
the exercised conflict; mapped files, oplocks, leases, descendant handles,
other access/share combinations, multiple participants, cancellation, native
close failure, filesystem variation, recovery, general exclusion, and
independent-host proof remain open. Windows is not admitted.

No runtime API, value, protocol, decoder, CLI command, public probe, production
subprocess or `ctypes`, dependency, workflow, permission, or hosted check is
added.

## Alternatives considered

- Infer sharing-mode-zero behavior from M153. Rejected because omitting only
  delete sharing does not execute a no-read/no-write/no-delete acquisition.
- Use a timing race between two unsynchronized processes. Rejected because the
  child acknowledgement and retained handle select exact ownership phases.
- Treat sharing mode zero as a complete lock. Rejected because Microsoft
  explicitly separates attribute-only access and many required quiescence
  participants remain untested.
- Add a runtime lock or cleanup adapter. Rejected because M147's retained-root,
  policy, receipt, recovery, and platform-admission requirements remain open.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  will collect the source test after the prerequisite stack is integrated.

## Validation

Focused validation must prove NTFS binding, exact zero sharing, noninheritability,
late-child false/error-32 denial, success after owner close, existing-child
readiness, parent false/error-32 refusal with no adopted handle, acquisition
after acknowledged child close, unchanged content, bounded process ownership,
and zero leaked handles or streams. Architecture tests must preserve M170,
M155, M153, M149, their accepted fixtures, runtime, examples, scripts,
dependencies, workflows, and wheel contents. Supported-Python, full
regression, installed-wheel, reproducibility, release, documentation,
governance, and findings-first gates remain required.

## References

- [Microsoft: `CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [Python: handle inheritance](https://docs.python.org/3/library/os.html#inheritance-of-file-descriptors)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [RFC-0136](0136-probe-windows-share-delete-exclusion.md)
- [RFC-0138](0138-probe-windows-child-owned-share-delete-handshake.md)
- [RFC-0153](0153-probe-windows-concurrent-explicit-abrupt-termination.md)
