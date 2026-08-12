# Current Task

- **Task:** M76 - enhanced-deflate sample-member preflight
- **Status:** Feature candidate is fully locally qualified and reviewed;
  exact-head hosted publication remains in progress.
- **Base:** Exact synchronized M75 closeout
  `ddf262dff7a8c93defad5a205adbaec460563439`, tree
  `c124cb2573a4329c8032d1d4eeb416e2e1556d24`.
- **Branch:** `release/m76-enhanced-deflate-preflight`

## Acceptance boundary

- Reject exactly central-directory ZIP general-purpose bit 4 on compression
  method 8 members during the existing all-member preflight.
- Emit the stable content-silent policy error
  `sample bundle uses enhanced deflating` before member metadata, inventory
  validation, staging, or member reads.
- Preserve M69 encryption and M75 compressed-patch error precedence.
- Keep bit 4 on stored members and all unexamined flag/method combinations
  outside this exact decision; local-header inconsistencies also remain out of
  scope. Do not create a broad flag allowlist or raw header parser.
- Prove owned source, snapshot, and archive cleanup and unchanged producer
  compatibility.
- Add RFC-0059 and align public security, architecture, release, changelog,
  maintainer, and project-state records.
- Change no workflow, runner allocation, dependency, version, sample producer,
  runtime package/API, release authority, tag, release, or publication surface.

## Evidence so far

- PKWARE APPNOTE 6.3.9 reserves general-purpose bit 4 for enhanced deflating
  with compression method 8.
- Exact installed CPython 3.12.13 source checks compressed-patch bit 5 and
  strong-encryption bit 6 at member open but does not inspect bit 4. The M76
  fixture proves normal deflate bytes carrying bit 4 remain readable.
- The first pytest launch used a missing basetemp parent and produced six setup
  errors; it is invalid environment evidence, not a product baseline.
- Against unchanged M75, the corrected regression was format/Ruff clean and
  strict Pyright clean; 7 M76 contracts failed and 3 standard-library,
  precedence/non-scope, and protected-surface guards passed in 0.41 seconds.
- The runtime checkpoint passed 28 inherited M69/M75/M76 assertions; only the
  deliberately absent RFC/docs assertion failed. Ruff requested one mechanical
  format adjustment; lint and strict Pyright were clean.
- After documentation and formatting, all 10 M76 assertions pass in 0.25
  seconds. The exact M64-M76 inherited group passes 136 assertions with 1 local
  filesystem-capability skip in 1.66 seconds. Strict docs build in 1.26 seconds
  with only the known upstream notice; affected static checks and whitespace
  pass.
- The complete local gate passes on CPython 3.12-3.14, all 825 architecture
  assertions, 10 real-wgpu tests, both five-repeat profiles, both vertical
  slices, and all four diagnostic validators. Two builds reproduce a pure
  274,258-byte wheel and 1,262,791-byte sdist; all distribution/release smokes
  pass.
- Findings-first review corrected one overbroad documentation implication:
  M76 observes central-directory flags exposed by `ZipInfo` and does not claim
  detection of local-header-only inconsistencies. The corrected 10-test focus,
  all 825 architecture assertions, whole-tree static gate, strict docs, and
  whitespace pass.
- Record-inclusive builds reproduce a 274,273-byte wheel at
  `373dbe9ad78c4c2ba6ff96e7533a84cc812057f2a985aea06c491706112fe40f`
  and a 1,264,049-byte sdist at
  `d11c63366f4e44405f8b4b02442ef6cca9db952c3068ac82202017fc1191e96a`;
  wheel, staging, and complete release smokes pass.
- The final scope/hygiene audit is clean at exactly 16 intended paths. Protected
  hashes and archive boundaries are unchanged; credential/private-key and
  explicit development-tool identity scans return zero matches; retired
  repository-control metadata remains absent. History is linear from exact M75
  closeout, only the intended local branch exists beside `main`, only
  `origin/main` exists remotely, and GitHub reports no open PR, tag, or release.
- After neutralizing a retired-directory literal caught by M59, the corrected
  post-record gate passes all 825 architecture assertions with 1 capability
  skip; static checks, strict docs, whitespace, and exact 16-path scope pass.

## Remaining gates

1. Create one DCO feature commit and publish a
   ready PR, wait for exact-head hosted qualification, audit review state,
   squash-merge, and verify the resulting main commit.
2. Publish the neutral integration-record and closeout PRs only after their
   bounded gates; delete all milestone branches and generated artifacts, then
   return to clean synchronized `main`.
