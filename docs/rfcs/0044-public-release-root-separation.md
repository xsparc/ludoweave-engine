# RFC-0044: Separate the public release candidate and output root

- **Status:** Accepted
- **Date:** 2026-08-11
- **Owners:** LudoWeave maintainers
- **Milestone:** M61

## Context

The portable public-release verifier accepts an expected candidate directory as
read-only comparison input and creates its public document, plan, download
directory, partials, and final assets beneath a runner-owned output root. M60
rejects pre-existing final output entries, but the two existing directory roots
were validated independently. If the output root was the candidate directory
or a directory beneath it, fresh verifier output could mutate the candidate
before the document validator observed it. A parent symlink or junction could
also make lexically separate roots resolve to that relationship.

Python 3.12-3.14 documents `Path.resolve(strict=True)` as making a path absolute,
resolving symbolic links, and failing when the path does not exist. This public
contract supports bounded static alias comparison, but it does not promise
canonical spelling on every case-insensitive filesystem. `Path.samefile()`
compares filesystem identity and therefore closes that remaining equivalence
gap. Neither operation provides a descriptor-confined or race-free filesystem
sandbox.

## Decision

After each final root is confirmed to be an existing non-symlink directory,
strictly resolve the expected candidate directory and runner-owned output root.
Resolution failure uses the existing content-silent
`public_release.candidate_unavailable` or `public_release.temp_unavailable`
code and retains the local cause only through exception chaining.

Before network side effects and before validator side effects, reject the
output root when its resolved identity equals the resolved candidate directory
or when the output root is a resolved descendant of that candidate. Use stable
`public_release.path_overlap`. Compare the resolved output root and each of its
ancestors to the candidate with `Path.samefile()` as well, so a differently
spelled alias on a case-insensitive filesystem receives the same decision.
Filesystem-identity inspection failure uses content-silent
`public_release.temp_unavailable`. Store the resolved directories in the
validated context so later work uses the identities that were compared.

A candidate directory may remain a separate child of the output root. In that
layout, the fixed document, plan, and download paths are siblings of the
candidate rather than entries beneath it; M60 continues to reject any actual
fixed-path collision. This is a directional ownership rule, not a blanket ban
on both possible ancestry relationships.

## Boundary

M61 is no race-free filesystem guarantee. It does not add directory
descriptors, descriptor-relative or no-follow opens, a directory-descriptor or
general path sandbox, locks, rollback, deletion on failure, cleanup, retry, or
protection against a concurrently hostile local process replacing roots after
validation.

M61 adds no workflow, runner allocation, action, permission, trigger,
credential, dependency, lock, version, runtime package/API, release mutation,
release authority, tag, release, or publication. Fixture and pull-request
evidence are not a real public release observation, independent verification,
proof of every delivery path, future availability, immutability, artifact
security, PyPI availability, or a supported channel.

## Consequences

- The expected candidate directory remains read-only during verifier output.
- Lexically different roots that resolve to the same unsafe relationship fail
  before network or validator work.
- Filesystem-identity-equivalent aliases fail even when resolved spellings
  differ on a case-insensitive filesystem.
- Root-resolution failures remain stable and content-silent.
- A safe candidate child of the output root remains supported.
- M60 final-entry collision and exclusive no-clobber operations remain intact.

## Alternatives considered

- Compare only the supplied path strings. Rejected because a resolved alias can
  hide equality or ancestry.
- Reject ancestry in both directions. Rejected because an output root may
  safely own the candidate as a separate child while writing fixed sibling
  entries.
- Depend on the later release validator to notice candidate mutation. Rejected
  because the read-only ownership failure must occur before network and local
  output side effects.
- Add descriptor-relative, no-follow filesystem confinement. Deferred because
  portable race isolation is a substantially larger platform-support decision
  than this bounded static root-separation contract.

## References

- [Python 3.14 `Path.resolve()`](https://docs.python.org/3.14/library/pathlib.html#pathlib.Path.resolve)
- [Python 3.14 `Path.samefile()`](https://docs.python.org/3.14/library/pathlib.html#pathlib.Path.samefile)
- [RFC-0043: constrain public release output paths](0043-public-release-output-path-conformance.md)
