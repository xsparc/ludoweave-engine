# Windows contained source-access source-commit Git child process-image binding probe

**Status:** Accepted M225 current-repository test evidence; executable
authenticity, source/build provenance, cross-principal proof, independent-host
proof, cleanup authority, and Windows admission have not occurred.

M225 composes a Windows-only, test-only Git child process-image binding around
M224's complete retained-executable observation. It performs no cache-fixture
operation and issues no cleanup.

## Suspended child-image binding

The probe performs one real Git lookup and opens the retained M224 executable
before child creation. Each of the existing 48 CPython Windows
`CreateProcess` calls receives `CREATE_SUSPENDED`. Windows therefore prevents
the primary thread from running while the returned process handle is used to
query and retain the actual executable image.

Each observed snapshot contains the normalized image name, volume serial, file
identifier, positive bounded size, and SHA-256. It must equal the retained M224
executable snapshot before its primary thread runs and before `ResumeThread`
is called. The previous suspend count must be exactly one. The original handles
are then returned to CPython's normal `Popen` ownership, so the inherited
timeout, output, and settlement behavior remains mandatory.

All 48 retained child-image files remain open until all 48 fixed Git object
reads have settled. Their snapshots and the retained M224 executable are
checked again before reverse-order close, followed by a fresh shared executable
snapshot after the M224 handle closes. Observation or resume failure before
ownership transfer terminates and waits for the suspended child and closes the
process, thread, and retained-image handles.

M223's one-path selector and exact subprocess count remain mandatory. M222's
no-lazy-fetch, no-replacement-object, sanitized-environment, no-shell,
no-input, timeout, bounded-output, and empty-standard-error rules remain in
force. The full M220 retained-source, image, Job, token, access, settlement,
and participant boundary also remains mandatory.

## Evidence and authority boundary

This is Git child process-image binding to the retained M224 executable only.
It does not authenticate the executable, a signer, publisher, origin, ACL, or
security descriptor. Native DLL and loader identity remain outside, and the
local object store remains outside the trust boundary.

This is not a source provenance attestation, and build provenance remains
unproved. Repository acquisition, imported modules, distinct-principal
behavior, hostile or privileged bypass, independent-host evidence, and
debugger/kernel resistance remain unbound. Criteria 6 and 7 remain unresolved.
Windows is not admitted, cleanup remains unimplemented and unauthorized, and
no public self-hosted runner is introduced.

M225 adds no runtime source, public API, CLI or MCP command, production
harness, collector, credential lifecycle, filesystem mutation, network
listener, dependency, package payload, version, workflow, permission, secret,
hosted allocation, cleanup action, or admission decision.

## Primary references

- [Microsoft: suspending thread execution](https://learn.microsoft.com/en-us/windows/win32/procthread/suspending-thread-execution)
- [Microsoft: `QueryFullProcessImageNameW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-queryfullprocessimagenamew)
- [Microsoft: `ResumeThread`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-resumethread)
- [Microsoft: `TerminateProcess`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)
- [Python subprocess reliability](https://docs.python.org/3/library/subprocess.html)
- [CPython 3.12 subprocess implementation](https://github.com/python/cpython/blob/3.12/Lib/subprocess.py)
- [CPython 3.13 subprocess implementation](https://github.com/python/cpython/blob/3.13/Lib/subprocess.py)
- [CPython 3.14 subprocess implementation](https://github.com/python/cpython/blob/3.14/Lib/subprocess.py)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
- [NIST SSDF publications](https://csrc.nist.gov/Projects/ssdf/publications)
