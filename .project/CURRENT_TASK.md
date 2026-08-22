# Current task

- **Task:** M97 - local-header extraction-version consistency preflight
- **Status:** Feature PR #243 and integration-record PR #244 are verified and
  squash-integrated. The closeout-only record passes local proof and audit;
  commit and publication are ready. No product or policy work remains.
- **Base:** Verified M97 integration-record squash
  `e64264e2084b718b4f85338831ed806b088eb322`, tree
  `881cf2cde38c5e833b2898b9fc652f0f116c08a7`.
- **Branch:** `release/m97-closeout`.

## Integrated scope

- After M96 local-extra consistency, private release smoke reads exactly two
  bytes at each public `ZipInfo.header_offset + 4`.
- Those local bytes must equal public central
  `bytes((info.extract_version, info.reserved))`.
- Mismatch raises stable content-silent `sample bundle local header extraction
  versions are inconsistent` before decoded-name policy, metadata, exact
  inventory, staging, or member reads.
- Every established policy through M96, empty-archive inventory behavior,
  owned-resource cleanup, and caller snapshot position remain intact.
- RFC-0080 and aligned public, security, architecture, release, roadmap,
  maintainer, test, and factual project records define the boundary.
- Workflow, runner allocations, actions, permissions, credentials,
  dependency/lock/version, sample producer, runtime package/API, release
  authority, tag, release, and publication remain unchanged.

## Hosted evidence

- Ready PR #243 exact DCO head
  `aa37212f4ec50c040fa39bfc98457133ab2744dd`, tree
  `8abe71ab97716a767517d211106281f25d20bb25`, passed run
  `32590870976` in exactly three Linux-first allocations.
- Linux job `97074392026` passed in 7m26s, macOS job `97075313835` in
  2m35s, and Windows job `97075313836` in 3m20s.
- Linux CPython 3.12 passed 2,820 tests. Linux 3.13/3.14 and macOS/Windows
  3.14 each passed 2,820 with one established capability skip.
- Every OS passed ten real-wgpu tests, graphics profiling, Clockwork Arena,
  and Agent World Builder. Linux also passed formatting, Ruff, strict Pyright,
  strict docs, base profiling, installed-wheel smoke, ten-artifact staging,
  and complete release smoke.
- Two hosted builds reproduced a 276,933-byte pure wheel at
  `39a2c02643778e823e119072a8c718cebb32f3bb3c7cc58a90981074b75e0326`
  and a 1,423,352-byte source archive at
  `e8a3ab4cb2c03b3ebb22ea284c50ca63d31e6ffe1e57fdeba96324c163d72090`.
- Two separated readiness audits retained exact head/tree/base, one DCO
  commit, 16 paths, three successful checks from one exact-head run,
  `MERGEABLE/CLEAN`, and zero comments, reviews, review comments, or review
  threads.
- Guarded squash `0f519c72c12d21e0a0001c21868bd0748c7d7b8c` has the exact
  qualified tree, sole M96 closeout parent, standalone DCO trailer, and a valid
  GitHub signature verified at `2026-08-22T18:41:22Z`. The feature branch is
  deleted remotely and locally.
- Ready integration-record PR #244 exact DCO head
  `cd590e88befe44d4dbcfcdf8a700b4e4c0efd90b`, tree
  `881cf2cde38c5e833b2898b9fc652f0f116c08a7`, passed run `32591861207`
  in one 45-second Linux job `97076836696`; desktop umbrella job
  `97076933484` skipped with zero steps. Hosted formatting, Ruff, strict docs,
  all 1,276 documentation-architecture assertions, reproducible builds,
  installed-wheel smoke, ten-artifact staging, and complete release smoke
  passed.
- Hosted record builds reproduced a 276,921-byte wheel at
  `cd857473dbe32729fe26ca30d6eb4f7ceac3431f927fe389c129af82e3d573d2`
  and a 1,424,470-byte source archive at
  `26d5de3ad8ddec68096e146c93db9f9c315af5f9b05efb2cf86592b2be755309`.
- Guarded integration-record squash
  `e64264e2084b718b4f85338831ed806b088eb322` has the exact reviewed tree,
  sole feature-squash parent, standalone DCO trailer, and a valid GitHub
  signature verified at `2026-08-22T18:51:16Z`. The record branch is deleted
  remotely and locally.

## Explicit non-scope

- No supported-version allowlist, minimum extractor-capability rule,
  reserved-byte policy, or semantic interpretation of the two bytes.
- No time/CRC/size or field-wide local/central comparison.
- No complete local-record or payload bound, next-header bound, gap, adjacency,
  contiguity, physical overlap rule, or inter-member layout validator.
- No archive repair, general archive sandbox, public release observation,
  workflow change, runtime feature, dependency, native/WASM work, tag, release,
  or publication.

## Remaining acceptance work

- Validate, commit, publish, audit, and squash-integrate exactly the three
  project closeout records without runner allocation.
- Delete verified M97 generated targets and all branches except `main`, verify
  the final feature/integration/closeout sole-parent chain, then select M98.
