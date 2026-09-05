# RFC-0203: Probe Windows contained source-access source binding

**Status:** Accepted
**Milestone:** M220
**Decision class:** Direction-preserving

## Context

M219 binds a fixed, same-logon, Job-contained contender to the retained
interpreter image selected by its controller. The contender script remains a
pathname argument that the child opens after launch, so that observation does
not bind the executed contender bytes. The smallest next observation is to
retain a fixed contender source before child creation and execute that exact
open file through inherited standard input.

Windows supports explicit inherited-handle allowlists through
`PROC_THREAD_ATTRIBUTE_HANDLE_LIST`. Python isolated mode accepts program text
from standard input without placing a script pathname on the command line.
These primitives permit a bounded source-binding observation without adding a
runtime launcher or a hosted workflow.

## Decision

Adopt the test-only [Windows contained source-access source-binding
probe](../security/windows-cache-cleanup-contained-source-access-source-binding-probe.md).

For each of M218's three live refusal phases, open and snapshot the fixed
contender source before child creation. Rewind that retained source and create
the expected direct `pythonw.exe -I -B -` child suspended. The source is
executed through inherited standard input; the handle allowlist contains
exactly three inherited handles: the read-only source plus two separate
write-only `NUL` handles for standard output and standard error.

Assign the suspended child as the sole member of a private kill-on-close Job,
then preserve M219's same-logon and retained expected/observed interpreter
image agreement. Recheck the retained source snapshot and rewind it before
resume. Require exact zero exit, unchanged source and image snapshots, exact
one-total/zero-active Job settlement, zero owned handles, and ordinary source
access after all retained handles close. The complete M218 three-phase refusal
and M217 participant boundary remains mandatory.

This decision is direction-preserving and makes no collection or cleanup
authority increase. It does not establish source-commit or build provenance.
Imported modules, interpreter/native loader state, distinct-principal and
independent-host behavior, hostile or privileged bypass, criteria 6 and 7,
Windows admission, and cleanup authority remain outside the evidence.

## Consequences

- The new fixed contender bytes are retained before child creation and supplied
  directly as the suspended child's standard input.
- The child receives only the source, output, and error handles explicitly
  admitted by the inherited-handle list.
- M219's interpreter-image binding, M218's access-only command behavior, Job
  containment, and participant phases remain unchanged.
- No runtime, dependency, package, workflow, permission, public runner,
  release, or cleanup surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Continue passing a script pathname

Rejected because the child would resolve and open that pathname after process
creation, leaving the executed bytes outside the retained-source observation.

### Pass source bytes through an anonymous pipe

Rejected because the retained read-only file already supplies a fixed bounded
source object and preserves a directly repeatable post-settlement snapshot.

### Bind imports, a source commit, and a build in the same milestone

Rejected because each is a distinct provenance boundary. Combining them would
overstate this current-host execution-source observation.

### Add a hosted Windows job

Rejected because the current-host test supplies the bounded observation and
the milestone must add zero GitHub Actions jobs or hosted allocation.
