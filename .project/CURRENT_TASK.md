# Current task

- **Task:** M99 - local-header CRC-32 consistency preflight
- **Status:** Feature PR #249 is exact-head hosted-validated and
  squash-integrated. The five-file factual integration record passes its
  corrected complete local source, documentation, architecture, distribution,
  and release proof plus final source separation and the precommit audit.
  The final documentation separator passes. Publication and hosted
  qualification remain; no runtime or policy change remains.
- **Base:** Verified M99 feature squash
  `909b7568fe98da9a77d226df57eb17a7571a68e5`, tree
  `77c40e7a27f70bc89e273225a8bb81966fc8dfa0`.
- **Branch:** `release/m99-integration-record`.

## Integrated scope

- After M98 timestamp consistency, private release smoke reads exactly four
  bytes at each public `ZipInfo.header_offset + 14`.
- Those local bytes must equal public central `ZipInfo.CRC` encoded as an
  unsigned four-byte little-endian value.
- Mismatch raises stable content-silent `sample bundle local header CRC-32
  values are inconsistent` before decoded-name policy, metadata, exact
  inventory, staging, or member reads.
- Every established policy through M98, empty-archive inventory behavior,
  owned-resource cleanup, and caller snapshot position remain intact.
- RFC-0082 and aligned public, security, architecture, release, roadmap,
  maintainer, test, and factual project records define the boundary.
- Workflow, runner allocations, actions, permissions, credentials,
  dependency/lock/version, sample producer, runtime package/API, release
  authority, tag, release, and publication remain unchanged.

## Hosted feature evidence

- Ready PR #249 exact DCO head
  `b3e1bc994e57fac2277e86b552d760f9ae9c90a1`, tree
  `77c40e7a27f70bc89e273225a8bb81966fc8dfa0`, passed run `32596930304`
  in exactly three Linux-first allocations.
- Linux job `97089296631` passed in 7m20s, macOS job `97090165770` in
  2m00s, and Windows job `97090165820` in 4m10s.
- Linux CPython 3.12 passed 2,877 tests. Linux 3.13/3.14 and macOS/Windows
  3.14 each passed 2,877 with one established capability skip.
- Every OS passed ten real-wgpu tests, graphics profiling, Clockwork Arena,
  and Agent World Builder. Linux also passed formatting, Ruff, strict Pyright,
  strict docs, base profiling, installed-wheel smoke, ten-artifact staging,
  and complete release smoke.
- Two hosted builds reproduced a 277,158-byte pure wheel at
  `232eaa8b23bbe6c5e0cf0fa5510521dadb175fae17baf893ff208695c061b76e`
  and a 1,439,905-byte source archive at
  `abaa619ce80968b3f49b3f0b25de6b9c075baf3d6de142e663e56f59c09701ae`.
- Two separated readiness audits around 34 passing local assertions retained
  exact head/tree/base, one DCO commit, 15 paths, three successful checks from
  one exact-head run, `MERGEABLE/CLEAN`, and zero comments, reviews, or review
  comments.
- Guarded squash `909b7568fe98da9a77d226df57eb17a7571a68e5` has the exact
  qualified tree, sole M98 closeout parent, standalone DCO trailer, and a valid
  GitHub signature verified at `2026-08-22T20:44:55Z`. The feature branch is
  deleted remotely; its verified local squash-era ref is pending deletion.

## Explicit non-scope

- No CRC recomputation, payload read, payload-integrity certification,
  polynomial selection, CRC repair, or alternate checksum.
- No compressed/uncompressed size comparison or constraint.
- No field-wide local/central comparison, complete local-record bound, payload
  or next-header bound, gap, adjacency, contiguity, physical non-overlap rule,
  or inter-member layout validator.
- No raw central-directory parser, archive repair, general archive sandbox,
  public release observation, workflow change, runtime feature, dependency,
  native/WASM work, tag, release, or publication.

## Remaining acceptance work

- Qualify and squash-integrate this five-file factual record through the
  bounded documentation path.
- Create and integrate the no-workflow closeout record, delete verified M99
  scratch targets and every branch except `main`, and only then select M100.
