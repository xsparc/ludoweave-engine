# RFC-0202: Probe Windows contained source-access image binding

**Status:** Accepted
**Milestone:** M219
**Decision class:** Direction-preserving

## Context

M218 observes retained launch-source write/delete sharing refusal from a fixed,
same-logon contender contained in a private Windows Job Object. It deliberately
does not bind that contender to the interpreter image the controller intended
to launch. The smallest next observation is to retain the expected interpreter
file before child creation and compare it with the suspended child's retained
process image before any contender code executes.

Windows exposes a process image name through `QueryFullProcessImageNameW` and
stable same-computer file identity through `FILE_ID_INFO`. A suspended process
therefore allows an access-only, current-host comparison of normalized name,
volume/file identity, bounded size, and SHA-256 before resume. Retained file
handles allow the immutable observations to be checked again after settlement.

## Decision

Adopt the test-only [Windows contained source-access image-binding
probe](../security/windows-cache-cleanup-contained-source-access-image-binding-probe.md).

For each of M218's three live refusal phases, retain and snapshot the expected
direct `pythonw.exe` image before creating the child. Create the fixed contender
suspended, assign it as the sole member of a private kill-on-close Job, and
verify the same-logon token boundary. Before resume, retain the observed process
image and require its normalized name, volume/file identity, bounded size, and
SHA-256 to equal the expected snapshot.

After the child exits successfully, require both retained image file handles to
produce the same identity and byte snapshots they produced before resume. Then
require exact one-total/zero-active Job settlement and zero owned handles. The
full M218 three-phase refusal and M217 participant boundary remains mandatory.

This decision is direction-preserving and makes no collection or cleanup
authority increase. It does not establish source or build provenance. The
contender script bytes, imported standard-library modules, loader state, native
DLLs, distinct-principal behavior, independent-host behavior, privileged
bypass, criteria 6/7, Windows admission, and cleanup authority remain outside
the evidence.

## Consequences

- The fixed contender is bound before resume to the retained interpreter image
  selected by the controller.
- Both expected and observed image file handles remain open through child
  settlement; post-exit stability is read from those handles without relying
  on a post-exit process-name query.
- M218's command, Job membership, same-logon, refusal, settlement, and
  no-mutation boundary remains unchanged.
- No runtime, fixture, dependency, package, workflow, permission, public
  runner, release, or cleanup surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Trust the configured executable path

Rejected because a configured path is intent, not an observation of the image
mapped by the suspended child.

### Query only the process image name

Rejected because path text alone does not bind file identity or bytes. The
probe requires the retained expected and observed file snapshots to agree.

### Bind scripts, imports, or build provenance in the same milestone

Rejected because those are separate trust and provenance boundaries. Combining
them would overstate this current-host interpreter-image observation.

### Add a hosted Windows job

Rejected because the current-host test supplies the bounded observation and the
milestone must add zero GitHub Actions jobs or hosted allocation.
