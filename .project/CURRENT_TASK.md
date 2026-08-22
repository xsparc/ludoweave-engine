# Current task

- **Task:** M98 - local-header timestamp consistency preflight
- **Status:** Implementation, exact supported-runtime suites, unchanged local
  quality/graphics/distribution/release gates, and corrected findings-first
  review pass. Final precommit audit and hosted qualification remain; no hosted
  pass is claimed yet.
- **Base:** Exact verified M97 closeout squash
  `9f4a3b915df40fe86a0fc5c759763186899ea1fe`, tree
  `678b6ff58513952a23041e6594fc621e71e9537b`.
- **Branch:** `release/m98-local-timestamp-consistency`.

## Approved scope

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

## Current evidence

- Local branch base, local `main`, and `origin/main` are exact M97 closeout with
  symmetric difference `0 0`; the worktree was clean and no PR was open before
  M98 edits.
- PKWARE APPNOTE 6.3.10 defines matching two-byte DOS time and two-byte DOS date
  fields in local and central member records. Python documents public central
  `ZipInfo.date_time` and public local `ZipInfo.header_offset`.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 each retained both central tuples
  `(2026, 8, 23, 4, 6, 8)` and read both payloads after only the second local
  time's low byte changed from `c4` to `e4`.
- The formatted, Ruff-clean, strict-Pyright-clean 28-assertion M98 contract has
  deliberate red evidence on exact CPython 3.14.5: 18 inherited/behavior/
  producer/protected-surface controls passed and ten policy/helper/order/docs
  assertions failed against unchanged M97.
- All 28 M98 assertions pass on exact CPython 3.12.13, 3.13.13, and 3.14.5;
  each complete suite passes 2,833 tests with 16 established skips.
- Repository-wide static, architecture, docs, metadata, real-wgpu, profile,
  Clockwork Arena, Agent World Builder, repeat-build, isolated-wheel,
  deterministic staging, and complete release gates pass after review
  correction.

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

- Finish the final precommit scope/history/integrity audit, commit with DCO,
  publish a ready PR, and qualify the exact head through the
  unchanged quota-conscious three-allocation CI, then audit and squash-merge.
- Record integration through the bounded documentation-only path, close out
  without allocating a workflow, delete verified scratch targets and every
  branch except `main`, and only then select M99.
