# Current task

- **Task:** M100 - local-header compressed-size consistency preflight
- **Status:** The primary-source direction, deterministic supported-runtime
  probe, deliberate red contract, runtime classifier, RFC-0083, aligned public
  documentation, supported-Python suites, complete local/static/architecture
  gate, real-wgpu and deterministic vertical slices, and initial reproducible
  distribution/release gate, and findings-first review pass. Record-inclusive
  artifacts, final source separator, and remote history/scope/integrity audit
  pass. The final post-audit separator passes, and the fully validated tree is
  contained in one standalone local DCO commit. Public push and ready-PR
  publication are held
  because an externally configured automated reviewer exposed its service
  identity on the completed M99 closeout PR.
- **Base:** Exact verified M99 closeout squash
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, tree
  `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`.
- **Branch:** `release/m100-local-compressed-size-consistency`.

## Approved scope

- After M99 CRC-32 consistency, private release smoke reads exactly four bytes
  at each public `ZipInfo.header_offset + 18`.
- Those local bytes must equal public central `ZipInfo.compress_size` encoded
  as an unsigned four-byte little-endian value.
- Mismatch raises stable content-silent `sample bundle local header compressed
  sizes are inconsistent` before decoded-name policy, metadata, exact
  inventory, staging, or member reads.
- Every established policy through M99, empty-archive inventory behavior,
  owned-resource cleanup, and caller snapshot position remain intact.
- RFC-0083 and aligned public, security, architecture, release, roadmap,
  maintainer, test, and factual project records define the boundary.
- Workflow, runner allocations, actions, permissions, credentials,
  dependency/lock/version, sample producer, runtime package/API, release
  authority, tag, release, and publication remain unchanged.

## Current evidence

- M99 closeout PR #251 merged as verified squash
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, with sole M99 integration
  parent, reviewed tree, standalone DCO trailer, and valid GitHub signature.
  Final history, branch, metadata, whitespace, and cleanup audits passed; only
  `main` remained locally and remotely before the M100 branch was created.
- PKWARE APPNOTE 6.3.10 defines the duplicated four-byte little-endian
  compressed-size fields. Python documents public `ZipInfo.compress_size` and
  `ZipInfo.header_offset`; CPython's writer uses the same central size while
  handling established descriptor and ZIP64 exceptions outside this profile.
- A deterministic two-member probe on exact CPython 3.12.13, 3.13.13, and
  3.14.5 retained central/local sizes `[11, 11]`, changed only the second local
  size to `12`, and still read both payloads.
- The format/Ruff-clean, strict-Pyright-clean M100 red contract collected 30
  assertions on exact CPython 3.14.5: 20 established behavior, precedence,
  producer, empty-archive, and protected-surface controls passed; ten intended
  policy/helper/ordering/documentation assertions failed against unchanged
  M99. No complete pass was claimed.
- The first implementation checkpoint passed Ruff, strict Pyright, all 59
  combined M99-M100 assertions, strict docs, and whitespace, but format check
  requested one mechanical reflow in `scripts/smoke_release.py`. After that
  reflow, both affected Python files are format/Ruff clean, strict Pyright has
  zero findings, all 59 assertions pass in 0.43 seconds, strict docs build in
  1.44 seconds with only the known upstream Material notice, and whitespace is
  clean.
- An attempted parallel supported-runtime gate first encountered sandboxed uv
  cache denial, then raced three exact-Python invocations against the shared
  `.venv`; only 3.14 completed while 3.12/3.13 failed during environment
  replacement. Sequential correction passes all 30 M100 assertions on exact
  CPython 3.12.13, 3.13.13, and 3.14.5.
- The initial CPython 3.12.13 full suite found six README regressions caused by
  compacting the historical status paragraph: exact M28-M34 no-evidence
  phrases were lost or split. Restoring them as readable bullets made the six
  assertions pass, then complete suites passed 2,892 tests with 16 established
  skips on 3.12.13, 3.13.13, and 3.14.5 in 109.88, 102.30, and 109.01 seconds.
- The unchanged 46-package lock and exact CPython 3.12.13 45-package graphics
  environment pass. All 343 Python files are format clean; Ruff and strict
  Pyright pass; architecture passes 1,362 assertions with one established
  Windows capability skip in 9.90 seconds; strict docs build in 1.55 seconds;
  all 35 metadata/M100 assertions pass; and whitespace is clean.
- All ten real-wgpu tests pass in 7.49 seconds. One-repeat base and graphics
  profiles validate; Clockwork Arena and Agent World Builder reproduce their
  established state, capture, and replay identities.
- Two fresh builds reproduce a 275,920-byte pure wheel at
  `eccad7badcf0c629d04f23531a0402c24f718b442153907d678a898662452ccb`
  and a 1,448,116-byte source archive at
  `f24551359391ddd62b1f3a4a0692bff7c70a4681d5363d0eedf1e350f88bc78b`;
  isolated-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass. Recording this evidence changes the source archive.
- Findings-first review found no actionable issue across the 15 intended paths.
  The runtime diff is exactly two constants, one ordered call, and one position-
  restoring helper using public ZIP metadata; stable error, M99 precedence,
  empty behavior, and owned cleanup are covered. Protected workflows, stager,
  project metadata, lock, runtime package/API, dependency/version, and release
  authority are unchanged. Credential and explicit service-identity scans are
  empty; no retired control path is tracked. The 94-entry pure wheel and 566-
  entry source archive contain no native, WASM, bytecode, or retired control-
  metadata entry.
- Review-inclusive repeat builds reproduce the same 275,920-byte wheel at
  `eccad7badcf0c629d04f23531a0402c24f718b442153907d678a898662452ccb`
  and a 1,450,072-byte source archive at
  `bccf6d8f119d8f633a39a64094badf3ad8a6c1dfb40ffe4eca1396465619211a`;
  isolated-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass. Hosted exact-head artifacts would remain authoritative
  after factual record updates change the source archive.
- Final source separator: the unchanged 46-package lock resolves in 0.78
  milliseconds; all 343 Python files remain format clean; Ruff and strict
  Pyright pass; all 1,362 architecture assertions pass with one established
  Windows capability skip in 10.28 seconds; strict docs build in 1.61 seconds;
  all 35 metadata/M100 assertions pass in 0.50 seconds; and whitespace is
  clean.
- Precommit audit: after fetch/prune, branch base, local `main`, `origin/main`,
  and merge base remain exact M99 closeout with divergence `0 0`. Exactly 15
  intended paths change; only `main` and the neutral M100 branch exist locally,
  and only `origin/main` exists remotely. Open PR, M100 run, release, and tag
  queries are empty. Protected workflow, metadata, lock, runtime package, and
  sample producer surfaces have no diff; Git has zero critical integrity
  findings; whitespace is clean; and exact DCO identity is configured.
- Final post-audit separator: strict docs build in 1.47 seconds; all 35
  metadata/M100 assertions pass in 0.47 seconds; credential, explicit service-
  identity, and retired-control scans remain at zero; and whitespace is clean.

## Explicit non-scope

- No decompression or recompression and no uncompressed-size comparison.
- No compression-ratio or archive-bomb policy and no payload-integrity
  certification.
- No field-wide local/central comparison, complete local-record bound, payload
  or next-header bound, gap, adjacency, contiguity, physical non-overlap rule,
  or inter-member layout validator.
- No raw central-directory parser, archive repair, general archive sandbox,
  public release observation, workflow change, runtime feature, dependency,
  native/WASM work, tag, release, or publication.

## Remaining acceptance work

- Publish and exact-head hosted-qualify the ready PR only after the automated-
  review identity exposure is
  resolved or the maintainer explicitly accepts that external disclosure risk.
