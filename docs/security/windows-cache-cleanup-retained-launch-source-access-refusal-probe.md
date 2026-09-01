# Windows retained launch-source access-refusal probe

**Status:** Accepted M216 current-host test evidence; no cross-principal or
independent-host collection has occurred.

M216 composes one current-host source-access observation with the exact frozen
M212-M215 process, token, session, executable-image, and retained-source
boundary. The probe is Windows-only, test-only, offline, and fixed-purpose. It
neither issues a collection action nor operates on a cache fixture. Criteria 6
and 7 remain unresolved, Windows is not admitted, and cleanup remains
unimplemented and unauthorized.

The retained launch-source access refusal is an observation of two access-only
open requests, not an attempted source mutation.

## Access-only refusal observation

M215 opens the fixed participant source for read access with `FILE_SHARE_READ`
only and retains that handle through participant settlement. M216 requests
write and delete access through separate `CreateFileW` calls while supplying
`FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE` on each competing
request. The broad competing share mode ensures the new request accepts the
retained handle's read access; refusal must therefore come from the retained
handle's omission of write and delete sharing.

Each request uses `OPEN_EXISTING` and performs no content or namespace action.
The only accepted refusal is exact native sharing error 32,
`ERROR_SHARING_VIOLATION`. An unexpected successful handle is closed before
the probe fails. Any other native error category fails closed rather than being
relabelled as sharing refusal.

Both access classes must refuse at three ordered phases:

1. before launch, after the initial retained-source snapshot;
2. after connection, once the exact contained participant and pipe identity are
   established but before the challenge; and
3. after ready, before the release message and while every M215 retained
   identity remains live.

After retained source settlement, when both parent and inherited child source
handles are closed, the same write-access and delete-access opens must succeed
and each resulting handle must close. The source is then reopened read-only and
its normalized name, volume/file identity, bounded size, and SHA-256 must equal
the pre-launch snapshot.

The probe does not attempt write, rename, replace, truncate, or delete. It does
not call a content writer or namespace mutator, and successful post-settlement
access handles are closed without using their granted rights.

## Ownership and failure behavior

Every competing handle that unexpectedly succeeds or is intentionally opened
after settlement is closed exactly once. A close failure is a native failure,
not a passing refusal. M215 continues to own the retained source and standard
handles; M212-M214 continue to own and settle process, thread, Job Object, pipe,
overlapped-I/O, token, and executable-image handles.

The live source snapshot must remain stable before protocol release and again
after the post-settlement access checks. A missing refusal, wrong error
category, missing post-settlement availability, close failure, identity drift,
or content drift invalidates the observation.

## Evidence and authority boundary

This is a same-process cooperative observation of Windows share-mode behavior
on one same-host, same-logon, same-session checkout. Microsoft documents that
share options remain effective until handle close regardless of process
context, but M216 does not run a hostile or alternate-principal competing
process and does not prove resistance to privileged, kernel-mode, backup/
restore, mapped-view, filesystem-filter, or hostile ABA behavior.

Source-commit provenance remains unproved. Imported standard-library module
bytes remain unbound, as do interpreter state, native DLLs, environment values
outside isolated-mode exclusions, and operating-system loader behavior. The
tracked fixture is not mutated, and no cleanup or collection action occurs.

M216 adds no runtime source, public API, CLI or MCP command, production
harness, collector, account lifecycle, privilege transition, filesystem
mutation, network listener, dependency, package payload, version, workflow,
permission, secret, hosted allocation, or admission decision. No public
self-hosted runner is introduced.

## Primary references

- [CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [File security and access rights](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights)
- [Standard access rights](https://learn.microsoft.com/en-us/windows/win32/secauthz/standard-access-rights)
- [System error codes 0-499](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-)
- [Python command-line interface](https://docs.python.org/3/using/cmdline.html)
- [SLSA provenance](https://slsa.dev/spec/v1.2/provenance)
- [GitHub Actions matrix jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
