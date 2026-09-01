# RFC-0204: Probe Windows contained source-access source-commit binding

**Status:** Accepted
**Milestone:** M221
**Decision class:** Direction-preserving

## Context

M220 retains a fixed contender source before child creation and executes those
bytes through inherited standard input. That proves a current-host retained
file observation, but the selected bytes are not bound to an immutable
repository object. The smallest next observation is to compare that retained
source with the exact blob in the already validated M220 commit.

Git object plumbing can resolve an exact commit, tree, parent, path, and blob
without consulting a moving branch or remote. This local object observation is
distinct from attesting how the repository was acquired or how a release was
built.

## Decision

Adopt the test-only [Windows contained source-access source-commit binding
probe](../security/windows-cache-cleanup-contained-source-access-source-commit-binding-probe.md).

Before each M220 contained contender runs, resolve the fixed M220 commit and
require its exact object type, tree, sole parent, source path, blob type, blob
size, and blob SHA-256. Compare the committed blob with the snapshot from the
already retained read-only source handle. After child settlement, resolve the
same immutable descriptor again, require it to be unchanged, and compare the
retained source again before close and post-close access validation.

Invoke only a resolved Git executable with fixed arguments, no shell, no
standard input, bounded output, empty standard error, a timeout, replacement
objects disabled, optional locks disabled, prompting disabled, and sanitized
Git-specific environment values. Fail closed on every unexpected result.

This decision is direction-preserving and makes no collection or cleanup
authority increase. It does not establish a SLSA source attestation or build
provenance. The Git executable, local object store, repository acquisition,
imports, native loader, distinct-principal and independent-host behavior,
hostile or privileged bypass, criteria 6 and 7, Windows admission, and cleanup
authority remain outside the evidence.

## Consequences

- The retained M220 contender bytes must equal the blob in one exact immutable
  local commit before every child launch and after every child settlement.
- M220's exact three inherited handles, suspended launch, private Job,
  same-logon token, interpreter image, access refusal, zero exit, settlement,
  and post-close access boundary remains unchanged.
- The check reads only the existing local object database and performs no
  repository or filesystem mutation.
- No runtime, dependency, package, workflow, permission, public runner,
  release, or cleanup surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Bind a moving branch name

Rejected because a branch is mutable and would not identify the exact source
object already validated by M220.

### Treat the local object check as provenance

Rejected because local object identity does not attest repository acquisition,
builder identity, dependency inputs, or artifact production.

### Add a hosted source-attestation workflow

Rejected because attestation and build provenance are separate milestones and
the current decision must not consume hosted allocation or add release
authority.
