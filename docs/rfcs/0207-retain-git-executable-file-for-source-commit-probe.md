# RFC-0207: Retain the Git executable file for the source-commit probe

**Status:** Accepted
**Milestone:** M224
**Decision class:** Direction-preserving

## Context

M223 resolves one absolute Git executable path and uses that selection for all
48 fixed object reads in the complete M222 observation. The selected file can
still be opened for replacement access between resolution and a later child
launch because M223 retains only the path.

Windows documents that a file handle's share modes remain effective until the
handle is closed. Omitting write and delete sharing from one retained read
handle therefore provides a bounded local observation of the selected file
without changing the historical M221-M223 evidence.

## Decision

Retain the selected Git executable file through one non-inheritable read-only
handle before entering the complete M223 boundary. Permit only
`FILE_SHARE_READ`, snapshot the normalized path, volume/file identity,
positive bounded size, and SHA-256 digest, and require the same snapshot after
all 48 fixed Git object reads.

Exercise the identical retainer against its own writable test source using
access-only competing opens. Require write and delete/rename access to fail
with the exact Windows sharing-violation category while that handle is
retained. After closing the handle, require both access categories to settle
and require a fresh file snapshot to equal the retained snapshot. The access
probe is separate because installed Git executables may be independently
protected by host ACLs that return access denied before share evaluation.

Perform the real `PATH`/`PATHEXT` lookup exactly once before retention. Scope a
fixed selector around M223 so M223's existing observer still proves that every
actual Git child command uses the same path.

This decision does not establish executable authenticity or provenance. It
does not prove a signer, publisher, ACL trust, actual child-process image,
native DLL or loader identity, repository acquisition, local-object-store
trust, or source/build provenance. It does not admit Windows or authorize
cleanup.

## Consequences

- The selected executable is held by the same read/share mode whose ordinary
  write, delete, and rename exclusion is demonstrated without mutating a file.
- The retained handle is not inherited by Git children and closes even when
  the inherited boundary raises or skips.
- M221, M222, and M223 evidence remains byte-for-byte unchanged.
- No runtime, package, dependency, lock, workflow, permission, fixture,
  example, script, benchmark, cleanup, or admission surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Copy Git into a private directory

Rejected because copying an executable adds filesystem mutation, provenance
questions, and a new cleanup obligation without proving native dependency
identity.

### Validate a code signature

Rejected because signer and publisher policy is a separate trust decision and
would not bind the local object store, loaded DLLs, or source provenance.

### Add hosted artifact attestations

Rejected because build attestations require additional hosted permissions and
allocation and do not prove this local executable-file retention boundary.
