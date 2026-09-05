# RFC-0219: Portable Git source-probe fixture

**Status:** Accepted
**Milestone:** M236
**Decision class:** Approved test-evidence portability repair

## Context

The M236 publication audit reproduced an M221 failure in a depth-one checkout.
The Windows CI checkout lacks the exact M220 commit object needed by the
historical source probe. Full-depth fetching would not solve the requested
squash-merge lifecycle: the original commit is not an ancestor of the squash.
The maintainer explicitly approved a portability repair preserving real binding
assertions, offline operation, and the existing three-job CI.

## Decision

Make the object-store input to M221-M235 explicit at pytest composition time.
Every Windows test in that source-commit family uses a fresh session-owned
partial bare object database populated from a pinned, bounded data-only fixture.
The fixture contains five original objects: the M220 commit, the three trees
on the fixed source path, and its blob. The parent ID remains a verified field
of the original commit; its object contents were never consumed by this probe.

Verify the complete fixture's SHA-256 before decoding, verify the exact object
inventory and each Git SHA-1 identity, then write loose objects only beneath a
new pytest-owned destination. An existing destination refuses. No remotes,
hooks, alternates, inherited repository settings, fetch, moving refs, or copied
working-tree files are used to construct the database.

The integration fixture redirects only the metadata repository path. It does
not mock subprocess results, native handles, signer data, retained source
bytes, or receipts. All existing native probes remain byte-for-byte unchanged.
They continue to execute real sanitized Git reads,
check commit/tree/parent/path/type/size/digest identities, compare the retained
contender bytes before and after execution, and enforce native process and
resource boundaries. Setup failure fails tests; there is no skip or fallback.

## Evidence interpretation

Hosted qualification also exposed two legacy portability defects. M159's
already Windows-only test must be excluded before import on non-Windows hosts,
because it imports `msvcrt` before pytest evaluates its platform marker. Its
Windows execution and assertions remain intact.

M153-M235 tree guards used the host-dependent ordering of `Path` objects. They
now sort by case-folded path-component tuples, with exact component tuples as
the tie-breaker. Names and payload bytes entering the digest are not normalized
or excluded. The existing protected-tree digests are unchanged. Only the
ordering expression and dependent guard-file hash pins change in those 83
files. A regression runs every affected guard against both path flavours and
opposite input orders, retaining mixed-case names and directory/file ordering.

This supersedes RFC-0204's assumption that automated runs read the developer's
existing checkout object database. Automated results now mean that current-host
native execution binds retained bytes to the pinned historical **fixture**.
They do not demonstrate ancestry or acquisition of the current checkout.
Historical results retain their original context and are not reclassified.

The deliberately partial database is not a clone, complete archive, release
artifact, provenance store, or generally connected Git history. Unrelated tree
entries and commit ancestry are intentionally absent. Its raw objects retain
their original identities; neither a synthetic commit nor a fabricated
historical identity replaces M220. Git object IDs are format identities, not
an authenticity claim. Windows cleanup remains unimplemented and unauthorized.

## Validation and non-goals

Test real Git traversal, missing required objects, corrupt or drifted commit/
blob content, manifest bounds/identity, destination refusal, fixture wiring,
and both shallow and squash-style checkouts. Run the inherited probe family
and repository gates without changing assertions. Existing platform skips
remain platform skips; absence of historical checkout objects is not skipped.

No runtime code, public API, dependency, compiler, lock, workflow, CI allocation,
network fallback, release, cleanup authority, or merge-policy change is added.
The fixture and composition code belong to tests, not the installed wheel.

## References

- [Git repository layout](https://git-scm.com/docs/gitrepository-layout)
- [Git loose-object format](https://git-scm.com/docs/gitformat-loose)
- [Checkout action: default single-commit fetch](https://github.com/actions/checkout)
- [GitHub pull-request merge methods](https://docs.github.com/en/pull-requests/reference/pull-request-merges)
