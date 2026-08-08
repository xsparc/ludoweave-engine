# RFC-0021: Enforce distribution reproducibility

- **Status:** Accepted
- **Date:** 2026-08-08

## Context

M6 made release staging deterministic and added checksums, an SPDX SBOM, and a
pinned tag-only provenance workflow. Its unit test proves that staging the same
input wheel and source distribution twice produces the same release directory.
It does not prove that two builds of the same source produce the same wheel and
source archive.

The [Hatch build configuration](https://hatch.pypa.io/latest/config/build/#reproducible-builds)
documents that reproducible-build mode is enabled by default and uses
`SOURCE_DATE_EPOCH` when supplied or an unchanging default timestamp otherwise.
Two clean M37 source builds on Windows produced byte-identical artifacts. That
observation is useful baseline evidence, but a future configuration, backend,
file-selection, permission, or archive-metadata change could regress without
failing the existing release stage.

The project needs an enforcement point that does not add hosted runners,
dependencies, native tooling, credentials, publication authority, or another
artifact format.

## Decision

M38 adds `scripts/verify_distribution_reproducibility.py`. It accepts two
distinct existing build directories and requires each to contain exactly one
`ludoweave-VERSION-py3-none-any.whl` and one matching
`ludoweave-VERSION.tar.gz`. The `.gitignore` file created by uv for an output
directory is ignored only when it is an ordinary file. Symlinks, directories,
additional files, missing artifacts, native/platform wheel tags, inconsistent
names, unreadable files, or differing bytes fail closed.

On success the verifier emits one deterministic
`ludoweave.distribution-reproducibility/1` JSON document containing each name,
byte count, and SHA-256 digest. On a validation or comparison failure it emits
a structured failure document to standard error and exits nonzero. It performs
no network access, installation, import, execution, archive extraction, or
mutation of either build.

The existing Linux pull-request distribution step and the existing tag-release
job each build twice into distinct directories and run the verifier before
installed-wheel smoke, release staging, attestation, or publication. The
repeat build runs inside the already allocated job. M38 adds no workflow job,
runner matrix entry, action, permission, trigger, dependency, cache key, or
credential.

The tag workflow's existing
[GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations)
remain the provenance mechanism. Reproducibility and provenance are
complementary: matching bytes do not identify a trustworthy builder, and an
attestation does not prove that an independent rebuild matches.

## Guarantee boundary

The enforced same-source/same-job claim is narrow: two builds from the same
checked-out source in one validated Linux job must produce byte-identical wheel
and sdist artifacts.
The verifier itself is platform-neutral, and an initial Windows probe matches
two local builds, but M38 does not claim cross-operating-system byte identity,
hermetic dependency resolution, independent rebuilder consensus, source-to-
binary transparency, release publication, or PyPI availability.

The wheel remains pure Python and the package version remains `0.1.0a1`. No
runtime module, public Python API, persistent format, command/receipt protocol,
dependency, lock entry, supported Python/platform contract, or native code is
changed.

## Alternatives rejected

- **Rely only on Hatch's default.** The backend documents reproducible mode,
  but an unexecuted default is not a project acceptance gate.
- **Treat reproducible release staging as sufficient.** Staging repeats fixed
  input bytes and therefore cannot detect nondeterministic wheel or sdist
  creation.
- **Use a separate rebuild runner.** That could support a broader independent
  or cross-platform claim, but would increase hosted allocations and is not
  needed for the bounded regression gate.
- **Replace attestations with digest comparison.** Matching local outputs do
  not establish builder identity or provenance.
- **Set or derive a new timestamp policy in M38.** The current backend already
  produced matching bytes. This milestone enforces the result without changing
  archive timestamps or claiming a new source-date policy.

## Consequences

- Distribution nondeterminism blocks pull-request validation and tagged
  publication before consumers or attestations receive divergent artifacts.
- The Linux distribution step performs one additional build but consumes no
  additional runner allocation.
- Contributors receive exact artifact identities for successful comparisons
  and stable reason codes for failures.
- A future cross-platform or independent-rebuilder claim requires a separate
  accepted proposal and evidence.
