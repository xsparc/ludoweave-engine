# RFC-0043: Constrain public release output paths

- **Status:** Accepted
- **Date:** 2026-08-11
- **Owners:** LudoWeave maintainers
- **Milestone:** M60

## Context

The M45-M58 portable public-release verifier creates a release document,
download directory, retrieval plan, asset partials, and final asset paths under
one validated runner-owned temporary directory. It already uses exclusive file
creation and hard-link publication for no clobber behavior. Its earlier
preflight checks, however, used `Path.exists()`, which follows the final link
and reports a dangling link as absent. A pre-existing dangling directory entry
could therefore allow network or validator work to begin before the later
exclusive operation rejected the collision.

Python 3.12-3.14 documents `Path.lstat()` as returning the final symbolic
link's own status rather than its target. It also documents `x` mode as
exclusive creation that fails when the file already exists. M60 uses those
public contracts and retains the existing cross-platform `os.link()` final
publication.

## Decision

Before network and before validator side effects, inspect the final
directory entry for the fresh release document, download directory, and
retrieval plan with `Path.lstat()`. Before creating an HTTPS connection, apply
the same check to each requested target and separate asset partial. A regular
file, directory, live link, dangling link, or other existing filesystem entry
is a filesystem collision.

Normal output collisions use `public_release.output_exists`; a fresh retrieval-
plan collision uses `public_release.plan_exists`. If final-entry inspection
fails for a reason other than absence, fail content-silently with the existing
output- or plan-failure taxonomy and retain the local cause only through
exception chaining. Creating the public download directory maps a late
`FileExistsError` to the same output-collision code.

Preflight does not replace exclusive creation. Direct and partial files remain
opened with `x`/`xb`, and final asset publication remains a hard-link create
followed by unlinking the owned partial. These operations retain no clobber
behavior if the path changes after preflight.

## Boundary

M60 is no race-free filesystem guarantee. It does not add directory
descriptors, open-at confinement, a filesystem sandbox, locks, rollback,
deletion on failure, alternate publication, retry, or cleanup behavior. It
does not claim that a concurrently hostile local process cannot replace parent
directories or entries between operations.

M60 adds no workflow, runner allocation, action, permission, trigger,
credential, dependency, lock, version, runtime package/API, release mutation,
release authority, tag, release, or publication. Fixture and pull-request
evidence are not a real public release observation, independent verification,
proof of every delivery path, future availability, immutability, artifact
security, PyPI availability, or a supported channel.

## Consequences

- Every known fresh-output collision fails before network or validator work.
- Dangling links receive the same collision treatment as other directory
  entries.
- Path-inspection errors remain stable and content-silent.
- Exclusive creation and hard-link publication continue to provide no clobber
  behavior after preflight.
- The guarantee is intentionally narrower than race-free local filesystem
  isolation.

## Alternatives considered

- Keep `Path.exists()` preflight only. Rejected because it follows the final
  link and does not identify a dangling link as a collision.
- Depend only on later exclusive creation. Rejected because a known collision
  should fail before network or validator side effects and with the intended
  stable code.
- Resolve the output path. Rejected because resolution follows the final link
  rather than inspecting the directory entry that must remain unused.
- Add descriptor-relative, no-follow filesystem confinement. Deferred because
  portable parent-directory race isolation is a substantially larger design
  and platform-support decision than this bounded collision contract.

## References

- [Python 3.14 `pathlib` status queries](https://docs.python.org/3.14/library/pathlib.html#querying-file-type-and-status)
- [Python 3.14 `open()` modes](https://docs.python.org/3.14/library/functions.html#open)
- [Python 3.14 `os.link()`](https://docs.python.org/3.14/library/os.html#os.link)
