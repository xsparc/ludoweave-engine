# RFC-0011: External sample-game adoption admission readiness

- **Status:** Accepted
- **Date:** 2026-08-07
- **Decision:** Define strict external sample-game admission and retain the current result as false
- **Related:** [readiness guide](../external-sample-game-adoption-readiness.md), [user guide](../user-guide.md), [RFC-0010](0010-external-contributor-rehearsal-admission-readiness.md)

## Summary

Add deterministic source, isolated-wheel, and release-bundle evidence for the
design plan's longer-term metric counting externally authored sample games. The
reviewed manifest contains no sample-game records, so the current result remains
false and no external adoption is claimed.

M28 defines how a later real game can be admitted. It does not solicit an
author, discover repositories, execute provider code, query mutable remote
state, or treat project-owned examples and synthetic fixtures as external use.

## Context

LudoWeave ships project-owned samples that exercise headless simulation,
commands, receipts, replay, and graphics. Those samples prove project behavior,
not adoption. A green installed-wheel smoke test also cannot establish that an
independent person authored and maintained a game outside this repository.

External authorship, ownership, licensing, and provenance are social and legal
facts. An offline evaluator can validate only a deliberately frozen record
after human reviewers establish those facts from public evidence.

## Decision

The external sample-game manifest:

1. requires at least one manually reviewed game authored by an independent
   external person before the result can become true;
2. permits only 2D and layered-2D games using an installed LudoWeave wheel;
3. requires exact headless-fixed-tick, typed-command-receipt, and
   verified-replay capability evidence with a validated outcome;
4. records a public repository, immutable Git revision, LudoWeave version,
   exact distinct source/execution/review SHA-256 identities, evidence locator,
   and reviewed public SPDX license;
5. requires explicit review attestations for authorship, independence,
   repository provenance, outcome, and licensing;
6. rejects project-owned or maintainer-authored games, unreviewed authorship or
   licensing, mutable or unsafe locators, duplicate games/repositories/
   revisions/evidence locators, and reused artifact identities;
7. preserves every accepted record through an executable mandatory prefix
   equal to the complete reviewed manifest identity sequence;
8. requires the exact whole-manifest digest to be pinned by reviewed code and
   strict installed evidence; and
9. never counts project examples, automated agents, tests, benchmarks,
   synthetic records, CI passes, or unreviewed external claims as adoption.

The current normative report is `not-ready`, with zero games and reason code
`external-sample-game-absent`. Tests may use nonexistent canonical-shaped
references solely to prove future gate behavior.

## Security, privacy, and determinism

The evaluator reads one explicitly selected bounded local manifest. It rejects
unknown or duplicate JSON fields, unsafe identifiers and locators, invalid Git
or SHA identities, incomplete capability coverage, nonvalidated outcomes,
unreviewed authorship or licenses, project/maintainer ownership, symlinks,
oversized documents, excess records, and incomplete history.

The public manifest may contain only minimal public provenance. It must not
contain email addresses, private correspondence, credentials, private prompts,
local paths, telemetry, or unpublished personal data. Reports expose only
aggregate counts, declared scopes, versions, capabilities, outcomes, and the
reviewed manifest digest.

The harness performs no discovery, networking, remote lookup, dynamic import,
installation, subprocess launch, provider execution, telemetry, author
contact, issue mutation, or retained-resource lifecycle.

## Consequences

- The externally authored sample-game metric has an exact artifact-exercised
  admission path, but remains zero.
- Project-owned samples remain behavioral evidence and are never reclassified
  as external adoption.
- A real independently authored, publicly reviewable, validated game is
  required before the result can become true.
- M28 changes no runtime source, public export, wire or persistent format,
  dependency, lock, package version, workflow, tag, release, or publication.

## Alternatives considered

- **Count LudoWeave's bundled games.** Rejected because project ownership is
  not external adoption.
- **Count stars, clones, or downloads.** Rejected because those mutable totals
  do not prove an authored game and would require telemetry or remote state.
- **Search GitHub automatically.** Rejected because discovery cannot establish
  authorship, provenance, licensing, or compatibility and introduces network
  nondeterminism.
- **Count an automated-agent game.** Rejected because project-directed
  automation is not independent external authorship.
- **Accept a source-tree-only demo.** Rejected because the adoption metric must
  exercise the supported installed boundary rather than repository internals.
- **Mark the result true from synthetic tests.** Rejected because fixtures
  prove evaluator mechanics, not users or adoption.
