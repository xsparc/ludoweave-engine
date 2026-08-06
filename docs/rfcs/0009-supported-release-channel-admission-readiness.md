# RFC-0009: Supported release channel admission readiness

- **Status:** Accepted
- **Date:** 2026-08-07
- **Decision:** Define strict release-channel admission and retain gate 6 as false
- **Related:** [readiness guide](../supported-release-channel-readiness.md), [release process](../release-process.md), [RFC-0003](0003-retain-experimental-command-receipt-contracts.md), [RFC-0007](0007-cross-version-corpus-admission-readiness.md), [RFC-0008](0008-external-consumer-feedback-admission-readiness.md)

## Summary

Add deterministic source, isolated-wheel, and release-bundle evidence that
distinguishes an established supported feature-release channel from the
project's existing tag-triggered prerelease machinery and local release
candidates. Retain RFC-0003 gate 6 as false because the reviewed manifest has
no release records.

M26 defines how later published facts can be admitted. It does not create or
push a tag, publish a GitHub release, configure or upload to PyPI, change the
package version/workflow, promise support, or promote stability.

## Context

Preview APIs require at least one supported feature release carrying a
deprecation before incompatible removal. A checked-in workflow can describe a
future publication mechanism, but it cannot establish that maintainers have
operated a recurring supported channel. Local release staging and pull-request
CI likewise prove artifacts, not publication or support history.

The current tag workflow is intentionally limited to GitHub prereleases and has
never been invoked by this milestone. PyPI trusted publishing and a
non-prerelease support policy remain separate maintainer decisions.

## Decision

The release-channel manifest:

1. requires at least two reviewed final `MAJOR.MINOR.PATCH` releases on distinct
   major/minor feature lines, each explicitly non-draft and non-prerelease;
2. accepts only canonical, unique, strictly increasing versions with exact
   `vVERSION` tags and Git commit identities;
3. requires the canonical project-tag release URL plus exact artifact and
   release-notes SHA-256 identities;
4. requires the exact `github-release` publication channel, supported status,
   and explicit non-yanked status for every record;
5. preserves the one-supported-feature-release deprecation window from
   `API_COMPATIBILITY.md`;
6. is append-only through an executable mandatory full-record prefix that must
   equal the complete reviewed manifest identity sequence;
7. requires the exact whole-manifest digest to be pinned by reviewed code and
   strict installed evidence; and
8. never treats a local candidate, prerelease workflow, synthetic fixture, CI
   pass, draft release, tag name, download count, or package index reservation
   as a supported feature release.

Before pinning a non-empty manifest, reviewers verify publication, tag and
commit identity, artifact/notes hashes, support and yank status, feature-line
ordering, and continued applicability of the deprecation policy. The offline
tool validates the frozen record but does not replace that review.

The current normative report is `not-ready` with zero releases and reason code
`supported-feature-release-channel-absent`. The synthetic future-state
regression proves only gate mechanics with canonical-shaped project-tag URLs
for nonexistent releases.

## Security, privacy, and determinism

The tool reads one explicitly selected bounded local manifest. Exact fields,
canonical final versions, non-IP HTTPS authorities without query/fragment
components, Git/SHA identities, record count, unique/order constraints,
publication channels, support/yank status, reviewed digest, and mandatory
history fail closed.

Generated reports omit release URLs, commits, artifact and notes hashes, paths,
environment/platform facts, timings, credentials, and provider messages. The
public manifest itself is deliberate reviewed evidence; private release
material must not be copied into it.

The harness performs no discovery, dynamic import, installation, subprocess,
network access, telemetry, repository lookup, global registration, tag
creation, upload, or publication. It is synchronous and retains no external
resource.

## Consequences

- Gate 6 now has an exact, artifact-exercised admission route, but remains
  false.
- Existing release staging and the prerelease workflow continue not to count as
  a supported feature-release channel.
- A recurring final-release history is required before the deprecation promise
  can be considered operable.
- Command/receipt stability remains experimental because gates 1, 2, and 6 are
  false.
- M26 changes no runtime source, public export, wire format, dependency, lock,
  package version, workflow topology, tag, release, or publication.

## Alternatives considered

- **Count the existing tag workflow.** Rejected because mechanism is not
  publication/support history and it currently creates prereleases only.
- **Count local release candidates or hosted CI.** Rejected because neither is
  a consumer-available supported feature release.
- **Require only one final release.** Rejected because one publication does not
  demonstrate a recurring feature channel capable of carrying a deprecation
  before a later incompatible removal.
- **Count two patch releases.** Rejected because patch cadence does not prove
  distinct feature-release lines.
- **Query GitHub or PyPI during CI.** Rejected because admission must be
  deterministic, offline, and resistant to mutable remote state.
- **Publish a release during M26.** Rejected because release authority and
  stability promotion are outside this evidence-only milestone.
- **Promote after defining the harness.** Rejected because the manifest is
  empty, cross-version release execution is absent, and no external feedback
  exists.
