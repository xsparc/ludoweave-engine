# Current Task

- **Task:** M60 - public release filesystem collision conformance
- **Status:** Feature hosted-qualified, reviewed, and squash-integrated;
  factual integration record is in progress on `records/m60-integration`.
- **Started:** 2026-08-11
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M59 closeout
  `9ba74e55b5c47d5f0bd030b53ad6a35a361c5735`, whose tree exactly matches the
  reviewed closeout candidate. GitHub reports a valid signature and DCO; only
  `main` existed locally/remotely, with no open pull request or closeout run.
- **Outcome:** Reject every pre-existing final directory entry used for fresh
  public-release output before network or validator side effects, including a
  dangling link that ordinary following existence checks report absent.
- **Acceptance:** The release document, output directory, fresh retrieval plan,
  asset target, and asset partial use non-following final-entry inspection.
  Files, directories, live links, dangling links, and inspection failures fail
  closed with stable, content-silent codes before download/connection work.
  Exclusive creation and hard-link publication retain no clobber behavior.
- **Boundary:** No race-free filesystem claim, directory-descriptor sandbox,
  rollback, cleanup, retry, workflow, runner-allocation, dependency, lock,
  version, runtime package/API, release authority, tag, release, publication,
  or real public release observation. Community-reserved tasks and deferred
  product proposals remain untouched.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Baseline:** The focused inherited M45-M58 and release-draft boundary passed
  317 tests with two platform-capability skips in 7.19 seconds. The first
  sandboxed `uv lock --check` was denied access to uv's existing user cache;
  the approved rerun resolved the unchanged 46-package lock in 0.83 ms.
- **Development evidence:** All eight initial assertions failed on the unchanged
  verifier. Six behavior cases reached an intentionally forbidden download or
  connection path; the scope fixture initially used one stale release-workflow
  hash; and the documentation contract named the intentionally absent RFC.
  After correcting the test-fixture hash and implementing final-entry
  `lstat()` inspection, the seven behavior/scope assertions passed in 0.21
  seconds. Documentation and two later edge-case regressions brought the final
  M60 group to ten passing assertions on CPython 3.12-3.14. The record-inclusive
  gate passes the unchanged lock, 303-file formatting, Ruff, strict Pyright,
  648 architecture assertions, strict docs, 2,188 baseline tests with 14
  expected skips, reproducible pure distributions, isolated-wheel smoke,
  complete release smoke, archive/scope/credential checks, and whitespace.
  Earlier complete graphics-enabled suites on CPython 3.13/3.14 each passed
  2,187 tests with 14 expected skips before the final test addition; the final
  ten M60 assertions pass on both versions.
- **Hosted gate:** Ready PR #132 exact head
  `836c1e14bbfe0e9bb94dbe1fc84df600279e0b23` passed run `31488972656`
  in exactly three Linux-first allocations. Linux job `93770741704` passed in
  7m25s before macOS `93772531511` and Windows `93772531611` began; they passed
  in 2m28s and 3m17s. Every complete compatibility suite passed 2,192 tests,
  with one expected skip outside the baseline. Every platform passed ten real-
  graphics tests, profile smoke, Clockwork Arena, and Agent World Builder.
- **Integration:** Two review audits found exact head/base, `MERGEABLE/CLEAN`,
  three successful checks, and no comment, review, or thread. Head-pinned
  GitHub-verified squash `8967bd8cfc11f1b29caadbf01da9255bd6eb4584` has tree
  `e17d11565f30e58b6eb705926702e257026f9b3b` exactly equal to the reviewed
  feature head and sole parent exact M59 closeout. The DCO-signed feature commit
  remains attached to PR #132. The generated squash body contains literal
  escaped newline text, so no parsed-trailer claim is made for that commit and
  public history is not rewritten. The feature branch is deleted locally and
  remotely; no post-merge `main` run or open PR exists.
