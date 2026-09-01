# Windows retained launch-source binding probe

**Status:** Accepted M215 current-host test evidence; no cross-principal or
independent-host collection has occurred.

M215 composes one current-host launch-source observation with the exact frozen
M212-M214 process, token, session, and executable-image boundaries. The probe
is Windows-only, test-only, offline, and fixed-purpose. It neither issues a
collection action nor operates on a cache fixture. Criteria 6 and 7 remain
unresolved, Windows is not admitted, and cleanup remains unimplemented and
unauthorized.

## Retained launch source

Before participant launch, the controller opens the fixed M212 participant
source through a retained launch-source handle with read-only access. It takes
a private snapshot of the normalized name, volume and file identifiers, size,
and SHA-256 through that handle, then rewinds the handle to offset zero.
The inherited M214 read bounds apply: the source must be non-empty and no
larger than 64 MiB, and hashing uses fixed 64 KiB chunks.

The controller creates the child directly as `pythonw.exe -I -B -` plus the
private control-pipe name. The participant source bytes are read from inherited
standard input, so no participant script pathname is placed on the child
command line or reopened by Python. Isolated mode ignores `PYTHON*` environment
settings and excludes the script directory and user site; bytecode writing is
disabled.

`STARTUPINFOEXW` and `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` constrain inheritance
to an exact three-handle allowlist: the read-only source handle is standard
input, and two separate write-only `NUL` handles are standard output and
standard error. Each handle is distinct, positive, and marked solely
inheritable before `CreateProcessW`; no other handle is intentionally inherited.
The two parent `NUL` handles close after successful participant startup. The
source handle remains owned through settlement.

After M212 binds the connected pipe client to the retained participant process,
M213 revalidates token/session identity, and M214 binds the fixed executable
image, the controller observes challenge/ready. Before release, it repeats the
retained-token and both executable-image checks and snapshots the same retained
source handle. Native client/session/DACL checks remain required before the
challenge. Any source name, file identity, size, or digest change fails closed
before release.

## Ownership and failure behavior

Every new handle is explicitly owned and closed once. Attribute-list storage
and its handle array remain alive through `CreateProcessW` and are released
immediately afterward. M212 continues to own process, thread, Job Object, pipe,
and overlapped-I/O settlement; M213 owns query-only token handles; M214 owns
the expected and observed executable-image handles.

The source is opened without write or delete sharing. This temporarily refuses
cooperative write/delete opens while the retained handle is live, but it grants
no mutation or cleanup authority. Invalid source identity, bounds, inheritance,
pipe shape, launch, challenge, or before-release stability fails closed.

## Evidence and authority boundary

This observation binds the fixed participant source file object and bounded
content used as Python standard input. Imported standard-library module bytes
remain unbound, as do interpreter state, native DLLs, environment values not
ignored by isolated mode, and operating-system loader behavior. Source-commit
provenance remains unproved. The retained handle reduces pathname re-open
ambiguity, but this cooperative current-host probe does not prove hostile ABA
resistance.

This is one same-host, same-logon, same-session observation. It does not prove
a distinct authenticated principal, independent host, trusted source checkout,
account or credential custody, fixture mutation, interruption durability,
collection, or cleanup. It is not qualifying M206 or M208 evidence and cannot
resolve criteria 6 or 7.

M215 adds no runtime source, public API, CLI or MCP command, production
harness, collector, account lifecycle, privilege transition, filesystem
mutation, network listener, dependency, package payload, version, workflow,
permission, secret, hosted allocation, or admission decision. No public
self-hosted runner is introduced.

## Primary references

- [UpdateProcThreadAttribute](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute)
- [Handle inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [GetHandleInformation](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-gethandleinformation)
- [STARTUPINFOW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfow)
- [CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Python command-line interface](https://docs.python.org/3/using/cmdline.html)
- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
