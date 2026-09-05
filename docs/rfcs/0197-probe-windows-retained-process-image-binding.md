# RFC-0197: Probe Windows retained process-image binding

**Status:** Accepted
**Milestone:** M214
**Decision class:** Direction-preserving

## Context

M212 proves that a connected local control client is the retained participant
process. M213 proves that process retains the expected same-logon primary token
and session through challenge/ready. Neither milestone binds the executable
image reported by the retained process handle to the fixed direct executable
selected before launch.

Windows exposes a process image name through a retained process handle and
stable file identity through a separately retained read-only file handle. A
bounded file digest adds content comparison without adding a product collector
or serializing host identity.

## Decision

Adopt the test-only [Windows retained process-image binding
probe](../security/windows-cache-cleanup-retained-process-image-binding-probe.md).

Open and retain the fixed expected `pythonw.exe` before launch. After the exact
M212 process binding and M213 token/session checks, query the executable name
from the retained process handle, open that file read-only, and retain its
handle through challenge/ready. Compare private normalized names, volume and
file identifiers, bounded sizes, and SHA-256 digests before the challenge.
Require both retained file snapshots to remain stable after `ready` and before
`release`.

The maximum image size is 64 MiB and reads use fixed 64 KiB chunks. Identity
values remain private. This decision is direction-preserving and makes no
collection or cleanup authority increase. No distinct-principal or
independent-host run has occurred, criteria 6 and 7 remain unresolved, Windows
remains unadmitted, and cleanup remains unimplemented and unauthorized.

## Consequences

- A later private harness proposal can require executable-image binding in
  addition to the frozen process, pipe, token, and session observations.
- An executable path string alone is insufficient; retained file identity,
  bounded content, and before-release stability must agree.
- The probe does not bind the loaded Python script, imports, command line,
  environment, or interpreter state and does not prove hostile ABA resistance.
- Local validation adds zero GitHub Actions jobs or hosted allocation.
- Fixture mutation, power interruption, collection custody, criteria 6/7, and
  Windows admission remain separate work.

## Alternatives rejected

### Trust the launch path or queried image name alone

Rejected because path aliases and replacement can make a string-only check
ambiguous. The retained expected and observed handles must identify matching
bounded content.

### Serialize executable identity as evidence

Rejected because local names, file IDs, sizes, digests, and handles are not
needed outside the pass/fail observation and could disclose host details.

### Add a product collector or hosted Windows job

Rejected because M214 is a local design-risk probe. It makes no collection or
cleanup authority increase and adds zero GitHub Actions jobs or hosted
allocation.
