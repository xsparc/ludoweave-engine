# RFC-0131: defer portable cache-cleanup capability

- **Status:** Accepted
- **Milestone:** M148
- **Date:** 2026-08-27

## Summary

Reject a standard-library-only portable asset-cache cleanup implementation.
Require evidence-backed, engine-owned platform capability adapters before any
platform is admitted for mutation. Cleanup remains unimplemented and
unauthorized.

## Context

RFC-0130 requires handle-relative, no-follow mutation that fails closed. The
portable Python API exposes filesystem features conditionally: callers must
inspect `os.supports_dir_fd`, `os.supports_fd`, and
`os.supports_follow_symlinks`. Availability differs by operation and platform.

Exact local probes on supported Windows CPython 3.12.13, 3.13.13, and 3.14.5
found no directory-descriptor support for open, unlink, rmdir, rename, or
replace; no relevant no-follow/directory/path open flags; and
`shutil.rmtree.avoids_symlink_attacks == False`.

Lower layers expose useful but non-portable primitives. POSIX defines `openat`,
`unlinkat`, and `renameat`; Linux adds constrained `openat2` resolution; macOS
exposes a stronger no-follow flag; and Win32 can open reparse points and mutate
an opened handle. These surfaces do not form one current portable CPython
contract, and none has complete repository-specific adversarial evidence.

## Decision

Accept the [asset-cache cleanup platform-capability
decision](../security/cache-cleanup-platform-capability-decision.md).

Do not add a cleanup implementation, public capability boolean, path-based
fallback, `ctypes` bridge, native extension, or platform allowlist. A future
proposal must define one private engine-owned adapter lifecycle and prove the
complete acquire/resolve/identity/quarantine/unlink/close chain on every
claimed platform. Native descriptors and handles remain private.

Partial capability is unsupported, not degraded. If any primitive, filesystem
semantic, identity check, or safe failure mode is absent, the operation must
refuse before mutation.

## Consequences

M148 resolves a design uncertainty without changing runtime bytes. Linux,
macOS, and Windows remain project platforms, but none is admitted for cache
cleanup. Platform-specific research can proceed independently while the public
engine remains backend-neutral and pure Python.

M148 adds no runtime API, protocol, decoder, CLI command, public probe, cache
access, candidate disclosure, cleanup authority, mutation, native code,
`ctypes`, dependency, workflow, permission, release authority, or CI change.
There is no remote cache or network behavior.

The next cleanup-related implementation milestone requires an accepted adapter
RFC, explicit maintainer approval, and real-host adversarial evidence. A
documentation-only probe result is insufficient.

## Alternatives considered

- Use `shutil.rmtree` everywhere. Rejected because its symlink-attack-resistant
  implementation is platform-conditional and is false on the exact supported
  Windows runtimes tested.
- Admit Unix and defer Windows. Rejected for this milestone because no real
  macOS/Linux adversarial evidence was executed and support scope is a separate
  product decision.
- Publish a boolean capability probe. Rejected because individual flags do not
  prove the complete safe mutation chain and could be misread as authorization.
- Call Win32 through `ctypes`. Deferred because ABI ownership, handle identity,
  reparse semantics, packaging, crash recovery, and maintenance need a separate
  design and validation boundary.
- Add hosted platform probes now. Rejected because they would consume CI quota
  without validating a concrete adapter or mutation behavior.

## Validation

Architecture tests must protect the M147 threat model plus runtime source,
scripts, dependencies, lock, and workflows byte-exact; prove the platform
decision is complete and registered; and prove no cleanup, adapter, native, or
probe implementation was added. Strict documentation, supported-Python tests,
installed consumers, reproducible distributions, release rehearsal, and
findings-first review remain required.

## References

- [Python `os` filesystem capabilities](https://docs.python.org/3/library/os.html#files-and-directories)
- [Python `shutil.rmtree`](https://docs.python.org/3/library/shutil.html#shutil.rmtree)
- [POSIX `openat`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/open.html)
- [Linux `openat2`](https://man7.org/linux/man-pages/man2/openat2.2.html)
- [Win32 `CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [Win32 `SetFileInformationByHandle`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfileinformationbyhandle)
- [RFC-0130](0130-asset-cache-cleanup-threat-model.md)
