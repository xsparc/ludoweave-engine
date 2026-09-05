# RFC-0198: Probe Windows retained launch-source binding

**Status:** Accepted
**Milestone:** M215
**Decision class:** Direction-preserving

## Context

M212 binds a connected local control client to a retained participant process.
M213 binds that process to the expected same-logon primary token and session.
M214 binds its executable image to a fixed direct `pythonw.exe`. Those results
do not prove which Python source bytes the process executed because the earlier
launch still supplied a script pathname for Python to reopen.

Windows supports explicit inherited-handle selection with
`PROC_THREAD_ATTRIBUTE_HANDLE_LIST`. CPython accepts program source from
standard input with `-`, while `-I` and `-B` reduce ambient import and bytecode
effects without requiring command-line or remote-process-memory introspection.

## Decision

Adopt the test-only [Windows retained launch-source binding
probe](../security/windows-cache-cleanup-retained-launch-source-binding-probe.md).

Open and retain the fixed M212 participant source before launch. Snapshot its
private normalized name, volume/file identity, bounded size, and SHA-256, then
rewind it. Launch fixed direct `pythonw.exe -I -B -` and the private pipe name,
with the retained source as standard input and two write-only `NUL` handles as
the exact explicit three-handle inheritance list. Do not place the participant
path on the command line.

After the exact M212-M214 bindings and challenge/ready observation, require the
same retained source, retained token, and expected/observed executable-image
handles to remain stable before release. Keep all identity values private and
close every owned handle once.

This decision is direction-preserving and makes no collection or cleanup
authority increase. No distinct-principal or independent-host run has occurred,
criteria 6 and 7 remain unresolved, Windows remains unadmitted, and cleanup
remains unimplemented and unauthorized.

## Consequences

- A later private harness proposal can require retained launch-source binding
  in addition to the frozen process, token, session, and executable-image
  observations.
- The participant executes the retained source bytes from inherited standard
  input rather than reopening a script pathname.
- Imported modules, interpreter state, native dependencies, source-commit
  provenance, and hostile ABA resistance remain unproved.
- Local validation adds zero GitHub Actions jobs or hosted allocation.
- Fixture mutation, power interruption, collection custody, criteria 6/7, and
  Windows admission remain separate work.

## Alternatives rejected

### Trust a script path on the child command line

Rejected because Python would reopen the name after launch, leaving an
unobserved lookup interval between the controller's source check and execution.

### Inspect the child command line through native process internals

Rejected because remote PEB/process-parameter memory layouts are unnecessary
and unstable for this boundary. The fixed controller-owned command line and
retained standard-input handle are directly observable.

### Add a product collector or hosted Windows job

Rejected because M215 is a local design-risk probe. It makes no collection or
cleanup authority increase and adds zero GitHub Actions jobs or hosted
allocation.
