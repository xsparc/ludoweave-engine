# Current Task

- **Task:** M63 - public release subordinate-output confinement
- **Status:** Implementation, local review, exact three-allocation hosted
  qualification, and feature squash integration are complete. This bounded
  four-document integration record is locally validated on
  `records/m63-integration`; hosted review remains pending.
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
- **Hosted evidence:** Ready PR #141 exact head
  `8fe7518efb1855c69f3f093eba921721421072ce` passed run `31507526704` in
  exactly three Linux-first allocations. Linux job `93832810911` passed in
  7m07s before macOS `93835048148` and Windows `93835048154` began; they passed
  in 2m59s and 3m11s. Baseline passed 2,233 tests; Ubuntu 3.13/3.14 and both
  desktop 3.14 suites each passed 2,233 with one expected skip. Hosted builds
  reproduced a 272,038-byte wheel at `df7348f0a9911611e1df59e91151b00320f8a4a5a86fcf97def39ac008d41b22`
  and a 1,151,376-byte source archive at
  `eb400512913e1d2cd748dc93f1c4bab26699d4878edb882e54cab2661c261cfb`;
  installed-wheel and complete release smoke passed. Two delayed full review
  audits were empty. GitHub-verified squash
  `e0f1dc683d5e38b69d01d342f843074470a8418a` has the exact reviewed tree, sole
  parent exact M62 closeout, and parsed DCO trailer.
