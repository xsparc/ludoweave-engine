# Asset-cache cleanup platform-capability decision

- **Status:** Accepted; no platform is admitted for cleanup
- **Milestone:** M148
- **Date:** 2026-08-27
- **Baseline:** CPython 3.12–3.14 and the M147 cleanup threat model

## Decision

Do not implement asset-cache cleanup with the current portable Python standard
library. Do not infer safety from path normalization, `lstat()`, a final-
component no-follow flag, or a successful `shutil.rmtree()` call.

A future cleanup must be composed over an engine-owned, platform-specific
filesystem capability. Each implementation must prove that it holds the exact
cache-root namespace, refuses traversal through links or reparse points,
revalidates object identity at use, stages quarantine on the same filesystem,
and fails closed when any primitive or guarantee is unavailable. Backend file
descriptors, operating-system handles, and native objects must never enter the
public API or a command/receipt payload.

M148 admits no implementation. The decision resolves only whether the present
portable standard-library surface is sufficient: it is not.

## Required capability

One admitted platform adapter must provide all of these semantics as one owned
lifecycle, not as unrelated feature probes:

1. open and retain an exact directory capability for the admitted cache root;
2. resolve every relative component beneath that capability without following
   symbolic links, junctions, reparse points, magic links, or mount escapes;
3. inspect identity and link/alias state from the opened object rather than a
   previously resolved string path;
4. move the same identity into a bounded same-filesystem quarantine without
   replacing an unrelated destination;
5. unlink or remove the quarantined identity relative to an owned directory
   capability;
6. make every handle non-inheritable and close it deterministically;
7. expose typed, backend-neutral outcomes while retaining native values
   privately; and
8. report unsupported, changed, busy, partial, and recovery-required states
   without falling back to a weaker path operation.

Availability of one function or constant is not admission. The complete chain
must survive concurrent namespace changes and the M147 adversarial suite.

## Current capability evidence

| Surface | Current evidence | Admission result |
| --- | --- | --- |
| Supported Windows CPython | Exact CPython 3.12.13, 3.13.13, and 3.14.5 on Windows report no `dir_fd` support for `os.open`, `os.unlink`, `os.rmdir`, `os.rename`, or `os.replace`; they expose no `O_DIRECTORY`, `O_NOFOLLOW`, `O_NOFOLLOW_ANY`, or `O_PATH`; and `shutil.rmtree.avoids_symlink_attacks` is `False`. | Rejected. The portable Python surface cannot retain a parent-directory capability through mutation. |
| Portable `pathlib` and string paths | No-follow inspection can identify some link types, but an inspected namespace component may change before a later path mutation. | Rejected under CCT-01 and CCT-02. |
| POSIX `openat`/`unlinkat`/`renameat` family | POSIX defines directory-relative operations to avoid pathname races. Python exposes `dir_fd` only when the running platform lists each function in `os.supports_dir_fd`; `os.fwalk` is Unix-only. | Promising but not admitted. Exact macOS/Linux end-to-end behavior and failure semantics have not been executed. |
| Linux `openat2` | Linux 5.6+ defines `RESOLVE_BENEATH`, `RESOLVE_NO_SYMLINKS`, `RESOLVE_NO_MAGICLINKS`, and `RESOLVE_NO_XDEV` for constrained resolution. The documented interface has no glibc wrapper, and CPython `os` exposes no `openat2` wrapper. | Monitor. A syscall or extension layer would be a separate native-boundary decision. |
| macOS no-follow surface | CPython documents `O_NOFOLLOW_ANY` as macOS-only in addition to Unix directory-relative functions. | Monitor. Documentation is not installed-host proof, and deletion/quarantine semantics still require adversarial validation. |
| Win32 handles | `CreateFile` can use `FILE_FLAG_OPEN_REPARSE_POINT`, and `SetFileInformationByHandle` can mark an opened handle for deletion with required access. These APIs and their filesystem/version-specific behavior are below Python's portable `os` surface. | Monitor. A Windows adapter requires a separate ABI, identity, reparse, sharing, recovery, and packaging design. |

## Why a capability probe is not added

A boolean such as “supports `dir_fd`” would be incomplete and easy to misuse.
It would not prove all-component resolution, reparse handling, hard-link policy,
same-filesystem quarantine, cross-process exclusion, identity-at-use, durable
receipts, or recovery. A public probe would turn partial environment metadata
into an apparent safety claim before an adapter contract exists.

No command, protocol, root export, environment diagnostic, or CI matrix probe
is added. Future evidence should be produced by explicitly invoked local
adversarial tests and reviewed artifacts before any essential hosted CI change
is proposed.

## Admission evidence required

Each platform implementation proposal must provide:

- exact supported Python, operating-system, filesystem, and primitive inventory;
- an engine-owned adapter contract with explicit acquire/use/close ownership;
- backend-neutral errors and receipts with no descriptor or handle leakage;
- adversarial component swaps, link/junction/reparse and mount substitution,
  hard-link aliases, project/cache overlap, and replacement-object tests;
- concurrent reader/writer, quarantine collision, retry, crash, disk-full,
  permission, restore, and finalize tests;
- installed-wheel proof on a real Windows, macOS, or Linux host for every
  platform claimed as admitted; and
- safe refusal evidence for every missing primitive or unsupported filesystem.

An implementation may support fewer platforms initially only through an
explicit product/support decision. It must not silently reduce the declared
Windows, macOS, and Linux project baseline or add mandatory native compilation.

## Residual risks and non-goals

The decision does not establish retained roots, quiescence, policy, trusted
time, candidate identity, quarantine, receipts, recovery, or cleanup authority.
It adds no runtime API, cache access, deletion, repair, native code, `ctypes`,
dependency, platform adapter, public capability probe, workflow, runner,
permission, release authority, or CI change. Remote cache and networking remain
out of scope.

## References

- [Python `os` filesystem capabilities](https://docs.python.org/3/library/os.html#files-and-directories)
- [Python `shutil.rmtree`](https://docs.python.org/3/library/shutil.html#shutil.rmtree)
- [POSIX `openat`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/open.html)
- [POSIX `renameat`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/rename.html)
- [Linux `openat2`](https://man7.org/linux/man-pages/man2/openat2.2.html)
- [Win32 `CreateFile`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea)
- [Win32 `SetFileInformationByHandle`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfileinformationbyhandle)
- [M147 threat model](cache-cleanup-threat-model.md)
