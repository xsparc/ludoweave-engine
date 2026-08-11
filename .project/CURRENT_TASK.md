# Current Task

- **Task:** M65 - portable sample member paths
- **Status:** Initial ready PR #147 passed the unchanged three-allocation hosted
  gate at exact head `fce4140dd2d1b2982a1e90091dd2b157b00e861c`, but review
  found that explicitly encoded non-regular ZIP modes were not rejected. The
  tests-first correction passes the complete local source, supported-Python,
  real-wgpu, profile, example, reproducibility, wheel, and release gates. A DCO-
  signed amended head and fresh hosted qualification remain required.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M64 closeout
  `92e706961e2ecd4e2c187a205cc045a8c6506ab9`, whose tree
  `8df4aaa8222517d729234792d162dfc115674767` exactly matches the reviewed
  closeout head. GitHub reports a valid signature and parsed DCO trailer. Only
  `main` existed locally/remotely, no pull request was open, `git fsck` passed,
  and the closeout created no run or check.
- **Outcome:** Give every admitted staged sample-ZIP file one deterministic
  portable extraction identity before the first filesystem write.
- **Acceptance:** Require an exact expected root; one or more portable ASCII
  components; at most 255 relative characters; no trailing period or Windows
  device stem; no explicit directory entry or explicitly encoded non-regular
  file type; case-insensitive complete-path uniqueness; one exact ancestor
  spelling; and no file/directory prefix collision. Retain exact spelling,
  common-producer compatibility for missing type bits, and all M64 bounds.
- **Boundary:** Private project-owned sample-bundle verification only. No
  Unicode normalization, locale comparison, filesystem probing, path rewriting,
  general archive sandbox, absolute-path portability guarantee, cleanup or
  rollback, workflow, dependency, sample producer, runtime API, release
  authority, tag, release, publication, or real public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Failing baseline:** The new 18-case M65 file failed 16 assertions and passed
  the valid nested-shape plus protected-surface guards in 0.56 seconds against
  unchanged M64 production code. Nonportable inputs wrote before incomplete-
  bundle failure or reached host `OSError`; duplicate/case-only paths overwrote
  or merged; prefix collisions failed after writes; the 255-character constant,
  collision preflight, and RFC-0048 were absent.
- **Development evidence:** The first focused gate stopped because Ruff would
  reformat the new test file. After mechanical formatting, both changed Python
  files are format/Ruff/strict-Pyright clean and all 17 non-documentation M65
  assertions pass in 0.26 seconds. The complete 18-case contract passes in 0.23
  seconds; strict docs build in 1.11 seconds with only the known upstream
  notice; all 720 architecture assertions and both release-artifact tests pass.
- **Pre-hosted candidate evidence:** Each graphics-enabled CPython 3.12.13,
  3.13.13, and
  3.14.5 suite passes 2,260 tests with 14 expected skips. Ten real-wgpu tests,
  five-repeat base/graphics profiles, Clockwork Arena, Agent World Builder, and
  all four diagnostic benchmark validators pass. Two builds reproduce a pure
  272,430-byte wheel and 1,169,917-byte source archive; isolated-wheel and
  complete release smoke pass.
- **Review:** Local findings-first review first strengthened the admitted exact
  255-character boundary. Hosted review then found a production defect: a ZIP
  FIFO, socket, or device mode without a trailing slash passed the filename-
  based directory and symlink guards. Four reviewer-derived regressions failed
  against the published head and pass after explicit file-type validation.
- **Corrected source and matrix gate:** After the correction, the unchanged lock
  and restored 45-package graphics environment pass whole-tree formatting,
  Ruff, strict Pyright, 727 architecture/release assertions, strict docs, and
  whitespace. Each supported graphics-enabled CPython suite passes 2,265 tests
  with 14 expected skips. Ten real-wgpu tests, both five-repeat profiles, and
  both vertical slices pass. Two builds reproduce a pure 272,430-byte wheel and
  1,172,451-byte source archive; isolated-wheel, staging, and complete release
  smoke pass.
- **Initial hosted evidence:** Run `31521633593` passed exact initial head
  `fce4140dd2d1b2982a1e90091dd2b157b00e861c` in three Linux-first
  allocations: Linux `93879809651` in 5m24s, macOS `93881371543` in 2m50s,
  and Windows `93881371674` in 4m05s. Merge remains blocked pending a fresh run
  because that head contains the confirmed non-regular-mode gap.
- **Required validation:** Unchanged lock/environment; whole-tree formatting,
  Ruff, strict Pyright, focused and inherited architecture/release tests, strict
  docs, all supported CPython versions, real-wgpu, profiles, both vertical
  slices, documented diagnostic benchmarks, twice-reproducible distribution,
  isolated-wheel smoke, complete release smoke, diff/history/security/archive
  review, exact amended DCO commit, and a fresh unchanged three-allocation
  hosted gate.
