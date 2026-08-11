# Current Task

- **Task:** M63 - public release subordinate-output confinement
- **Status:** Script correction, regression suite, RFC, public documentation,
  complete local validation, and findings-first review are complete on
  `security/m63-public-release-output-confinement`; hosted publication remains
  pending.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M62 closeout
  `1cdc1b452cbe79c9e4f082acb4dd1205f4b3648f`, whose tree
  `03abc8d3a45b568e98eebcd9a492e6f96ff71049` exactly matches the reviewed
  closeout head. GitHub reports a valid signature and parsed DCO trailer. Only
  `main` existed locally/remotely, no pull request was open, the closeout
  created no run or check, and no post-closeout `main` run exists.
- **Outcome:** Preserve the public consumer's documented one-JSON-document
  output when it invokes in-process release validation and complete smoke.
- **Acceptance:** Redirect subordinate stdout and subordinate stderr on normal
  return and exception; accept only an exact built-in zero integer without
  comparison/truth hooks; retain content-silent document/smoke failure codes;
  emit exactly one JSON document on the consumer's designated channel.
- **Boundary:** The process-global redirection is admitted only for this single-
  thread standalone utility. No direct file-descriptor or arbitrary subprocess
  capture, concurrency claim, subprocess wrapper, cleanup, rollback, retry,
  workflow, runner allocation, dependency, lock, version, runtime package/API,
  release authority, tag, release, publication, or real public release
  observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Development evidence:** Against unchanged M62 production code, the initial
  11-case M63 file failed ten assertions and passed the protected-surface guard
  in 0.46 seconds. Smoke output escaped on success, nonzero failure, and
  exception; boolean and float zero values were accepted; hostile comparison
  hooks escaped; and RFC-0046 was absent. The minimal script correction passed
  all ten non-documentation assertions with one docs assertion deselected in
  0.69 seconds. The first focused static gate stopped because the test annotated
  pytest's non-public capture-result type; after returning plain strings, both
  changed Python files are formatted, Ruff clean, and strict-Pyright clean.
  The complete documented contract passes all 11 assertions in 0.24 seconds,
  and strict docs build in 1.14 seconds. The inherited contracts initially
  exposed three stale literal guards, then one remaining order guard; after
  strengthening them, all 688 architecture assertions pass in 4.81 seconds
  and the release-draft suite passes 56 tests with two expected skips in 5.15
  seconds. The complete candidate then passed 2,228 tests with 14 expected
  skips on each supported CPython version, the real renderer/profile/examples,
  all four diagnostic benchmark validators, and reproducible artifact smoke.
  Findings-first review added direct validator exception-restoration coverage;
  the strengthened M63 file now passes 12 tests and the architecture suite 689.
  The final record-inclusive candidate passes 2,229 tests with 14 expected
  skips on each supported CPython version, final renderer/profile/examples and
  diagnostic benchmark gates, and a twice-reproduced local distribution with
  installed-wheel and complete release smoke.
- **Hosted gate:** This security/documentation maintenance slice is substantive
  and requires exactly three Linux-first allocations; desktop jobs may begin
  only after Linux qualification succeeds.
