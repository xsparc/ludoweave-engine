# RFC-0012: External contributor-retention admission readiness

- **Status:** Accepted
- **Date:** 2026-08-07
- **Decision:** Define strict contributor-retention admission and retain the current result as false
- **Related:** [readiness guide](../external-contributor-retention-readiness.md), [first-contribution readiness](0010-external-contributor-rehearsal-admission-readiness.md), [sample-game adoption readiness](0011-external-sample-game-adoption-admission-readiness.md)

## Summary

Add deterministic source, isolated-wheel, and release-bundle evidence for the
design plan's longer-term preference for contributor retention over raw stars.
The reviewed manifest contains no retention records, so the current result
remains false and no retained external contributor is claimed.

M29 defines how a later real return contribution can be admitted. It does not
contact contributors, query GitHub, collect telemetry, invent people or public
records, or treat maintainers, non-human automation, synthetic fixtures, CI,
stars, forks, and downloads as retention.

## Context

M27 defines a strict path for a first independent external contribution, but a
single contribution does not establish retention. Repository popularity also
does not show that a contributor returned. The relevant event is the same
independent external human completing a later, distinct merged project
contribution through the public path.

Identity, independence, same-person continuity, chronology, provenance, and
the meaning of a return are social facts. An offline evaluator can validate
only a deliberately frozen record after human reviewers establish those facts
from public evidence.

## Decision

The external contributor-retention manifest:

1. requires at least one manually reviewed independent external human with a
   first and later return contribution before the result can become true;
2. requires distinct public project issues and merged pull requests for both
   contributions, exact base/head/merge Git identities, canonical merge
   timestamps, valid DCO, reviewed provenance, and the complete clean-setup,
   focused-check, and complete-gate sequence;
3. requires the return merge timestamp to follow the first merge timestamp and
   explicit human review of identity, independence, same-contributor
   continuity, chronology, and retention;
4. records distinct patch and review SHA-256 identities for both contributions
   and rejects cross-role or cross-record reuse; public contributor logins are
   canonicalized case-insensitively before uniqueness checks;
5. permits bounded bug-fix, documentation, feature, maintenance, test, and
   tooling contributions without changing the evaluator's authority;
6. rejects maintainers, non-human automation, unreviewed identity or
   independence, open/unmerged changes, incomplete validation, invalid DCO, unsafe public
   references, duplicate identities, and malformed chronology;
7. preserves every accepted contributor through an executable mandatory exact
   prefix equal to the complete reviewed manifest identity sequence;
8. requires the exact whole-manifest digest to be pinned by reviewed code and
   strict installed evidence; and
9. never counts stars, forks, downloads, traffic, CI actors, project-authored
   fixtures, or synthetic GitHub-shaped records as contributor retention.

Before pinning a nonempty manifest, reviewers verify the contributor's public
identity and continuing independence, the two public issue/PR records, exact
revisions and artifacts, merge chronology, DCO and validation outcomes,
provenance, same-person continuity, and retention conclusion. The evaluator
checks the frozen record but cannot replace that review.

The current normative report is `not-ready`, with zero retained contributors
and reason code `retained-external-contributor-absent`. Synthetic future-state
regressions use nonexistent canonical-shaped project references solely to
prove gate mechanics.

## Security, privacy, and determinism

The evaluator reads one explicitly selected bounded local manifest. It rejects
unknown or duplicate JSON fields, unsafe identities and project references,
invalid Git/SHA/timestamp values, non-human or non-external contributors,
incomplete review and validation, non-merged outcomes, symlinks, oversized
or documents exceeding 16 structural object/array levels, excess records,
duplicate contributors and evidence identities, and incomplete mandatory
history. Canonical timestamps are ASCII UTC values; Unicode digit lookalikes
are rejected.

The public manifest may contain only minimal public provenance: a public
GitHub login, project issue/PR references, Git object IDs, artifact hashes,
canonical public merge timestamps, and bounded review facts. It must not
contain email addresses, credentials, private correspondence, private prompts,
local paths, telemetry, or unpublished personal data. Reports expose only
admitted aggregate counts, scopes, validation steps, reason codes, and the
reviewed manifest digest.

The harness performs no discovery, networking, remote lookup, dynamic import,
installation, subprocess launch, provider execution, telemetry, contributor
contact, issue mutation, or retained-resource lifecycle.

## Consequences

- The contributor-retention metric has an exact artifact-exercised admission
  path but remains zero.
- M27's empty first-contribution rehearsal result and M28's empty external
  sample-game result remain unchanged.
- A real independently reviewed human return contribution is required before
  the result can become true.
- M29 changes no runtime source, public export, wire or persistent format,
  dependency, lock, package version, workflow, CI topology, tag, release, or
  publication.

## Alternatives considered

- **Count stars, forks, downloads, or traffic.** Rejected because popularity is
  not contributor retention and requires mutable remote state or telemetry.
- **Count two pull requests by any account.** Rejected because bots,
  maintainers, duplicate identities, and unreviewed same-person assumptions do
  not establish independent external retention.
- **Query GitHub during CI.** Rejected because mutable remote metadata cannot
  establish identity, independence, provenance, or undisclosed assistance.
- **Store private correspondence or email.** Rejected because only minimal
  public evidence and artifact identities belong in the repository.
- **Count the first contribution alone.** Rejected because M27 already covers
  first-contribution readiness; retention requires a later return.
- **Mark the result true from synthetic tests.** Rejected because fixtures
  prove validation mechanics, not people, contributions, or retention.
