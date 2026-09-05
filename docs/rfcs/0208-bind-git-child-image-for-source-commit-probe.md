# RFC-0208: Bind each Git child process image for the source-commit probe

**Status:** Accepted
**Milestone:** M225
**Decision class:** Direction-preserving

## Context

M223 proves that every fixed Git command begins with one selected absolute
path. M224 retains that selected executable file and holds its stable identity
and content across all 48 commands. Neither milestone observes the executable
image created for an actual Git child process.

A direct post-launch query has a race because these object reads are
short-lived. Windows provides `CREATE_SUSPENDED` as a creation-time boundary:
the primary thread cannot run until `ResumeThread` reduces its initial suspend
count to zero.

## Decision

Bind each Git child process image while composing the complete M224 boundary.
Intercept CPython's Windows `CreateProcess` call only inside the test, add
`CREATE_SUSPENDED`, and use the returned process handle to open a retained
image observation before its primary thread runs.

Require each observed image's normalized name, volume/file identity, positive
bounded size, and SHA-256 to equal the retained M224 executable snapshot.
Require the primary thread's previous suspend count to be exactly one, then
resume it and return the original process/thread handles to CPython's normal
`Popen` ownership. Retain every observed image file until all 48 fixed Git
object reads settle, recheck each snapshot, and close in reverse order.

If observation or resume fails before `CreateProcess` returns ownership,
terminate and wait for the suspended process, close its thread and process
handles, close any retained image, and propagate failure.

This decision does not establish executable authenticity or provenance. It
does not prove a signer, publisher, ACL trust, native DLL or loader identity,
repository acquisition, local-object-store trust, or source/build provenance.
It does not admit Windows or authorize cleanup.

## Consequences

- Each actual Git process image is compared with the already-retained M224
  executable before child code can run.
- M221 through M224 evidence remains byte-for-byte unchanged.
- The composition depends on CPython's private Windows `CreateProcess`
  plumbing and is validated only across the supported CPython 3.12-3.14
  matrix; it is not a public API dependency.
- No runtime, package, dependency, lock, workflow, permission, fixture,
  example, script, benchmark, cleanup, or admission surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Query each `Popen` after construction

Rejected because a short-lived Git process can exit before the image-name
query, making the observation timing-dependent.

### Open each process again by PID

Rejected because PID lookup introduces an avoidable lifetime and reuse race
when the original creation handles are already available.

### Add hosted provenance attestations

Rejected because provenance is a broader authority claim and would add hosted
permissions and allocation without proving this local child-image boundary.
