# RFC-0042: Adopt tool-neutral repository metadata

- **Status:** Accepted
- **Date:** 2026-08-11
- **Owners:** LudoWeave maintainers
- **Milestone:** M59

## Context

LudoWeave already uses purpose-based maintenance paths and neutral branch
names. A review after M58 found that the current tracked tree still retained a
small runtime-test fixture label plus historical maintenance records and
duplicated absence guards carrying retired tooling-specific identity markers.
Those strings were not engine behavior, attribution authority, or required
release evidence, but their continued presence conflicted with the repository
metadata convention.

Historical commit objects, pull-request identities, commit hashes, authorship,
and DCO trailers remain the authoritative provenance record. Rewriting that
history would be destructive and is outside this maintenance decision.

## Decision

The current tracked tree uses role-, purpose-, product-, and milestone-based
metadata rather than retired tooling-specific identity labels.

Current project records replace obsolete branch and control-path labels with
explicit descriptive redactions while retaining commit, tree, pull-request,
workflow, test, artifact, and timing evidence. One schema-test actor becomes a
neutral fixture identity. Three duplicated root-path checks are consolidated
into one architecture guard.

The consolidated guard checks both conditions:

- retired root control paths remain absent, including untracked paths; and
- tracked plus non-ignored working-tree text contains none of the retired
  identity markers.

The marker set is represented without printing its decoded values in tracked
source. This is a disclosure convention, not a security boundary or a claim
that immutable repository history no longer contains earlier labels.

Product-facing agent terminology remains unchanged because it describes a
public engine capability, protocol, example, or metric rather than repository
tooling provenance.

## Boundary

M59 changes current-tree repository metadata, test fixtures, documentation,
and architecture enforcement only. It does not rewrite Git history, change
authors or DCO evidence, delete Git objects, alter runtime source, change a
public API or protocol, modify a workflow, allocate a new CI topology, add a
dependency, change the lock, change the package version, publish a release, or
alter release authority.

The absence guard is limited to the repository working tree. It is not a
forensic erasure claim for clones, forks, logs, pull-request databases,
artifact caches, or immutable commit history.

## Consequences

- Current repository text follows one enforceable tool-neutral convention.
- Historical technical evidence remains useful through stable commit, PR,
  workflow, artifact, test, and timing identities.
- Maintainers can discuss engine agents normally without implying tooling
  provenance.
- Future tracked or non-ignored working-tree regressions fail a focused
  architecture test.

## Alternatives considered

- Rewrite Git history. Rejected as destructive and unnecessary for a
  current-tree convention.
- Delete historical evidence wholesale. Rejected because exact technical and
  validation facts remain valuable.
- Keep duplicated literal path checks. Rejected because they repeat retired
  labels in tracked source and split one policy across three milestones.
- Remove all uses of the word `agent`. Rejected because that would erase
  intentional product terminology and change documentation semantics.
