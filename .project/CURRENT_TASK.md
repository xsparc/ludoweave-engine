# Current task

- **Task:** M101 - local-header uncompressed-size consistency preflight
- **Status:** The M100 feature is fully locally validated in one standalone DCO
  commit and remains unpushed because of the external reviewer-identity hold.
  M101 primary-source direction, deterministic supported-runtime probe, and
  corrected deliberate red contract, runtime classifier, RFC-0084, aligned
  documentation, and corrected implementation checkpoint are complete on a
  local stacked branch. Supported-Python, complete local/static/architecture,
  real-wgpu, deterministic examples/profiles, initial reproducible release, and
  findings-first review, record-inclusive artifact, final source, stacked
  remote-history/scope/integrity, and post-audit gates pass. The fully validated
  M101 tree is contained in one standalone local DCO commit stacked directly on
  M100. Both milestones remain unpushed.
- **Base:** Fully locally validated M100 DCO commit
  `103f84bf57f0b4ae0ca07548b453c199eec88f49`, tree
  `ff3a7105aa7fef413d7cea40a126758cbc42882b`, with sole parent exact M99
  closeout.
- **Branch:** `release/m101-local-uncompressed-size-consistency`.

## Approved scope

- After M100 compressed-size consistency, private release smoke reads exactly
  four bytes at each public `ZipInfo.header_offset + 22`.
- Those local bytes must equal public central `ZipInfo.file_size` encoded as an
  unsigned four-byte little-endian value.
- Mismatch raises stable content-silent `sample bundle local header
  uncompressed sizes are inconsistent` before decoded-name policy, metadata,
  exact inventory, staging, or member reads.
- Every established policy through M100, empty-archive inventory behavior,
  owned-resource cleanup, and caller snapshot position remain intact.
- RFC-0084 and aligned public, security, architecture, release, roadmap,
  maintainer, test, and factual project records define the boundary.
- Workflow, runner allocations, actions, permissions, credentials,
  dependency/lock/version, sample producer, runtime package/API, release
  authority, tag, release, and publication remain unchanged.

## Current evidence

- M100 commit `103f84bf57f0b4ae0ca07548b453c199eec88f49` is one commit
  ahead of exact `origin/main`, has sole M99 closeout parent, the validated
  15-path tree, exact author/committer identity, and standalone DCO trailer.
  Its worktree was clean before M101 branch creation; it is not pushed and no
  hosted qualification is claimed.
- All 26 generated M100 scratch targets were verified under the exact workspace
  `.tmp` root and removed. The first sandboxed cleanup removed nine and hit
  access denial on 17 pytest directories; the approved exact-root retry removed
  those 17. No tracked or recoverable file was removed, and no M100 scratch
  target remains.
- PKWARE APPNOTE 6.3.10 defines the adjacent four-byte local and central
  uncompressed-size fields. Python documents public `ZipInfo.file_size` and
  `ZipInfo.header_offset`; descriptor and ZIP64 exceptions remain outside the
  already constrained fixed profile.
- The first deterministic probe run reproduced the behavior gap on exact
  CPython 3.12.13 while Ruff lint passed, but format check requested one
  mechanical reflow. After correction, exact 3.12.13, 3.13.13, and 3.14.5 all
  retained local/central sizes `[9, 9]`, changed only the second local size to
  `10`, and read both payloads; the probe is format/Ruff clean.
- Initial M101 contract static checks passed Ruff and strict Pyright, while
  format check requested one reflow. The red run also found one contract bug:
  XOR mutation changed `9` to `8` while the expected observation was `10`.
  After using deterministic increment and formatting, the 15-assertion contract
  is format/Ruff clean, strict Pyright reports zero findings, exact CPython
  3.14.5 passes five supported-runtime, M100-precedence, empty-archive,
  producer, and protected-surface controls, and ten intended policy/helper/
  cleanup/ordering/documentation assertions fail in 0.74 seconds against
  unchanged M100. No complete pass is claimed.
- The first implementation checkpoint passed Ruff, strict Pyright, all 45
  combined M100-M101 assertions in 0.83 seconds, strict docs in 1.64 seconds,
  and whitespace, but format check requested one mechanical runtime reflow.
  After correction, both affected Python files are format/Ruff clean, strict
  Pyright has zero findings, all 45 assertions pass in 0.42 seconds, strict docs
  build in 1.59 seconds with only the known upstream Material notice, and
  whitespace is clean.
- All 15 M101 assertions pass on exact CPython 3.12.13, 3.13.13, and 3.14.5 in
  0.26, 0.74, and 0.61 seconds. Complete suites on those runtimes each pass
  2,907 tests with 16 established skips in 109.53, 100.69, and 108.07 seconds.
- The unchanged 46-package lock and exact CPython 3.12.13 45-package graphics
  environment pass. All 344 Python files are format clean; Ruff and strict
  Pyright pass; architecture passes 1,377 assertions with one established
  Windows capability skip in 9.10 seconds; strict docs build in 1.49 seconds;
  all 20 metadata/M101 assertions pass; and whitespace is clean.
- All ten real-wgpu tests pass in 6.83 seconds. One-repeat base and graphics
  profiles validate; Clockwork Arena and Agent World Builder reproduce their
  established state, capture, and replay identities.
- Two fresh builds reproduce a 275,992-byte pure wheel at
  `6a218c01241cb53133c6cee75c84da577ad848c544195897e810733772498c3e`
  and a 1,453,740-byte source archive at
  `b054c4e6db0806c3d2a88b0e03706b61d22c706a43bb8e52cb3f5a2732a6303c`;
  isolated-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass. Recording this evidence changes the source archive.
- Findings-first review found no actionable issue across the 15 intended paths.
  The runtime diff is two constants, one ordered call, and one position-
  restoring helper using public ZIP metadata; stable error, M100 precedence,
  empty behavior, and cleanup are covered. Protected workflows, stager,
  metadata, lock, runtime package/API, dependencies, version, and release
  authority are unchanged. Credential and explicit service-identity scans are
  empty; no retired control path is tracked. The 94-entry pure wheel and 568-
  entry source archive contain no native, WASM, bytecode, or retired control-
  metadata entry.
- Review-inclusive repeat builds reproduce the same 275,992-byte wheel at
  `6a218c01241cb53133c6cee75c84da577ad848c544195897e810733772498c3e`
  and a 1,454,710-byte source archive at
  `a9b014dcc5fb21d0e4880b2b9f1ef182a5c9ef26ee0ced9b556072cdb58a1509`;
  isolated-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass. Hosted exact-head artifacts would remain authoritative
  after final factual record changes.
- Final source separator: the unchanged 46-package lock resolves in 0.82
  milliseconds; all 344 Python files remain format clean; Ruff and strict
  Pyright pass; all 1,377 architecture assertions pass with one established
  Windows capability skip in 8.49 seconds; strict docs build in 1.44 seconds;
  all 20 metadata/M101 assertions pass in 0.42 seconds; and whitespace is
  clean.
- Precommit audit: after fetch/prune, `HEAD`, the M100 branch, and M100 expected
  base are exact; local `main` and `origin/main` remain exact M99 closeout;
  merge base is M100 and divergence from `origin/main` is the expected `1 0`
  before the M101 commit. Exactly 15 intended paths change. Only `main` and the
  required M100/M101 stacked branches exist locally, and only `origin/main`
  exists remotely. Open PR, M101 run, release, and tag queries are empty.
  Protected surfaces have no M101 diff; Git has zero critical integrity
  findings; whitespace is clean; and exact DCO identity is configured.
- Final post-audit separator: strict docs build in 1.48 seconds; all 20
  metadata/M101 assertions pass in 0.43 seconds; credential, explicit service-
  identity, and retired-control scans remain at zero; and whitespace is clean.

## Explicit non-scope

- No decompression or recompression and no payload-content read during
  preflight.
- No compression-ratio or archive-bomb policy and no payload-integrity
  certification.
- No field-wide local/central comparison, complete local-record bound, payload
  or next-header bound, gap, adjacency, contiguity, physical non-overlap rule,
  or inter-member layout validator.
- No raw central-directory parser, archive repair, general archive sandbox,
  public release observation, workflow change, runtime feature, dependency,
  native/WASM work, tag, release, or publication.

## Remaining acceptance work

- Publish and exact-head hosted-qualify M100/M101 ready PRs only after the
  automated-review identity exposure
  is resolved or the maintainer explicitly accepts that disclosure risk.
