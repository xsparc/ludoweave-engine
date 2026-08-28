# RFC-0155: probe Windows descendant non-exclusion

- **Status:** Accepted
- **Milestone:** M172
- **Date:** 2026-08-29

## Summary

Add one Windows-only, test-only NTFS probe for both acquisition orders between
M171's zero-sharing directory owner and a fixed child holding one descendant
file. Require both owners to coexist and close independently. Record that a
zero-sharing directory handle is not recursive quiescence. Add no runtime or CI
surface.

## Context

M171 proves share-mode exclusion for repeated opens of the same ordinary
directory object. The accepted M147 threat model requires cross-process
quiescence covering readers, writers, leases, pins, and publication state
through candidate derivation and mutation. M171 does not establish whether its
directory owner affects handles to files beneath that directory.

Microsoft documents share compatibility for the file object named by an open
request. `IoCheckShareAccess` receives the particular file object and its
associated share-access state. Those contracts do not state that a directory
open recursively controls separate descendant file objects. A current-host
probe is required before considering M171's primitive for a private adapter.

## Decision

Accept the [Windows descendant non-exclusion
probe](../security/cache-cleanup-windows-descendant-non-exclusion-probe.md) as
current-host, test-only evidence.

Create one ordinary `live/candidate.bin` beneath an NTFS pytest root. A fixed
isolated child opens only that relative file for generic read access with read,
write, and delete sharing, null security attributes, and no caller-controlled
input. It proves the handle noninheritable, emits exact bounded `ready`, waits
for one fixed release byte, closes the handle, emits exact bounded `closed`,
and exits zero.

Exercise both orderings:

1. acquire M171's zero-sharing `live` directory owner, then start the descendant
   holder and require `ready` while the root owner remains live; and
2. start the descendant holder and require `ready`, then acquire M171's
   zero-sharing `live` directory owner while the child remains live.

In both cases require simultaneous ownership, unchanged candidate bytes,
noninheritable handles, independent deterministic close, bounded process and
stream settlement, and zero leaked parent handles. Use no sleeps, retries,
shells, broad inheritance, path arguments, environment-selected behavior,
arbitrary commands, or unbounded output.

## Consequences

The current NTFS host permits the separate directory and descendant file
objects to remain open simultaneously in either acquisition order. M171's
zero-sharing directory owner excludes incompatible opens of that directory;
it does not recursively exclude access to a file beneath it.

This result blocks promotion of the M171 primitive as a complete subtree lock.
A future quiescence design must bind every relevant participant through a
separate protocol, generation, lease/pin registry, or stronger proven platform
primitive and must revalidate retained roots at use.

This is not proof for writes, deletes, mappings, descendant directories,
multiple participants, oplocks, leases, cancellation, process death, native
close failure, other filesystems, recovery, policy, receipts, or independent
hosts. Windows is not admitted.

No runtime API, value, protocol, decoder, CLI command, public probe, production
subprocess or `ctypes`, dependency, workflow, permission, or hosted check is
added.

## Alternatives considered

- Infer recursive behavior from the term `directory handle`. Rejected because
  documented share checking is tied to the opened file object.
- Promote M171 directly into a private adapter. Rejected because descendant
  participants would remain outside the proven exclusion boundary.
- Use a same-process ordinary file object. Rejected because a fixed child gives
  explicit cross-process ownership and bounded close phases.
- Add a runtime participant registry now. Rejected because retained-root,
  generation, recovery, policy, and receipt design remain jointly unresolved.
- Add another hosted matrix entry. Rejected because the existing Windows suite
  will collect this source test after the prerequisite stack is integrated.

## Validation

Focused validation must prove NTFS binding, exact fixed descendant path,
generic-read/all-sharing access, null security attributes, noninheritability,
both acquisition orders, simultaneous live owners, unchanged content,
independent close, bounded output/waits, and zero leaked handles or streams.
Architecture tests must preserve M171, M155, M149, their fixtures, runtime,
examples, scripts, dependencies, workflows, and wheel contents. Supported-
Python, full regression, installed-wheel, reproducibility, release,
documentation, governance, and findings-first gates remain required.

## References

- [Microsoft: `CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [Microsoft: `IoCheckShareAccess`](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-iocheckshareaccess)
- [GitHub Actions matrix strategy](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [M147 cleanup threat model](../security/cache-cleanup-threat-model.md)
- [RFC-0154](0154-probe-windows-exclusive-root-acquisition.md)
