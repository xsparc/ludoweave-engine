# Current task

- **Task:** M99 - local-header CRC-32 consistency preflight
- **Status:** Feature PR #249 is exact-head hosted-validated and
  squash-integrated. Integration-record PR #250 is exact-head hosted-validated
  and squash-integrated. The three-file no-workflow closeout record passes its
  local metadata, whitespace, and precommit history/scope/integrity gates;
  the final separator also passes. Commit and publication remain. No runtime
  or policy change remains.
- **Base:** Verified M99 integration-record squash
  `d658bd7df926775ea77b36b34dec377a14a76bb6`, tree
  `a602729574488b940a541e64cad805cc3b96ffa6`.
- **Branch:** `release/m99-closeout`.

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
  deleted remotely and locally.

## Hosted integration-record evidence

- Ready PR #250 exact DCO head
  `0cdfa5285db965f9238b6fe878912f20c7f0f4d8`, tree
  `a602729574488b940a541e64cad805cc3b96ffa6`, passed exact-head run
  `32597990726` in one 52-second Linux allocation; the desktop matrix
  placeholder skipped without allocating a runner.
- Strict docs built in 2.20 seconds; all 1,333 hosted architecture assertions,
  reproducible distribution, isolated-wheel smoke, deterministic ten-artifact
  staging, and complete release smoke passed.
- Hosted repeat builds reproduced a 277,176-byte pure wheel at
  `156b2f5fd64c6ec7ad99d4706279b79bdc7978da51eaf4c8ff08ade8f7e4fee2`
  and a 1,441,004-byte source archive at
  `43390607d097dbd6afbf3c203f949c3b7b579b715eb61811cfe6db2649ecf8a7`.
- Two separated readiness audits around 34 passing local assertions retained
  exact head/tree/base, one DCO commit, five paths, one exact-head successful
  run, `MERGEABLE/CLEAN`, and zero comments, reviews, or review comments.
- Guarded squash `d658bd7df926775ea77b36b34dec377a14a76bb6` has the exact
  qualified tree, sole M99 feature-squash parent, standalone DCO trailer, and a
  valid GitHub signature verified at `2026-08-24T13:01:51Z`. The integration
  branch is deleted remotely and locally.

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

- Validate, commit, publish, audit, and squash-integrate exactly the three
  factual closeout records without allocating a workflow.
- Delete verified M99 scratch targets and every branch except `main`, verify
  the final feature/integration/closeout sole-parent chain, then select M100.
