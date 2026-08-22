# Current task

- **Task:** M99 - local-header CRC-32 consistency preflight
- **Status:** The bounded four-byte implementation, aligned documentation,
  exact supported-runtime suites, complete local gates, and findings-first
  review pass after a corrected first checkpoint. Review-inclusive packaging
  and release smoke, final source separator, and precommit remote/history/
  integrity audit plus final documentation separator pass. DCO commit,
  publication, and hosted gates remain; no hosted M99 pass is claimed yet.
- **Base:** Exact verified M98 closeout squash
  `6d4529efb0476f3e3e45f78204d2b0aa192da018`, tree
  `7e3ffae0423fd2b4da1725db48864b9c04f8ad35`.
- **Branch:** `release/m99-local-crc-consistency`.

## Approved scope

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

## Current evidence

- Closed M98 main, local and remote branch state, and merge base are exact at
  `6d4529efb0476f3e3e45f78204d2b0aa192da018` with divergence `0 0`.
  Only `main` exists locally/remotely; no PR, release, tag, or unexpected
  workflow remains. Its feature/integration/closeout squash chain retains exact
  sole parents, reviewed trees, DCO trailers, and valid GitHub signatures.
- M98 closeout PR #248 used exact DCO head
  `7e06f6897a5c58431b278a9ed7f9a1ac6e1b1960`, tree
  `7e3ffae0423fd2b4da1725db48864b9c04f8ad35`, allocated no workflow, passed
  two separated readiness audits without feedback, and squash-merged at
  `2026-08-22T19:59:48Z`. All 22 verified M98 scratch targets are absent and
  the five metadata-hygiene assertions pass.
- PKWARE APPNOTE 6.3.10 defines the corresponding four-byte local and central
  CRC-32 fields. Python documents public central `ZipInfo.CRC` and public local
  `ZipInfo.header_offset`; CPython reads validate against the central value.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 each retained central CRCs
  `[3724039362, 2868864084]` and read both payloads after only the second local
  CRC changed from `2868864084` to `2868864085`.
- The 29-assertion M99 contract is format/Ruff clean and strict Pyright reports
  zero findings. Against unchanged M98 on exact CPython 3.14.5, 19 inherited,
  runtime, producer, and protected-surface assertions passed; ten stable-error,
  helper, cleanup, ordering, and documentation assertions failed as intended.
- After one mechanical format/navigation/literal-wording correction, all 57
  combined M98-M99 assertions and strict docs pass. All 29 focused assertions
  pass on exact CPython 3.12.13, 3.13.13, and 3.14.5; each complete suite
  passes 2,862 tests with 16 established skips.
- The unchanged lock/graphics environment, all repository-wide static,
  architecture, docs, metadata, whitespace, real-wgpu, profile, vertical-slice,
  repeat-build, isolated-wheel, staging, and complete release gates pass. A
  findings-first diff/package/security review remains.
- Findings-first review found no remaining actionable defect across the exact
  15-path scope, one-field order/error/cleanup boundary, public-field use,
  documentation, package contents, protected surfaces, or credential/identity
  scans.
- Review-inclusive repeat builds reproduce the pure wheel and source archive;
  isolated-wheel smoke, ten-artifact staging, and complete release smoke pass.

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

- DCO-commit, publish, exact-head qualify, audit, and squash-integrate.
- Audit, DCO-commit, publish, exact-head qualify through the unchanged
  quota-conscious workflow, squash-integrate, record, close, and clean M99.
