# RFC-0206: Bind Git executable selection for the source-commit probe

**Status:** Accepted
**Milestone:** M223
**Decision class:** Direction-preserving

## Context

M221 resolves `git` to an absolute file before each fixed object read, and
M222 excludes lazy object retrieval. Python documents `shutil.which()` as a
`PATH`/`PATHEXT` search on Windows. Repeating that search across the three
participant phases permits the selected executable path to drift during one
observation even though each individual subprocess receives an absolute path.

The retained-source boundary is test-only. The smallest additional evidence is
therefore a scoped composition that holds one resolved path across the complete
M222 boundary without changing M221 or M222 historical evidence.

## Decision

Resolve the Git executable exactly once before the complete M222 observation.
Temporarily bind M221's private executable selector to that absolute file and
observe every direct subprocess command. Require exactly one `PATH`/`PATHEXT`
lookup, all 48 expected fixed Git object reads, and the same selected path as
the first command element for every read.

Preserve M222's command, environment, no-lazy-fetch, no-replacement-object,
no-shell, no-input, timeout, bounded-output, and empty-standard-error rules,
plus the complete M220 retained-source, image, Job, token, access, settlement,
and three-participant boundary.

This decision does not establish executable identity or provenance. It does
not prevent replacement of the file at the selected path, authenticate its
bytes or signer, bind native dependencies or loader state, authenticate the
local object store, or establish source/build provenance, collection, cleanup,
criteria 6/7, or Windows admission.

## Consequences

- One M223 observation cannot select different Git paths between fixed object
  reads because only one ambient executable lookup occurs.
- Every actual child command remains directly observable and begins with the
  selected absolute file.
- M221 and M222 implementation and evidence files remain byte-for-byte
  unchanged.
- No runtime, package, dependency, lock, workflow, permission, public runner,
  release, cleanup, or admission surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Cache the selection globally

Rejected because a module-global cache would broaden lifetime and mutable
state. The observation needs only a scoped per-test binding.

### Hash or verify the selected executable

Rejected because executable content, signing, replacement races, loaded DLLs,
and provenance are separate trust decisions that this slice cannot prove.

### Add hosted artifact attestations

Rejected because GitHub recommends attestations for released artifacts rather
than frequent test builds. They require hosted permissions and allocation and
do not prove this local executable-selection boundary.
