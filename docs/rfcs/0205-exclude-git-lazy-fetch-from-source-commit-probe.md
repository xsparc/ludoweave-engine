# RFC-0205: Exclude Git lazy fetch from the source-commit probe

**Status:** Accepted
**Milestone:** M222
**Decision class:** Corrective, direction-preserving

## Context

M221 describes its fixed Git object reads as offline. Git can nevertheless
retrieve a missing object from a configured promisor remote on demand unless
lazy fetching is disabled. Sanitizing Git-specific environment values,
disabling prompts, and naming an exact object do not by themselves exclude
that transport path.

The object reader is test-only and otherwise has the intended bounded,
read-only shape. The smallest correction is therefore to exclude lazy fetch at
that existing invocation boundary rather than introduce another reader or a
network-control mechanism.

## Decision

Pass both the command-line option and environment variable documented by Git:
`--no-lazy-fetch` and `GIT_NO_LAZY_FETCH=1`. Strip ambient `GIT_*` values before
installing the fixed environment value, and place the global option before
`-C` and the object-plumbing arguments.

Add a Windows-only regression that executes the complete M221 boundary, spies
on the direct subprocess invocation, and proves an ambient lazy-fetch override
and object-directory value cannot enter the child environment. Preserve
M221's timeout, bounded output, empty-standard-error, no-shell, no-input,
replacement-object, optional-lock, and prompt exclusions.

This is a corrective, direction-preserving change to the current tree.
Historical M221 evidence is not rewritten. It does not establish a SLSA source
attestation or build provenance, authenticate the Git executable or object
store, attest repository acquisition, or grant collection, cleanup, or
admission authority.

## Consequences

- The fixed Git reader refuses on-demand retrieval of missing promisor objects
  through both supported exclusion forms.
- Existing local objects remain readable through the exact M221 commit and
  blob checks.
- The correction changes two lines of the M221 reader and adds only tests and
  documentation.
- No runtime, package, dependency, lock, workflow, permission, public runner,
  release, or cleanup surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Rely on noninteractive mode

Rejected because disabling prompts does not categorically disable a configured
noninteractive promisor fetch.

### Depend only on the current repository configuration

Rejected because repository acquisition and partial-clone configuration are
outside the M221 evidence boundary.

### Add hosted provenance or attestation work

Rejected because source and build provenance are distinct future decisions and
would add hosted permissions and allocation unrelated to this correction.
