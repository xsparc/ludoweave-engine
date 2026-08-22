# Current task

- **Task:** M98 - local-header timestamp consistency preflight
- **Status:** Feature PR #246 is exact-head hosted-validated and
  squash-integrated. Corrected integration-record PR #247 is exact-head
  hosted-validated and squash-integrated. The three-file no-workflow closeout
  record passes its local metadata, whitespace, and precommit remote/history/
  integrity gates; commit and publication remain. No product or policy change
  remains.
- **Base:** Verified M98 integration-record squash
  `0225660c0b24ca4a5831adf96b20b0cb922d2754`, tree
  `1ab4b10f8665fb7edb376d8bd45315735d980ec2`.
- **Branch:** `release/m98-closeout`.

## Integrated scope

- After M97 extraction-version consistency, private release smoke reads exactly
  four bytes at each public `ZipInfo.header_offset + 10`.
- Those local MS-DOS time/date bytes must equal the representation reconstructed
  from public central `ZipInfo.date_time`.
- Mismatch raises stable content-silent `sample bundle local header timestamps
  are inconsistent` before decoded-name policy, metadata, exact inventory,
  staging, or member reads.
- Every established policy through M97, empty-archive inventory behavior,
  owned-resource cleanup, and caller snapshot position remain intact.
- RFC-0081 and aligned public, security, architecture, release, roadmap,
  maintainer, test, and factual project records define the boundary.
- Workflow, runner allocations, actions, permissions, credentials,
  dependency/lock/version, sample producer, runtime package/API, release
  authority, tag, release, and publication remain unchanged.

## Hosted feature evidence

- Ready PR #246 exact DCO head
  `403c050224262563f5a7e77d17d7cbfa62732420`, tree
  `65e83878ffb50e5c654ba3b4e7e53fb60458b9dd`, passed run `32593756442`
  in exactly three Linux-first allocations.
- Linux job `97081449858` passed in 7m27s, macOS job `97082337246` in
  2m01s, and Windows job `97082337331` in 3m58s.
- Linux CPython 3.12 passed 2,848 tests. Linux 3.13/3.14 and macOS/Windows
  3.14 each passed 2,848 with one established capability skip.
- Every OS passed ten real-wgpu tests, graphics profiling, Clockwork Arena,
  and Agent World Builder. Linux also passed formatting, Ruff, strict Pyright,
  strict docs, base profiling, installed-wheel smoke, ten-artifact staging,
  and complete release smoke.
- Two hosted builds reproduced a 277,044-byte pure wheel at
  `02fe38271e0f0b450f4fe6a63d0fd759ac3bdb04b662d0283ab7d5cf81dad6d3`
  and a 1,431,495-byte source archive at
  `4ea71905c2a49a6de6898209f75e83f0560ee25d192cb98ce18b3c6813ce28cb`.
- Two separated readiness audits retained exact head/tree/base, one DCO
  commit, 16 paths, three successful checks from one exact-head run,
  `MERGEABLE/CLEAN`, and zero comments, reviews, review comments, or review
  threads.
- Guarded squash `f89fdbb733925344b8d362b60db035d7df575687` has the exact
  qualified tree, sole M97 closeout parent, standalone DCO trailer, and a valid
  GitHub signature verified at `2026-08-22T19:40:48Z`. The feature branch is
  deleted remotely and locally.

## Hosted integration-record evidence

- Corrected ready PR #247 exact DCO head
  `ab7378aae45e620afeedf737f16b3c65af8a0ef8`, tree
  `1ab4b10f8665fb7edb376d8bd45315735d980ec2`, passed exact-head run
  `32595002867` in one 44-second Linux allocation; the desktop matrix
  placeholder skipped without allocating a runner.
- Strict docs built in 2.01 seconds; all 1,304 hosted architecture assertions,
  reproducible distribution, isolated-wheel smoke, deterministic ten-artifact
  staging, and complete release smoke passed.
- Hosted repeat builds reproduced a 277,034-byte pure wheel at
  `eca01f9e9ed31a6d625583348e902adb55b6110f48a67cd82042c8313c415378`
  and a 1,432,942-byte source archive at
  `194fe3349cfc19b8aa5c576f5999631dc5754bbe9ebd2e2baee6710d80bf9f35`.
- Two separated readiness audits retained exact head/tree/base, one DCO
  commit, five paths, one exact-head successful run, and `MERGEABLE/CLEAN`.
  The one corrected review thread remained resolved and outdated with zero
  unresolved threads or issue comments.
- Guarded squash `0225660c0b24ca4a5831adf96b20b0cb922d2754` has the exact
  qualified tree, sole M98 feature-squash parent, standalone DCO trailer, and a
  valid GitHub signature verified at `2026-08-22T19:54:43Z`. The integration
  branch is deleted remotely and locally.

## Explicit non-scope

- No timestamp semantics validator, timezone or UTC conversion, wall-clock
  comparison, calendar validation, reproducibility rule, canonical timestamp,
  extended-timestamp or NTFS-extra interpretation, or sub-second recovery.
- No CRC/size or field-wide local/central comparison.
- No complete local-record or payload bound, next-header bound, gap, adjacency,
  contiguity, physical-overlap rule, or inter-member layout validator.
- No archive repair, general archive sandbox, public release observation,
  workflow change, runtime feature, dependency, native/WASM work, tag, release,
  or publication.

## Remaining acceptance work

- Commit, publish, audit, and squash-integrate exactly the three validated
  factual closeout records without allocating a workflow.
- Delete verified M98 generated targets and all branches except `main`, verify
  the final feature/integration/closeout sole-parent chain, then select M99.
