# RFC-0013: Installation-matrix admission readiness

- **Status:** Accepted
- **Date:** 2026-08-07
- **Decision:** Define strict published-wheel installation-matrix admission and retain the current result as false
- **Related:** [readiness guide](../installation-matrix-readiness.md), [release process](../release-process.md), [supported release-channel readiness](0009-supported-release-channel-admission-readiness.md)

## Summary

Add deterministic source, isolated-wheel, and release-bundle evidence for the
design plan's longer-term installation-success metric. The reviewed manifest contains no installation records,
so the current result remains false and no published-wheel matrix success is
claimed.

M30 defines how later real clean-install evidence can be admitted. It does not
publish or download a release, query GitHub, run remote jobs, collect telemetry,
or treat source-checkout CI, local builds, maintainers, automation, or synthetic
fixtures as released-user installations.

## Context

The supported Python and platform contract is already tested in pull-request
CI, and release smoke installs a locally built wheel. Those gates establish
development compatibility. They do not establish that one immutable public
release wheel was installed cleanly across the supported matrix after
publication.

Artifact provenance, publication, clean-environment conditions, runner
identity, and successful execution are external facts. An offline evaluator
can validate only a deliberately frozen record after reviewers establish those
facts from public evidence.

## Decision

The installation-matrix manifest:

1. requires one complete seven-environment matrix covering Ubuntu CPython
   3.12/3.13/3.14 and macOS/Windows CPython 3.12/3.14;
2. requires every record to name the same canonical public project release,
   universal pure-Python wheel URL, release version/tag, and wheel SHA-256;
3. requires a fresh isolated environment, installation from the release wheel,
   no dependencies, and no native compiler;
4. requires installed version, doctor, `hello_headless`, and headless
   Clockwork Arena checks to pass in exact order;
5. requires canonical CPython patch versions, platform/environment agreement,
   successful outcomes, distinct canonical public project validation-job
   locations and installation-log SHA-256 identities, canonical ASCII UTC
   timestamps, and reviewed provenance and validation;
6. rejects partial or duplicate environments, artifact drift, duplicate logs,
   unsafe or non-project locations, malformed values, unreviewed facts, and
   failed or incomplete checks;
7. preserves every accepted environment as a complete executable mandatory
   prefix equal to the reviewed manifest identity sequence;
8. requires the exact whole-manifest digest to be pinned by reviewed code and
   strict installed evidence; and
9. never counts source-checkout tests, local builds, synthetic fixtures, CI job
   count, downloads, or package-index metadata as installation success.

Before pinning a nonempty manifest, reviewers verify the public release and
asset, immutable wheel identity, exact matrix, isolation conditions, absence of
dependencies/native compilation, check outputs, log identities, provenance,
and validation conclusion. The evaluator checks the frozen record but cannot
replace that review.

The current normative report is `not-ready`, with zero successful environments
and reason code `installation-matrix-evidence-absent`. Synthetic future-state
regressions prove gate mechanics only.

## Security, privacy, and determinism

The evaluator reads one explicitly selected bounded local manifest. It rejects
unknown or duplicate JSON fields, non-project release/asset locations,
incompatible environment identities, invalid versions/hashes/timestamps,
unreviewed provenance, failed checks, symlinks, oversized documents, documents
exceeding 16 structural object/array levels, excess records, duplicate
environments/logs, artifact drift, and incomplete mandatory history.

The public manifest may contain only canonical public project artifact and
validation-job locations, CPython/platform identifiers, immutable hashes,
canonical public validation timestamps, and bounded review facts. It must not contain
credentials, private logs, local paths, prompts, telemetry, hostnames, IP
addresses, or unpublished user data. Reports expose only admitted aggregate
counts, environment IDs, release versions, required checks, reason codes, and
the reviewed manifest digest.

The harness performs no discovery, networking, remote lookup, dynamic import,
installation, subprocess launch, provider execution, telemetry, release
mutation, or retained-resource lifecycle.

## Consequences

- Installation success has an exact artifact-exercised admission path but
  remains unproven.
- Existing source and locally built wheel CI remain engineering evidence, not
  public-release installation evidence.
- A real immutable public release and complete reviewed clean-install matrix
  are required before the result can become true.
- M30 changes no runtime source, public export, wire or persistent format,
  dependency, lock, package version, workflow, CI topology, tag, release,
  publication, certification, or support promise.

## Alternatives considered

- **Count the pull-request matrix.** Rejected because it validates source and
  locally built artifacts before publication.
- **Count wheel builds.** Rejected because building an artifact is not a clean
  installation of one immutable public asset.
- **Query GitHub during CI.** Rejected because mutable remote state and network
  availability would make the evidence nondeterministic.
- **Record private runner logs.** Rejected because only minimal public evidence
  and immutable log identities belong in the repository.
- **Mark the result true from synthetic tests.** Rejected because fixtures
  prove validation mechanics, not released installations.
