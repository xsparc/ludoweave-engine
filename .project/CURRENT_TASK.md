# Current Task

- **Task:** M65 - portable sample member paths
- **Status:** Corrected feature PR #147 and integration-record PR #148 are fully
  validated, reviewed, squash-integrated, and verified. This exact three-record
  closeout establishes the clean M66 selection base without requesting hosted
  CI.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** GitHub-verified integration squash
  `b88090a78fdd6cb4978863e0792d7741cd07efb3`, whose tree
  `2c24ce9d68e7068d745f794a423b6d6d60d971b2` exactly matches reviewed PR
  #148 head `1401a2423bdbd001c359735a365f4be14a010d60`. Its sole parent is the M65
  feature squash `b01335592d0e984c6b3eb6a35d31294081cff0d5`; GitHub reports a valid
  signature and exact parsed DCO trailer.
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
  and Windows `93881371674` in 4m05s. Merge was blocked because that head
  contained the confirmed non-regular-mode gap.
- **Corrected hosted evidence:** Exact amended head `9de1e2e6` passed run
  `31523863615` in three Linux-first allocations: Linux `93887270228` in
  7m32s, macOS `93889429991` in 2m09s, and Windows `93889429975` in 4m11s.
  Static/docs, supported Python, real-wgpu, profiles, both vertical slices,
  reproducible distribution, isolated-wheel smoke, staging, and corrected
  complete release smoke all passed.
- **Review resolution:** The valid mode-type finding was answered with the
  tests-first correction and resolved only after the fresh hosted pass. Two
  delayed exact-head audits found no later review, issue comment, review
  comment, or unresolved thread.
- **Integration evidence:** Exact four-document head `1401a242` passed run
  `31525664897` in one 43-second Linux allocation; the desktop umbrella skipped
  with zero steps. Hosted formatting, Ruff, strict docs, 725 architecture
  assertions, reproducible distribution, isolated-wheel smoke, staging, and
  complete release smoke passed. Two delayed audits were empty. Squash
  `b88090a` has the exact reviewed tree, valid signature, sole parent the
  feature squash, and parsed DCO.
- **Closeout gate:** Change exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md`; run architecture,
  strict docs, scope, Git-object, and whitespace checks; create a DCO-signed
  ready PR that requests no hosted runner; verify the squash; delete every M65
  branch locally/remotely; clean only verified generated M65 outputs; and leave
  synchronized clean `main` before selecting M66.
