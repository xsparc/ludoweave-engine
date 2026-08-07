# External sample-game adoption readiness

No externally authored sample game is currently admitted. M28 provides an
offline, reviewable path for counting that longer-term adoption metric without
turning project-owned examples, synthetic fixtures, CI, maintainers, or
automated agents into external users.

## What can count

A future record can count only after human review establishes all of these
facts together:

- an independent external author owns a publicly readable sample-game
  repository at an exact immutable Git revision;
- the game is a 2D or layered-2D game, not a benchmark, test fixture, copied
  project example, or maintainer-authored demonstration;
- it uses an installed LudoWeave wheel and exercises headless fixed ticks,
  typed command receipts, and verified replay;
- its run outcome is validated and the exact source, execution evidence, and
  review artifacts have distinct SHA-256 identities;
- its public license and authorship have been manually reviewed;
- its independence, repository provenance, and validated outcome have each
  been explicitly reviewed; and
- it is not owned by this project or authored by a LudoWeave maintainer.

The manifest freezes those reviewed facts. The evaluator checks the frozen
shape, identities, bounded resources, and complete mandatory history. It
cannot discover games, establish authorship or independence, inspect remote
repositories, validate a license, or replace human provenance review.

## Current evidence

The reviewed manifest is exactly 280 bytes and contains zero records. Its
current deterministic report is therefore `not-ready`, with zero games, zero
authors, and reason code `external-sample-game-absent`. The synthetic populated
fixtures in the tests prove only admission mechanics; they are not games,
authors, repositories, users, feedback, or adoption evidence.

Run the source-tree evidence explicitly:

```console
uv run --frozen python examples/external_sample_game_adoption_readiness.py
```

The same evaluator and exact empty manifest run from an isolated wheel and the
deterministic release sample bundle. Generated reports omit author identifiers,
repository locations, revisions, artifact hashes, license identifiers, paths,
platform facts, and timings.

## History and updates

Before a nonempty manifest is accepted, reviewers must pin its complete
ordered identity sequence as the mandatory history and pin the whole-manifest
SHA-256 in the evaluator and installed validator. A reviewed manifest cannot
silently add, drop, replace, reorder, or reuse a prior game, repository,
revision, or artifact identity.

Evidence updates require a normal reviewed pull request. Public source and
review evidence may be referenced, but email, private correspondence,
credentials, private prompts, local paths, telemetry, or unpublished personal
information must not be stored.

## Boundaries

The evaluator performs one bounded synchronous read of an explicitly selected
local JSON document. It uses no networking, telemetry, discovery, dynamic
imports, subprocesses, provider execution, or retained external resources. M28
does not solicit authors, open or mutate issues or pull requests, publish a
package, promote stability, certify a game, or change runtime source, public
APIs, persistent formats, dependencies, the lock, workflows, or CI topology.

See [RFC-0011](rfcs/0011-external-sample-game-adoption-admission-readiness.md)
for the accepted decision.
